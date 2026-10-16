"""Turn the raw WID + INSEE files into the yearly series the page draws.

    python3 -I pipeline/build_data.py <raw_dir> <out.json> [manual_dir] [--partial]

manual_dir defaults to data/manual in the repository. Every cross-check
source must have been fetched; pass --partial to build without the missing
ones (the output then records which sources were left out).

Units: WID averages and thresholds are per adult (20+), income split equally
within couples, in constant euros of the WID price base year (the year where
the national-income price index `inyixxi999` equals 1).
"""
import csv
import datetime
import hashlib
import inspect
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "pipeline"))  # -I drops the script dir
import top_tail  # noqa: E402
from sources import SOURCES  # noqa: E402

CONCEPTS = {
    "ptinc": "Pre-tax national income",
    "diinc": "Post-tax national income (after taxes, cash and in-kind transfers, public services)",
    "hweal": "Net personal wealth",
}
GROUPS = ["p0p100", "p0p50", "p50p90", "p90p100", "p95p100", "p99p100", "p99.9p100", "p99.99p100", "p99.999p100"]
# Non-overlapping layers that partition the adult population; transfers are
# measured between these. Bounds are percentile ranks.
LAYERS = [(0, 50), (50, 90), (90, 99), (99, 99.9), (99.9, 99.99), (99.99, 99.999), (99.999, 100)]
THRESHOLDS = ["10", "25", "50", "75", "90", "95", "99", "99.5", "99.9", "99.99", "99.999"]
COMPOSITION_ITEMS = ["hou", "bus", "fin", "deb"]
FIRST_YEAR = 1900


class DataError(ValueError):
    """An input does not have the shape or values the method relies on."""


def check(condition, message):
    # Not `assert`: data checks must survive `python -O`.
    if not condition:
        raise DataError(message)


def pct(x):
    """Percentile rank as WID writes it: 99.9 -> '99.9', 50.0 -> '50'."""
    return f"{x:.3f}".rstrip("0").rstrip(".")


def g_percentile_bins():
    """WID's 127 generalized-percentile bins: p0p1 ... p99.999p100."""
    edges = [float(p) for p in range(0, 99)]
    edges += [99 + i / 10 for i in range(10)]
    edges += [99.9 + i / 100 for i in range(1, 10)]
    edges += [99.99 + i / 1000 for i in range(1, 11)]
    return [f"p{pct(a)}p{pct(b)}" for a, b in zip(edges, edges[1:])]


def load_wid(path):
    wanted = re.compile(r"^(?:[ats](?:ptinc|diinc|hweal)j992|ahw(?:hou|bus|fin|deb)j992|inyixxi999|npopuli992|xlcusxi999)$")
    data = defaultdict(dict)  # (variable, percentile) -> {year: value}
    quality = defaultdict(dict)  # variable -> {year: WID data_quality flag}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            if wanted.match(row["variable"]) and row["value"]:
                data[(row["variable"], row["percentile"])][int(row["year"])] = float(row["value"])
                if row["percentile"] == "p0p100" and row["data_quality"]:
                    quality[row["variable"]][int(row["year"])] = int(row["data_quality"])
    return data, quality


def load_rich_lists(manual_dir):
    """Hand-compiled rich-list totals (one source URL per row), if present."""
    out = {}
    for name, value_cols in [("challenges_500", ("total_eur_bn",)), ("forbes_france_billionaires", ("total_usd_bn", "total_eur_bn", "n_billionaires"))]:
        path = Path(manual_dir) / f"{name}.csv"
        if not path.exists():
            continue
        rows = {}
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if any(row.get(col, "").strip() for col in value_cols):
                    rows[row["year"]] = {k: v for k, v in row.items() if v not in ("", None)}
        out[name] = rows
    return out


def series(data, variable, percentile, years, digits=0):
    values = data.get((variable, percentile), {})
    return [round(values[y], digits) if y in values else None for y in years]


def bin_bounds(name):
    lo, hi = re.match(r"p([\d.]+)p([\d.]+)$", name).groups()
    return float(lo), float(hi)


