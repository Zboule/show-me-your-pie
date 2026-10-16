"""Tests for the pipeline and the built dataset.

    python3 -m unittest discover -s pipeline/tests -v

Model tests (top_tail) run on their own. Dataset tests read
site/data/france.json and are skipped with a message if it has not been
built. Where possible a test compares two things computed differently, so it
can fail; tests that are true by construction were removed.
"""
import json
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pipeline"))
import top_tail  # noqa: E402

DATA_PATH = ROOT / "site" / "data" / "france.json"
METHOD_DOC = ROOT / "docs" / "03-method.md"


class TopTailModel(unittest.TestCase):
    def test_pareto_share_matches_closed_form_for_several_alphas(self):
        # Inside a Pareto top bin, the richest fraction f holds f^(1 - 1/alpha).
        for alpha in (1.5, 2.0, 3.0):
            bins = [(99.999, 100.0, 1.0)]
            full = top_tail.top_n_wealth(0.001, bins, alpha)
            part = top_tail.top_n_wealth(0.0005, bins, alpha)
            self.assertAlmostEqual(part / full, 0.5 ** (1 - 1 / alpha), places=9, msg=alpha)

    def test_chain_alpha(self):
        # Threshold doubles while the top share falls 4x: alpha = ln 4 / ln 2 = 2.
        self.assertAlmostEqual(top_tail.chain_alpha(10, 20, 4), 2.0, places=12)
        with self.assertRaises(ValueError):
            top_tail.chain_alpha(10, 100, 2)  # alpha < 1

    def test_guards(self):
        bins = [(99.999, 100.0, 5.0), (99.998, 99.999, 1.0)]
        with self.assertRaises(ValueError):
            top_tail.top_n_wealth(0.01, bins, 2)  # more than the bins cover
        with self.assertRaises(ValueError):
            top_tail.top_n_wealth(0.001, list(reversed(bins)), 2)  # wrong order
        with self.assertRaises(ValueError):
            top_tail.top_n_wealth(0.0005, bins, 1.0)  # split of the top bin needs alpha > 1
        self.assertAlmostEqual(top_tail.top_n_wealth(0.0015, bins, None), 5.0 * 0.001 + 1.0 * 0.0005, places=12)  # whole top bin: no alpha needed

    def _toy(self, rl_multiple, params, top_share=0.05):
        mean, adults = 1e5, 5e7
        total = mean * adults
        n_top = adults * 1e-5  # people in the top bin
        bins = [(99.999, 100.0, top_share * total / n_top)]
        shares, bounds = [1 - top_share, top_share], [(0, 99.999), (99.999, 100)]
        return top_tail.scenario_shares(shares, bounds, bins, 2.0, mean, adults, rl_multiple * top_share * total, params), total

    def test_correction_hits_the_list_exactly(self):
        # Whole top bin covered: n = members × 1.8 adults must equal the bin.
        params = {"members_per_family": 500 / (500 * top_tail.ADULTS_PER_MEMBER), "non_resident_share": 0}
        (out, w_n, rl_adj), total = self._toy(2.0, params)
        self.assertAlmostEqual(w_n / total, 0.05, places=9)
        self.assertAlmostEqual(out[1], 0.10, places=9)        # list = 2 × WID top
        self.assertAlmostEqual(out[0], 0.90, places=9)
        self.assertAlmostEqual(sum(out), 1, places=12)

    def test_non_resident_cut_and_no_correction_below_wid(self):
        params = {"members_per_family": 500 / (500 * top_tail.ADULTS_PER_MEMBER), "non_resident_share": 0.6}
        (out, w_n, rl_adj), total = self._toy(2.0, params)  # 2 × 0.4 = 0.8 of WID
        self.assertIsNone(out)
        self.assertAlmostEqual(rl_adj / w_n, 0.8, places=9)

    def test_straddling_layer_by_hand(self):
        # Layers [0,99.99), [99.99,99.999), [99.999,100]; list covers the top
        # 0.002% (top bin + half of the next g-percentile band).
        mean, adults = 1e5, 1e8
        total = mean * adults
        bins = [(99.999, 100.0, 4e9), (99.998, 99.999, 1e9)] + [(99.99 + i / 1000, 99.991 + i / 1000, 5e8) for i in range(7, -1, -1)]
        w = [b[2] * (b[1] - b[0]) / 100 * adults for b in bins]
        top, mid = w[0], sum(w[1:])
        shares = [(total - top - mid) / total, mid / total, top / total]
        bounds = [(0, 99.99), (99.99, 99.999), (99.999, 100)]
        n = 0.002 / 100 * adults
        params = {"members_per_family": n / (500 * top_tail.ADULTS_PER_MEMBER), "non_resident_share": 0}
        w_n = top + w[1]
        rl = 1.5 * w_n
        out, got_wn, _ = top_tail.scenario_shares(shares, bounds, bins, 2.0, mean, adults, rl, params)
        self.assertAlmostEqual(got_wn, w_n, delta=1e-6 * w_n)
        scale = (total - rl) / (total - w_n)
        self.assertAlmostEqual(out[2], top * 1.5 / total, places=9)
        self.assertAlmostEqual(out[1], (w[1] * 1.5 + (mid - w[1]) * scale) / total, places=9)
        self.assertAlmostEqual(sum(out), 1, places=12)