def build_layers(data, code, years):
    """Share and average of each layer, summed from WID's g-percentiles.

    WID's 127 g-percentile averages are published at full precision, while
    group shares are rounded to 4 decimals (±1e-4 of the total, about ±0.5% of
    the thinnest layer). So each layer is the sum of the bins it covers:

        wealth[a,b) = sum over bins in [a,b) of avg_bin × width_bin
        share[a,b)  = wealth[a,b) / sum over all bins
        avg[a,b)    = wealth[a,b) / (b − a)

    WID's published shares are kept as `share_published` and used as an
    independent check. A year with a missing bin falls back to differencing
    the published top shares and is listed in `fallback_years`.
    """
    bins = [(b, *bin_bounds(b)) for b in g_percentile_bins()]
    out = {f"p{pct(a)}p{pct(b)}": {"share": [], "avg": [], "share_published": [], "bounds": [a, b]} for a, b in LAYERS}
    fallback = []

    def top_share(a, y):
        if a == 0:
            return 1.0
        if a == 50:
            return 1 - data[(f"s{code}j992", "p0p50")][y]
        return data[(f"s{code}j992", f"p{pct(a)}p100")][y]

    for y in years:
        mass = {}
        try:
            per_bin = [(lo, hi, data[(f"a{code}j992", name)][y] * (hi - lo)) for name, lo, hi in bins]
            total = sum(m for _, _, m in per_bin)
            for a, b in LAYERS:
                mass[(a, b)] = sum(m for lo, hi, m in per_bin if lo >= a - 1e-9 and hi <= b + 1e-9)
        except KeyError:
            per_bin = None
        for a, b in LAYERS:
            layer = out[f"p{pct(a)}p{pct(b)}"]
            try:
                published = top_share(a, y) - (top_share(b, y) if b < 100 else 0)
            except KeyError:
                published = None
            layer["share_published"].append(None if published is None else round(published, 6))
            if per_bin is not None:
                share = mass[(a, b)] / total
                avg = mass[(a, b)] / (b - a)
            elif published is not None and (f"a{code}j992", "p0p100") in data and y in data[(f"a{code}j992", "p0p100")]:
                share = published
                avg = published * data[(f"a{code}j992", "p0p100")][y] * 100 / (b - a)
            else:
                share = avg = None
            layer["share"].append(None if share is None else round(share, 6))
            layer["avg"].append(None if avg is None else round(avg))
        if per_bin is None:
            fallback.append(y)
    for key, layer in out.items():
        for y, s_, p_ in zip(years, layer["share"], layer["share_published"]):
            if s_ is not None and p_ is not None:
                # Independent check: WID's published shares (4 decimals) must agree.
                check(abs(s_ - p_) < 2e-4, f"{code} {y} {key}: bins give {s_}, WID share {p_}")
    return out, fallback


def extrapolated_from(quality):
    """First year of the trailing run of years flagged lower than the years before.

    WID lowers `data_quality` where it extends a benchmark forward (for France:
    wealth after 2014, income after 2018).
    """
    years = sorted(quality)
    last = quality[years[-1]]
    i = len(years) - 1
    while i > 0 and quality[years[i - 1]] == last:
        i -= 1
    return years[i] if i > 0 and quality[years[i - 1]] > last else None


def build_concept(data, quality, code):
    years = sorted(y for y in data[(f"a{code}j992", "p0p100")] if y >= FIRST_YEAR)
    bins = g_percentile_bins()
    layers, fallback = build_layers(data, code, years)
    q = quality[f"a{code}j992"]
    return {
        "extrapolated_from": extrapolated_from(q),
        "quality": [q.get(y) for y in years],
        "layers": layers,
        "layer_fallback_years": fallback,
        "label": CONCEPTS[code],
        "years": years,
        "avg": {g: series(data, f"a{code}j992", g, years) for g in GROUPS},
        "share": {g: series(data, f"s{code}j992", g, years, 5) for g in GROUPS if g != "p0p100"},
        # WID stores the threshold at rank p on the bin starting at p.
        "threshold": {
            t: series(data, f"t{code}j992", next(b for b in bins if b.startswith(f"p{t}p")), years)
            for t in THRESHOLDS
        },
        "gp": {"bins": bins, "avg": [series(data, f"a{code}j992", b, years) for b in bins]},
    }


def build_composition(data):
    deciles = [f"p{i}p{i + 10}" for i in range(0, 100, 10)]
    groups = {
        "p0p50": deciles[:5],
        "p50p90": deciles[5:9],
        "p90p100": ["p90p100"],
        "p99p100": ["p99p100"],
        "p99.9p100": ["p99.9p100"],
    }
    years = sorted(data[("ahwhouj992", "p99p100")])
    out = {"years": years, "groups": {}}
    for group, parts in groups.items():
        out["groups"][group] = {
            item: [
                round(sum(data[(f"ahw{item}j992", p)][y] for p in parts) / len(parts))
                for y in years
            ]
            for item in COMPOSITION_ITEMS
        }
    return out


# WIL Technical Note 2025/01 (Bajard et al. 2025, pp. 4-5): Forbes sources are
# harmonised from 1988 and WID's top g-percentile is raised to the Forbes total
# where lower. Shares of the top wealth bin are therefore calibrated from here.
FORBES_CALIBRATED_FROM = 1988


def top_bins_for(data, bins, y):
    """(lo, hi, avg) wealth g-percentiles from p99.9 up, ordered top down."""
    out = [(*bin_bounds(b), data[("ahwealj992", b)][y]) for b in bins if b.startswith("p99.9")]
    return sorted(out, key=lambda t: -t[0])


def build_scenarios(data, concept, rich_lists, deflator, adults, dwa):
    """Layer shares under alternative assumptions for the top of wealth.

    Rich-list scenarios: see top_tail.py. ECB / Banque de France scenario:
    WID's top-5% share is replaced by the DWA top-5% share (households) and
    every g-percentile above p95 is scaled by the same factor, everyone else
    by the complementary factor, so the total is unchanged.
    """
    challenges = rich_lists.get("challenges_500", {})
    # Real Challenges totals by year; years inside the covered range with no
    # published total are filled by geometric interpolation between the
    # neighbouring published years (recorded as interpolated), so scenario
    # lines do not drop back to WID for a single missing year.
    published = {int(y): float(r["total_eur_bn"]) * 1e9 / deflator[y]
                 for y, r in challenges.items() if r.get("total_eur_bn") and y in deflator}
    real_list, interpolated = dict(published), []
    if published:
        known = sorted(published)
        for y in range(known[0], known[-1] + 1):
            if y in published:
                continue
            a = max(k for k in known if k < y); b = min(k for k in known if k > y)
            real_list[y] = published[a] * (published[b] / published[a]) ** ((y - a) / (b - a))
            interpolated.append(y)
    keys = list(concept["layers"])
    bounds = [concept["layers"][k]["bounds"] for k in keys]
    bins = concept["gp"]["bins"]
    out = {"params": {**top_tail.SCENARIOS,
                      "dwa_lower": {"label": "ECB / Banque de France accounts: top 5% set to their (lower) level"}},
           "forbes_calibrated_from": FORBES_CALIBRATED_FROM,
           "layers": {}, "years": {}, "corrected_years": {}, "rich_list_check": {},
           "interpolated_list_years": interpolated}
    for name in out["params"]:
        out["layers"][name] = {k: [] for k in keys}
        out["years"][name] = []
        out["corrected_years"][name] = []
    for name in top_tail.SCENARIOS:
        out["rich_list_check"][name] = {"years": [], "wid_top_n_eur": [], "list_eur": [], "adults_covered": top_tail.adults_covered(top_tail.SCENARIOS[name])}

    for i, y in enumerate(concept["years"]):
        shares = [concept["layers"][k]["share"][i] for k in keys]
        if y in concept["layer_fallback_years"]:
            continue
        mean = sum(concept["layers"][k]["avg"][i] * (b - a) / 100 for k, (a, b) in zip(keys, bounds))
        if y in real_list:
            top = top_bins_for(data, bins, y)
            try:  # only needed if a list covered fewer adults than the top bin
                alpha = top_tail.chain_alpha(data[("thwealj992", "p99.99p99.991")][y],
                                             data[("thwealj992", "p99.998p99.999")][y], 5)
            except (KeyError, ValueError):
                alpha = None
            rl_real = real_list[y]
            for name, params in top_tail.SCENARIOS.items():
                new, w_n, rl_adj = top_tail.scenario_shares(shares, bounds, top, alpha, mean, adults[str(y)], rl_real, params)
                chk = out["rich_list_check"][name]
                chk["years"].append(y); chk["wid_top_n_eur"].append(round(w_n)); chk["list_eur"].append(round(rl_adj))
                if new is not None:
                    out["corrected_years"][name].append(y)
                    check(abs(sum(new) - 1) < 1e-5, f"{name} {y}: scenario shares sum to {sum(new)}")
                out["years"][name].append(y)
                for k, v in zip(keys, new or shares):
                    out["layers"][name][k].append(round(v, 6))
        if dwa and y in dwa["years"]:
            target = dwa["share"]["top5"][dwa["years"].index(y)]
            mass = [(lo, hi, data[("ahwealj992", b)][y] * (hi - lo)) for b in bins for lo, hi in [bin_bounds(b)]]
            total = sum(m for *_, m in mass)
            top5 = sum(m for lo, _, m in mass if lo >= 95 - 1e-9)
            f_top, f_rest = target * total / top5, (1 - target) * total / (total - top5)
            scaled = [(lo, hi, m * (f_top if lo >= 95 - 1e-9 else f_rest)) for lo, hi, m in mass]
            new = [sum(m for lo, hi, m in scaled if lo >= a - 1e-9 and hi <= b + 1e-9) / total for a, b in bounds]
            check(abs(sum(new) - 1) < 1e-6, f"dwa_lower {y}: shares sum to {sum(new)}")
            out["years"]["dwa_lower"].append(y)
            out["corrected_years"]["dwa_lower"].append(y)
            for k, v in zip(keys, new):
                out["layers"]["dwa_lower"][k].append(round(v, 6))
    out["topbin_check"] = topbin_check(data, concept["years"])
    return out