class Dataset(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not DATA_PATH.exists():
            raise unittest.SkipTest(f"{DATA_PATH} not built: run pipeline/build_data.py first")
        text = DATA_PATH.read_text(encoding="utf-8")

        def no_constants(name):
            raise ValueError(f"non-standard JSON constant {name}")
        cls.D = json.loads(text, parse_constant=no_constants)

    def test_layers_agree_with_published_shares(self):
        # Layers are summed from g-percentiles; WID's published group shares
        # are an independent rounding of the same distribution.
        for code, c in self.D["concepts"].items():
            for k, L in c["layers"].items():
                for y, s, p in zip(c["years"], L["share"], L["share_published"]):
                    if s is not None and p is not None:
                        self.assertLess(abs(s - p), 2e-4, f"{code} {k} {y}")

    def test_middle_40_matches_wid_direct_share(self):
        c = self.D["concepts"]["hweal"]
        for y, s, p in zip(c["years"], c["layers"]["p50p90"]["share"], c["share"]["p50p90"]):
            if s is not None and p is not None:
                self.assertLess(abs(s - p), 2e-4, y)

    def test_layer_averages_increase_up_the_distribution(self):
        for code, c in self.D["concepts"].items():
            layers = sorted(c["layers"].values(), key=lambda l: l["bounds"][0])
            for i, y in enumerate(c["years"]):
                avgs = [l["avg"][i] for l in layers]
                self.assertEqual(avgs, sorted(avgs), msg=f"{code} {y}")

    def test_thresholds_increase(self):
        for code, c in self.D["concepts"].items():
            ranks = sorted(c["threshold"], key=float)
            for i, y in enumerate(c["years"]):
                vals = [c["threshold"][r][i] for r in ranks if c["threshold"][r][i] is not None]
                self.assertEqual(vals, sorted(vals), msg=f"{code} {y}")

    def test_threshold_average_coherence(self):
        # t_j <= a_j <= t_{j+1} for every g-percentile; violations are recorded.
        for code, issues in self.D["meta"]["coherence_issues"].items():
            self.assertEqual(issues, [], code)

    def test_g_percentiles_rebuild_the_published_mean_every_year(self):
        for code, c in self.D["concepts"].items():
            widths = [hi - lo for lo, hi in (map(float, b[1:].split("p")) for b in c["gp"]["bins"])]
            self.assertAlmostEqual(sum(widths), 100, places=6)
            for i, y in enumerate(c["years"]):
                col = [c["gp"]["avg"][j][i] for j in range(len(widths))]
                if None in col or c["avg"]["p0p100"][i] is None:
                    continue
                mean = sum(w * a for w, a in zip(widths, col)) / 100
                self.assertAlmostEqual(mean / c["avg"]["p0p100"][i], 1, delta=0.02, msg=f"{code} {y}")

    def test_price_base_year(self):
        self.assertEqual(self.D["deflator"][str(self.D["meta"]["price_base_year"])], 1)

    def test_comparison_wiring(self):
        groups = {"wealth_top10": ("hweal", "p90p100"), "wealth_top5": ("hweal", "p95p100"),
                  "wealth_top1": ("hweal", "p99p100"), "wealth_bottom50": ("hweal", "p0p50"),
                  "income_top10": ("diinc", "p90p100"), "income_bottom50": ("diinc", "p0p50")}
        for key, (code, group) in groups.items():
            wid = next(s for s in self.D["comparison"][key] if s["source"].startswith("WID"))
            self.assertEqual(wid["values"], self.D["concepts"][code]["share"][group], key)
            for s in self.D["comparison"][key]:
                self.assertEqual(len(s["years"]), len(s["values"]))
                for v in s["values"]:
                    self.assertTrue(v is None or 0 <= v <= 1, f"{key} {s['source']} {v}")

    def test_scenario_deflation_of_rich_list(self):
        # The rich-list check must hold the Challenges total, deflated, times (1 − c).
        sc = self.D["concepts"]["hweal"]["scenarios"]
        chk = sc["rich_list_check"]["ggp_low"]
        y = chk["years"][-1]
        raw = float(self.D["rich_lists"]["challenges_500"][str(y)]["total_eur_bn"]) * 1e9
        expected = raw / self.D["deflator"][str(y)] * (1 - sc["params"]["ggp_low"]["non_resident_share"])
        self.assertAlmostEqual(chk["list_eur"][-1] / expected, 1, delta=1e-6)

    def test_scenarios_sum_to_one_and_respect_direction(self):
        c, sc = self.D["concepts"]["hweal"], self.D["concepts"]["hweal"]["scenarios"]
        for name, layers in sc["layers"].items():
            for j, y in enumerate(sc["years"][name]):
                self.assertAlmostEqual(sum(l[j] for l in layers.values()), 1, delta=1e-5, msg=f"{name} {y}")
                wid = c["layers"]["p99.999p100"]["share"][c["years"].index(y)]
                top = layers["p99.999p100"][j]
                if name == "dwa_lower":
                    self.assertLessEqual(top, wid + 1e-9, y)
                else:
                    self.assertGreaterEqual(top, wid - 1e-9, y)

    def test_scenario_values_match_method_doc(self):
        # Oracle: the 2024 table in docs/03-method.md must match the build.
        doc = METHOD_DOC.read_text(encoding="utf-8")
        c, sc = self.D["concepts"]["hweal"], self.D["concepts"]["hweal"]["scenarios"]
        for name in sc["layers"]:
            years = sc["years"][name]
            if 2024 not in years:
                continue
            value = sc["layers"][name]["p99.999p100"][years.index(2024)]
            self.assertTrue(f"`{name}` | {value * 100:.1f}%" in doc, f"{name}: 2024 value {value * 100:.1f}% missing from the method doc")

    def test_ipp_amounts(self):
        t = self.D["ipp_top_income"]
        for key, m in t["measures"].items():
            self.assertTrue(all(v is not None and v > 0 for v in m["bn"]), key)
        # Group sizes: each IPP group is 10x the next one.
        hh = t["measures"]["taxable"]["households"]
        for a, b in zip(hh, hh[1:]):
            self.assertAlmostEqual(a / b, 10, delta=0.01)

    def test_no_non_finite_numbers(self):
        def walk(x):
            if isinstance(x, float):
                self.assertTrue(math.isfinite(x))
            elif isinstance(x, dict):
                for v in x.values():
                    walk(v)
            elif isinstance(x, list):
                for v in x:
                    walk(v)
        walk(self.D)


if __name__ == "__main__":
    unittest.main()


class Paper(unittest.TestCase):
    def test_every_generated_number_appears_in_the_paper(self):
        numbers = ROOT / "paper" / "numbers.json"
        if not numbers.exists():
            self.skipTest("run pipeline/paper_numbers.py first")
        import re
        text = re.sub(r"\s+", " ", (ROOT / "paper" / "paper.md").read_text(encoding="utf-8"))
        # Whole-number match: "22" must not be found inside "2022" or "22.5".
        def quoted(v):
            return re.search(r"(?<![\d.,])" + re.escape(v) + r"(?![\d])", text) is not None
        missing = {k: v for k, v in json.loads(numbers.read_text(encoding="utf-8")).items() if not quoted(v)}
        self.assertEqual(missing, {}, "numbers in paper/numbers.json not quoted in paper/paper.md")

    def test_numbers_file_is_current(self):
        # Regenerating from the built dataset must give the committed file.
        import subprocess, tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "numbers.json"
            subprocess.run([sys.executable, "-I", str(ROOT / "pipeline" / "paper_numbers.py"), str(DATA_PATH), str(out)],
                           check=True, capture_output=True)
            self.assertEqual(json.loads(out.read_text(encoding="utf-8")),
                             json.loads((ROOT / "paper" / "numbers.json").read_text(encoding="utf-8")))


class Provenance(unittest.TestCase):
    def test_built_from_current_manual_files(self):
        # The committed dataset must have been built from the hand-compiled
        # files as they are now (otherwise it carries stale rows and sources).
        import hashlib
        D = json.loads(DATA_PATH.read_text(encoding="utf-8"))
        recorded = {k: v for k, v in D["meta"]["inputs_sha256"].items() if k.startswith("manual/")}
        self.assertTrue(recorded, "no manual inputs recorded")
        for name, digest in recorded.items():
            path = ROOT / "data" / name
            self.assertTrue(path.exists(), f"{name} recorded but missing")
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest, f"{name} changed since the build")
        on_disk = {f"manual/{p.name}" for p in (ROOT / "data" / "manual").glob("*.csv")}
        self.assertEqual(on_disk, set(recorded), "manual files added or removed since the build")


class PageCore(unittest.TestCase):
    def test_javascript_core(self):
        import shutil, subprocess
        node = shutil.which("node")
        if not node:
            self.skipTest("Node.js not installed")
        r = subprocess.run([node, "--test", str(ROOT / "pipeline" / "tests" / "test_core.mjs")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout[-2000:] + r.stderr[-2000:])