def topbin_check(data, years):
    """Entry threshold of the top 0.001% vs what the thresholds just below imply.

    alpha from p99.99 → p99.998 (rank ratio 5); projecting that slope from
    p99.998 to p99.999 (rank ratio 2) gives the threshold a smooth Pareto tail
    would have.
    """
    out = []
    for y in years:
        try:
            t1, t2, t3 = (data[("thwealj992", b)][y] for b in ("p99.99p99.991", "p99.998p99.999", "p99.999p100"))
            alpha = top_tail.chain_alpha(t1, t2, 5)
        except (KeyError, ValueError):
            continue
        out.append({"year": y, "threshold": round(t3), "projected": round(t2 * 2 ** (1 / alpha)), "alpha_chain": round(alpha, 3)})
    return out


def coherence(data, code, years):
    """Years and bins where a g-percentile average lies outside its thresholds
    (t_j <= a_j <= t_{j+1} must hold in any distribution)."""
    bins = g_percentile_bins()
    issues = []
    for y in years:
        for j, b in enumerate(bins):
            t = data.get((f"t{code}j992", b), {}).get(y)
            a = data.get((f"a{code}j992", b), {}).get(y)
            t_next = data.get((f"t{code}j992", bins[j + 1]), {}).get(y) if j + 1 < len(bins) else None
            if t is None or a is None:
                continue
            if a < t - 1 or (t_next is not None and a > t_next + 1):
                issues.append({"year": y, "bin": b, "threshold": t, "average": a, "next_threshold": t_next})
    return issues


def load_crosschecks(raw_dir, manual_dir, partial):
    """Independent sources (pipeline/sources/*).

    A source that was not fetched, or whose own consistency checks fail, stops
    the build unless `partial` is set; what was left out is recorded.
    """
    out, status = {}, {}
    for name, module in SOURCES.items():
        if not (Path(raw_dir) / name).exists():
            if not partial:
                raise DataError(f"cross-check source '{name}' not fetched: run pipeline/fetch.py, or pass --partial")
            status[name] = "not fetched"
            print(f"  skipped {name}: not fetched")
            continue
        params = inspect.signature(module.load).parameters
        loaded = module.load(raw_dir, manual_dir) if "manual_dir" in params else module.load(raw_dir)
        problems = {k: loaded.get(k) for k in ("_missing", "_checks") if loaded.get(k)}
        if problems:
            if not partial:
                raise DataError(f"cross-check source '{name}' reports problems: {problems}")
            status[name] = f"problems: {problems}"
        else:
            status[name] = "ok"
        out[name] = loaded
        print(f"  loaded cross-check source: {name}")
    return out, status


IPP_MEASURES = [
    # (key, study prefix in the CSV, measure prefix, label)
    ("taxable", "Bach Bozio Guillouzouic M", "taxable_income_mean_above", "IPP: taxable income"),
    ("dividend_imputed", "Bach Bozio Guillouzouic M", "dividend_imputed_income_mean_above",
     "IPP: retained profits allocated in proportion to dividends (DINA-style)"),
    ("comprehensive", "Bach Bozio Guillouzouic M", "comprehensive_income_mean_above",
     "IPP: retained profits allocated through ownership chains (2025 paper)"),
    ("economic_note92", "IPP Note 92 (", "economic_income_mean_above",
     "IPP: economic income, Note 92 (2023, revised)"),
]
IPP_GROUPS = {"top 1%": ("p99p100", 1), "top 0.1%": ("p99.9p100", 0.1),
              "top 0.01%": ("p99.99p100", 0.01), "top 0.001%": ("p99.999p100", 0.001)}


def build_ipp_comparison(concept, manual_dir, adults, deflator):
    """Top incomes in 2016, in nominal euros: WID pre-tax vs IPP measures.

    Euros, not shares: WID shares are of national income (€1.9tn) while IPP
    shares are of fiscal or comprehensive income of tax households (€1.0–1.2tn),
    so equal shares would not mean equal amounts. WID groups are equal-split
    adults ranked by pre-tax income; IPP groups are tax households (foyers)
    ranked by each IPP measure.
    """
    path = Path(manual_dir) / "ipp_top_income.csv"
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    year = 2016
    i = concept["years"].index(year)
    n_adults = adults[str(year)]
    out = {"year": year, "groups": list(IPP_GROUPS), "unit": f"billion euros, {year} prices",
           "wid_pretax_bn": [], "wid_adults": [], "measures": {}}
    for g, (wid_group, pct_size) in IPP_GROUPS.items():
        people = n_adults * pct_size / 100
        out["wid_adults"].append(round(people))
        out["wid_pretax_bn"].append(round(concept["avg"][wid_group][i] * deflator[str(year)] * people / 1e9, 3))
    for key, prefix, measure, label in IPP_MEASURES:
        sel = [r for r in rows if r["study"].startswith(prefix) and r["measure"].startswith(measure)]
        values, households = [], []
        for g in IPP_GROUPS:
            match = [r for r in sel if r["group"] == g or r["group"].startswith(g + " ")]
            if not match:
                values.append(None); households.append(None); continue
            r = match[0]
            values.append(round(float(r["value"]) * float(r["n_households"]) / 1e9, 3))
            households.append(int(float(r["n_households"])))
        out["measures"][key] = {"label": label, "bn": values, "households": households,
                                "source_url": sel[0]["source_url"] if sel else None}
    return out


def build_vintage_comparison(concept, manual_dir):
    """Top wealth shares for one year from an earlier WID-team estimate
    (Garbinti, Goupille-Lebret & Piketty, WID WP 2016/5, before the Forbes
    calibration) next to the current WID vintage."""
    with open(Path(manual_dir) / "top_wealth_estimates.csv", newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["source"].startswith("Garbinti") and r["unit"].startswith("%")]
    groups = {"bottom 50%": "p0p50", "middle 40%": "p50p90", "top 10%": "p90p100", "top 1%": "p99p100",
              "top 0.1%": "p99.9p100", "top 0.01%": "p99.99p100", "top 0.001%": "p99.999p100"}
    out = []
    for r in rows:
        g = next((k for k in groups if r["group"].startswith(k + " ")), None)
        if g is None:
            continue
        y = int(r["year"])
        current = (concept["share"][groups[g]][concept["years"].index(y)] if groups[g] in concept["share"]
                   else concept["layers"][groups[g]]["share"][concept["years"].index(y)])
        out.append({"year": y, "group": g, "earlier": float(r["share_or_amount"]) / 100,
                    "current": current,
                    "earlier_source": r["source"], "source_url": r["source_url"]})
    rank = list(groups)
    return sorted(out, key=lambda r: rank.index(r["group"]))


def build_purchasing(crosschecks):
    """Consumer prices, pre-committed spending and housing price levels."""
    prices, housing = crosschecks.get("prices"), crosschecks.get("housing")
    if not prices or not housing:
        return None

    def series(d, key, scale=1.0):
        s = d[key]
        return {"years": s["years"], "values": [None if v is None else round(v * scale, 5) for v in s["values"]],
                "unit": s["unit"], "source": s["source"], "url": s.get("url")}

    def mean_of(keys):
        parts = [dict(zip(prices[k]["years"], prices[k]["values"])) for k in keys]
        years = sorted(set.intersection(*(set(p) for p in parts)))
        return {"years": years, "values": [round(sum(p[y] for p in parts) / len(parts), 5) for y in years],
                "unit": "index, 2025=1 (unweighted mean of decile indices)"}

    # CPI from 1990, extended back with INSEE's long coefficient, joined at 1990.
    cpi = dict(zip(prices["cpi_all"]["years"], prices["cpi_all"]["values"]))
    long = dict(zip(prices["cpi_long"]["years"], prices["cpi_long"]["values"]))
    join = min(cpi)
    k = cpi[join] / long[join]
    spliced = {**{y: v * k for y, v in long.items() if y < join}, **cpi}
    deciles = ["lt_d1", "d1_d2", "d2_d3", "d3_d4", "d4_d5", "d5_d6", "d6_d7", "d7_d8", "d8_d9", "gt_d9"]

    # Disposable (cash) income per consumption unit by tenth of persons, ERFS.
    # Published in constant euros of the table's base year; converted to
    # nominal with INSEE's CPI. Where a year appears twice (series break), the
    # newer method is kept.
    erfs = crosschecks["insee"]["erfs_mean_by_decile"]
    base_year = int(re.search(r"(\d{4})", erfs["unit"]).group(1))
    by_year = {}
    for i, col in enumerate(erfs["columns"]):
        by_year[col["year"]] = {d: erfs["data"][f"mean_d{d}"][i] for d in range(1, 11)}
    years = sorted(y for y in by_year if y in spliced)
    def group_mean(ds):
        return [round(sum(by_year[y][d] for d in ds) / len(ds) * spliced[y] / spliced[base_year]) for y in years]
    disposable = {"years": years, "unit": "euros per consumption unit per year, nominal",
                  "source": erfs["source"], "url": erfs.get("url"),
                  "note": f"ERFS mean niveau de vie by tenth (constant {base_year} euros), nominal via INSEE CPI; newer method kept at series breaks.",
                  "bottom50": group_mean(range(1, 6)), "middle40": group_mean(range(6, 10)), "top10": group_mean([10])}
    rate = crosschecks["rates"]["mortgage_rate"]
    check(len(rate["years"]) >= 20 and len(years) >= 20,
          f"too few years for housing: {len(rate['years'])} mortgage rates, {len(years)} ERFS years")
    return {
        "disposable_income": disposable,
        "mortgage_rate": {k: rate[k] for k in ("years", "values", "unit", "source", "url", "series_key")},
        "cpi_all": {"years": sorted(spliced), "values": [round(spliced[y], 5) for y in sorted(spliced)],
                    "unit": "index, 2025=1", "joined_at": join,
                    "note": f"INSEE CPI all households from {join}; earlier years from INSEE's long euro/franc coefficient (two decimals, coarse before ~1950), rescaled to match in {join}."},
        "cpi_bottom50": mean_of([f"cpi_decile_{d}" for d in deciles[:5]]),
        "cpi_middle40": mean_of([f"cpi_decile_{d}" for d in deciles[5:9]]),
        "cpi_top10": mean_of([f"cpi_decile_{d}" for d in deciles[9:]]),
        "precommitted_share": series(prices, "precommitted_share_of_rdb", 0.01),
        "paris_flat_eur_m2": series(housing, "backcast_paris_apartments_eur_m2"),
        "rest_flat_eur_m2": series(housing, "backcast_rest_metro_apartments_eur_m2"),
    }


def build_comparison(concepts, crosschecks):
    """Compact side-by-side series of the same indicator from each source.

    Each indicator maps to a list of series {source, unit, years, values,
    style}; INSEE series are split at its methodological breaks (a None
    between segments) so no line is spliced across a break.
    """
    def wid(code, group):
        c = concepts[code]
        return {"source": "WID (adults, equal split)", "years": c["years"], "values": c["share"][group]}

    out = {k: [] for k in ["wealth_top10", "wealth_top5", "wealth_top1", "wealth_bottom50", "wealth_middle40",
                           "income_top10", "income_bottom50"]}
    out["wealth_top10"].append(wid("hweal", "p90p100"))
    out["wealth_top5"].append(wid("hweal", "p95p100"))
    out["wealth_top1"].append(wid("hweal", "p99p100"))
    out["wealth_bottom50"].append(wid("hweal", "p0p50"))
    out["wealth_middle40"].append(wid("hweal", "p50p90"))
    out["income_top10"].append(wid("diinc", "p90p100"))
    out["income_bottom50"].append(wid("diinc", "p0p50"))

    dwa = crosschecks.get("dwa")
    if dwa:
        for key, group in [("wealth_top10", "top10"), ("wealth_top5", "top5"), ("wealth_bottom50", "bottom50"), ("wealth_middle40", "middle40")]:
            out[key].append({"source": "ECB / Banque de France DWA (households, net wealth)",
                             "years": dwa["years"], "values": dwa["share"][group]})

    insee = crosschecks.get("insee")
    if insee:
        hvp = insee["hvp_inequality"]
        long = insee["hvp_long_series"]
        old = [i for i, col in enumerate(long["columns"]) if "pre2010_method" in col["label"]]
        for key, recent, derived in [("wealth_top10", "gross_top10_share", "top10_share_derived"),
                                     ("wealth_top1", "gross_top1_share", "top1_share_derived"),
                                     ("wealth_bottom50", "gross_bottom50_share_derived", "bottom50_share_derived")]:
            years = [long["columns"][i]["year"] for i in old] + [None] + hvp["years"]
            values = [long["data"][derived][i] for i in old] + [None] + hvp["data"][recent]
            out[key].append({"source": "INSEE wealth survey (households, gross wealth)",
                             "years": years, "values": values, "style": "dots"})
        erfs = insee["erfs_indicators"]
        for key, field, transform in [("income_top10", "S90_share", lambda v: 1 - v),
                                      ("income_bottom50", "S50_share", lambda v: v)]:
            years, values = [], []
            for seg in erfs["segments"]:
                a, b = seg["index"]
                if years:
                    years.append(None); values.append(None)
                for i in range(a, b + 1):
                    v = erfs["data"][field][i]
                    years.append(erfs["columns"][i]["year"])
                    values.append(None if v is None else round(transform(v), 4))
            out[key].append({"source": "INSEE ERFS (persons, disposable income per consumption unit)",
                             "years": years, "values": values})
        cnd = insee["cnd_2019"]["data"]["shares"]["after_transfers"]
        for key, field in [("income_top10", "top10_share_derived"), ("income_bottom50", "bottom50_share_derived")]:
            out[key].append({"source": "INSEE distributed national accounts, incl. public services (2019)",
                             "years": [2019], "values": [cnd[field]], "style": "dots"})
    return out


def file_digest(path):
    """sha256 of a raw file; SDMX headers (send time, message id) are skipped."""
    data = path.read_bytes()
    if path.suffix == ".xml":
        data = re.sub(rb"<message:Header>.*?</message:Header>", b"", data, flags=re.S)
    return hashlib.sha256(data).hexdigest()


def main(raw_dir, out_path, manual_dir=None, partial=False):
    raw = Path(raw_dir)
    manual_dir = Path(manual_dir) if manual_dir else REPO / "data" / "manual"
    for name in ("challenges_500.csv", "forbes_france_billionaires.csv", "ipp_top_income.csv"):
        check((manual_dir / name).exists(), f"{manual_dir / name} is missing (pass the manual folder as 3rd argument)")
    data, quality = load_wid(raw / "WID_data_FR.csv")
    deflator = data[("inyixxi999", "p0p100")]
    price_base = next(y for y, v in sorted(deflator.items()) if abs(v - 1) < 1e-9)
    concepts = {code: build_concept(data, quality, code) for code in CONCEPTS}
    rich_lists = load_rich_lists(manual_dir)
    deflator_out = {str(y): round(v, 5) for y, v in sorted(deflator.items()) if y >= FIRST_YEAR}
    adults_out = {str(y): int(v) for y, v in sorted(data[("npopuli992", "p0p100")].items()) if y >= FIRST_YEAR}
    crosschecks, source_status = load_crosschecks(raw_dir, manual_dir, partial)
    concepts["hweal"]["scenarios"] = build_scenarios(data, concepts["hweal"], rich_lists, deflator_out, adults_out,
                                                     crosschecks.get("dwa"))
    coherence_issues = {code: coherence(data, code, concepts[code]["years"]) for code in CONCEPTS}
    vintage = raw / "wid_vintage.json"
    out = {
        "meta": {
            "country": "France",
            "unit": f"constant {price_base} euros per adult (20+), equal split within couples",
            "price_base_year": price_base,
            "built": datetime.date.today().isoformat(),
            "wid_vintage": json.loads(vintage.read_text(encoding="utf-8")) if vintage.exists() else None,
            "sources_status": source_status,
            "coherence_issues": coherence_issues,
            "inputs_sha256": {
                str(f.relative_to(raw.parent if f.is_relative_to(raw) else manual_dir.parent)): file_digest(f)
                for f in sorted(raw.rglob("*")) + sorted(manual_dir.glob("*.csv"))
                if f.is_file() and f.name != "WID_metadata_FR.csv"
            },
            "layers": [f"p{pct(a)}p{pct(b)}" for a, b in LAYERS],
            "sources": {"wid": "WID.world bulk download, France (WID_data_FR.csv)"},
        },
        "concepts": concepts,
        "composition": build_composition(data),
        "deflator": deflator_out,
        "eur_per_usd": {str(y): round(v, 5) for y, v in sorted(data[("xlcusxi999", "p0p100")].items()) if y >= FIRST_YEAR},
        "rich_lists": rich_lists,
        "comparison": build_comparison(concepts, crosschecks),
        "ipp_top_income": build_ipp_comparison(concepts["ptinc"], manual_dir, adults_out, deflator_out),
        "purchasing": build_purchasing(crosschecks),
        "vintages": build_vintage_comparison(concepts["hweal"], manual_dir),
        "adults": adults_out,
    }
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    # allow_nan=False: a NaN would make the whole JSON unreadable in browsers.
    Path(out_path).write_text(json.dumps(out, separators=(",", ":"), allow_nan=False), encoding="utf-8")
    print(f"wrote {out_path} ({Path(out_path).stat().st_size // 1024} KB), prices in {price_base} euros")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--partial"]
    if len(args) not in (2, 3):
        sys.exit(__doc__)
    main(*args, partial="--partial" in sys.argv[1:])
