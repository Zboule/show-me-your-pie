"""Every number quoted in paper/paper.md, computed from the built dataset.

    python3 -I pipeline/paper_numbers.py site/data/france.json paper/numbers.json

Writes the numbers as JSON and as a Markdown table (paper/numbers.md). The
test suite checks that each formatted value appears in the paper, so the text
cannot drift from the data.
"""
import json
import math
import sys
from pathlib import Path


def pct(x, digits=1):
    return f"{x * 100:.{digits}f}%"


def main(data_path, out_path):
    D = json.loads(Path(data_path).read_text(encoding="utf-8"))
    C, adults = D["concepts"], D["adults"]
    width = lambda L: (L["bounds"][1] - L["bounds"][0]) / 100

    def share(code, key, y):
        c = C[code]
        return c["layers"][key]["share"][c["years"].index(y)]

    def avg(code, key, y):
        c = C[code]
        return c["layers"][key]["avg"][c["years"].index(y)]

    def total(code, y):
        c = C[code]
        i = c["years"].index(y)
        return sum(L["avg"][i] * width(L) for L in c["layers"].values()) * adults[str(y)]

    N = {}
    w = "hweal"
    E, B = C[w]["years"][-1], 1990
    for y in (1900, 1950, 1980, 1990, 2014, E):
        N[f"wealth_top0001_{y}"] = pct(share(w, "p99.999p100", y), 2 if share(w, "p99.999p100", y) < 0.01 else 1)
        N[f"wealth_bottom50_{y}"] = pct(share(w, "p0p50", y))
    N["wealth_top1_1900"] = pct(sum(share(w, k, 1900) for k in ("p99p99.9", "p99.9p99.99", "p99.99p99.999", "p99.999p100")))
    N["wealth_top1_1980"] = pct(sum(share(w, k, 1980) for k in ("p99p99.9", "p99.9p99.99", "p99.99p99.999", "p99.999p100")))
    N[f"wealth_top1_{E}"] = pct(sum(share(w, k, E) for k in ("p99p99.9", "p99.9p99.99", "p99.99p99.999", "p99.999p100")))
    N["bottom50_avg_1990"] = f"€{round(avg(w, 'p0p50', B), -2):,.0f}"
    N[f"bottom50_avg_{E}"] = f"€{round(avg(w, 'p0p50', E), -2):,.0f}"
    dT = total(w, E) - total(w, B)
    N["wealth_rise_tn"] = f"€{dT / 1e12:.1f} tn"
    for key, name in (("p99.999p100", "top0001"), ("p0p50", "bottom50")):
        net = share(w, key, E) * total(w, E) - share(w, key, B) * total(w, B)
        N[f"captured_{name}"] = pct(net / dT)
    s0 = share(w, "p0p50", B)
    N["bottom50_net_bn"] = f"€{(share(w, 'p0p50', E) * total(w, E) - s0 * total(w, B)) / 1e9:.0f} bn"
    N["bottom50_at_start_share_bn"] = f"€{s0 * dT / 1e9:.0f} bn"
    N["adults_top0001"] = f"{round(adults[str(E)] * 1e-5, -1):.0f}"

    sc = C[w]["scenarios"]
    def scen(name):
        ys = sc["years"][name]
        return sc["layers"][name]["p99.999p100"][ys.index(E)]
    for name in sc["layers"]:
        N[f"scenario_{name}"] = pct(scen(name))
    N["scenario_years_ggp_low"] = str(len(sc["corrected_years"]["ggp_low"]))
    N["scenario_years_no_cut"] = str(len(sc["corrected_years"]["no_cut"]))
    tb = sc["topbin_check"][-1]
    N["topbin_threshold_m"] = f"€{tb['threshold'] / 1e6:.0f} M"
    N["topbin_projected_m"] = f"€{tb['projected'] / 1e6:.0f} M"
    N["topbin_ratio"] = f"{tb['threshold'] / tb['projected']:.1f}"

    v = next(r for r in D["vintages"] if r["group"] == "top 0.001%")
    N["vintage_earlier"] = pct(v["earlier"])
    N["vintage_current"] = pct(v["current"])
    for g, key in (("bottom 50%", "bottom50"), ("middle 40%", "middle40")):
        v = next(r for r in D["vintages"] if r["group"] == g)
        N[f"vintage_{key}_earlier"] = pct(v["earlier"])
        N[f"vintage_{key}_current"] = pct(v["current"])

    # Poorest share of adults holding as much as the top 0.001% (end year).
    c = C[w]
    i = c["years"].index(E)
    bins = []
    for j, b in enumerate(c["gp"]["bins"]):
        lo, hi = (float(x) for x in b[1:].split("p"))
        bins.append((lo, hi, c["gp"]["avg"][j][i] * (hi - lo)))
    tot = sum(m for *_, m in bins)
    target, cum = share(w, "p99.999p100", E), 0.0
    for lo, hi, m in bins:
        if m > 0 and (cum + m) / tot >= target:
            N["poorest_equivalent"] = pct((lo + (target * tot - cum) / m * (hi - lo)) / 100)
            break
        cum += m

    N[f"pretax_bottom50_{E}"] = pct(share("ptinc", "p0p50", E))
    N[f"posttax_bottom50_{E}"] = pct(share("diinc", "p0p50", E))
    N[f"pretax_top0001_{E}"] = pct(share("ptinc", "p99.999p100", E), 2)

    def gap(key, a, b, lo=0, hi=9999):
        A = next(s for s in D["comparison"][key] if s["source"].startswith(a))
        Bs = next(s for s in D["comparison"][key] if s["source"].startswith(b))
        d = []
        for y, val in zip(Bs["years"], Bs["values"]):
            if y is None or val is None or not lo <= y <= hi or y not in A["years"]:
                continue
            x = A["values"][A["years"].index(y)]
            if x is not None:
                d.append(x - val)
        return min(d), max(d)
    g = gap("wealth_top5", "WID", "ECB")
    N["dwa_top5_gap"] = f"{g[0] * 100:.1f}–{g[1] * 100:.1f}"
    g = gap("wealth_bottom50", "WID", "ECB")
    N["dwa_bottom50_gap"] = f"{g[0] * 100:.1f} to +{g[1] * 100:.1f}"

    t = D["ipp_top_income"]
    m = t["measures"]
    for k, g in enumerate(t["groups"]):
        N[f"ipp_ratio_{g.replace(' ', '_')}"] = f"{m['comprehensive']['bn'][k] / t['wid_pretax_bn'][k]:.{1 if k > 1 else 2}f}"
    N["ipp_wid_top0001_bn"] = f"{t['wid_pretax_bn'][-1]:.1f}"
    N["ipp_div_top0001_bn"] = f"{m['dividend_imputed']['bn'][-1]:.1f}"

    P = D["purchasing"]
    inc, rate = P["disposable_income"], dict(zip(P["mortgage_rate"]["years"], P["mortgage_rate"]["values"]))
    for region, key in (("paris", "paris_flat_eur_m2"), ("rest", "rest_flat_eur_m2")):
        pr = dict(zip(P[key]["years"], P[key]["values"]))
        for y in (inc["years"][0], inc["years"][-1]):
            cost = 70 * pr[y]
            income = inc["bottom50"][inc["years"].index(y)]
            N[f"years_{region}_{y}"] = f"{cost / income:.0f}"
            if y in rate:
                r = rate[y]
                N[f"repay_{region}_{y}"] = pct(cost * r / (1 - (1 + r) ** -25) / income, 0)
        y = 2000
        cost = 70 * pr[y]
        r = rate[y]
        N[f"repay_{region}_{y}"] = pct(cost * r / (1 - (1 + r) ** -25) / inc["bottom50"][inc["years"].index(y)], 0)

    # Figures previously typed by hand in the paper.
    worst = max(abs(s_ - p_) for cc in C.values() for L in cc["layers"].values()
                for s_, p_ in zip(L["share"], L["share_published"]) if s_ is not None and p_ is not None)
    N["slices_vs_published_max"] = f"{math.ceil(worst * 1e5) / 1e5:.5f}"
    pc = P["precommitted_share"]
    N["precommitted_first"] = pct(pc["values"][0])
    N["precommitted_last"] = pct(pc["values"][-1])
    N["precommitted_first_year"] = str(pc["years"][0])
    N["precommitted_last_year"] = str(pc["years"][-1])
    cnd = next(s for s in D["comparison"]["income_bottom50"] if "distributed" in s["source"])
    N["cnd_bottom50_2019"] = pct(cnd["values"][0], 0)
    cpi = dict(zip(P["cpi_all"]["years"], P["cpi_all"]["values"]))
    # Real growth of mean wealth per adult 1980 → end year, WID prices vs CPI.
    mean = lambda y: total(w, y) / adults[str(y)]
    g_wid = mean(E) / mean(1980) - 1
    f = lambda y: D["deflator"][str(max(y, 1950))] / cpi[max(y, 1950)]
    g_cpi = mean(E) * f(E) / (mean(1980) * f(1980)) - 1
    N["growth_wealth_1980_wid"] = pct(g_wid, 0)
    N["growth_wealth_1980_cpi"] = pct(g_cpi, 0)
    gb, gt = P["cpi_bottom50"], P["cpi_top10"]
    N["cpi_decile_gap_pts"] = f"{((gb['values'][-1] / gb['values'][0]) - (gt['values'][-1] / gt['values'][0])) * 100:.1f}"
    def fell_range(key):
        c = C[w]; ys = c["years"]; e = c["layers"][key]["share"][ys.index(E)]
        fell = [y for y in ys if y < E and c["layers"][key]["share"][ys.index(y)] > e]
        # Longest run of consecutive start years (in the series) where the share fell.
        runs, cur = [], []
        for y in ys:
            if y >= E:
                break
            if y in fell:
                cur.append(y)
            else:
                if cur: runs.append(cur)
                cur = []
        if cur: runs.append(cur)
        best = max(runs, key=len)
        return best[0], best[-1]
    a, b = fell_range("p0p50"); N["start_fell_bottom50"] = f"between {a} and {b}"
    a, b = fell_range("p50p90"); N["start_fell_middle40"] = f"between {a} and {b}"
    def fell_runs(key):
        c = C[w]; ys = c["years"]; e = c["layers"][key]["share"][ys.index(E)]
        runs, cur = [], []
        for y in [y for y in ys if 1950 <= y < E]:
            if c["layers"][key]["share"][ys.index(y)] > e:
                cur.append(y)
            elif cur:
                runs.append(cur); cur = []
        if cur: runs.append(cur)
        return "; ".join(f"{r[0]}–{r[-1]}" if len(r) > 1 else str(r[0]) for r in runs)
    N["start_fell_middle40_runs"] = fell_runs("p50p90")
    L = C[w]["layers"]["p99.999p100"]["share"]; i = C[w]["years"].index(E)
    N["smooth_top0001_raw"] = pct(L[i], 2)
    N["smooth_top0001_two_year"] = pct((L[i] + L[i - 1]) / 2, 2)

    # ---- Round-2 referee: ranges instead of points for the very top ----
    fb = D["rich_lists"]["forbes_france_billionaires"][str(E)]
    forbes_real = float(fb["total_eur_bn"]) * 1e9 / D["deflator"][str(E)]
    N["forbes_billionaires_n"] = fb["n_billionaires"]
    N["forbes_floor"] = pct(forbes_real / total(w, E))
    pub = ["dwa_lower", "ggp_low"]
    tops = [scen(n) for n in pub] + [share(w, "p99.999p100", E), forbes_real / total(w, E)]
    N["top0001_range_low"] = pct(min(tops))
    N["top0001_range_high"] = pct(max(tops))
    # Poorest share holding as much as the top 0.001%, under each scenario:
    # scenarios rescale the bottom of the distribution uniformly, so the
    # cumulative curve is WID's times bottom50_scenario / bottom50_WID.
    def poorest(target_share):
        cum = 0.0
        for lo, hi, m in bins:
            if m > 0 and (cum + m) / tot >= target_share:
                return (lo + (target_share * tot - cum) / m * (hi - lo)) / 100
            cum += m
        return 1.0
    eqs = [poorest(share(w, "p99.999p100", E))]
    for n in pub:
        ys = sc["years"][n]
        b50 = sc["layers"][n]["p0p50"][ys.index(E)]
        eqs.append(poorest(scen(n) * share(w, "p0p50", E) / b50))
    N["poorest_equivalent_low"] = pct(min(eqs))
    N["poorest_equivalent_high"] = pct(max(eqs))
    caps = []
    for n in pub:
        ys = sc["years"][n]
        s_end = sc["layers"][n]["p99.999p100"][ys.index(E)]
        caps.append((s_end * total(w, E) - share(w, "p99.999p100", B) * total(w, B)) / dT)
    caps.append((share(w, "p99.999p100", E) * total(w, E) - share(w, "p99.999p100", B) * total(w, B)) / dT)
    caps.append((forbes_real - share(w, "p99.999p100", B) * total(w, B)) / dT)  # Forbes floor
    N["captured_top0001_low"] = pct(min(caps))
    N["captured_top0001_high"] = pct(max(caps))
    g = gap("wealth_top5", "WID", "ECB")
    g = gap("wealth_middle40", "ECB", "WID")
    N["dwa_middle40_gap"] = f"{g[0] * 100:.1f}–{g[1] * 100:.1f}"
    E18 = 2018
    N["pretax_bottom50_2018"] = pct(share("ptinc", "p0p50", E18))
    N["posttax_bottom50_2018"] = pct(share("diinc", "p0p50", E18))
    N["posttax_bottom50_2019"] = pct(share("diinc", "p0p50", 2019))
    for y in (1950, 1990, 2014):
        N[f"wealth_top1_{y}"] = pct(sum(share(w, k, y) for k in ("p99p99.9", "p99.9p99.99", "p99.99p99.999", "p99.999p100")))
    ys = C[w]["years"]; L50 = C[w]["layers"]["p0p50"]["share"]; e50 = L50[ys.index(E)]
    rose = [y for y in ys if 1950 <= y < E and L50[ys.index(y)] < e50]
    N["start_rose_bottom50_after_1950"] = ", ".join(str(y) for y in rose[-4:])
    pr = dict(zip(P["paris_flat_eur_m2"]["years"], P["paris_flat_eur_m2"]["values"]))
    best = max(((pr[y] * 70 * rate[y] / (1 - (1 + rate[y]) ** -25) / inc["bottom50"][inc["years"].index(y)], y)
                for y in inc["years"] if y in rate and y in pr))
    N["repay_paris_peak"] = pct(best[0], 0)
    N["repay_paris_peak_year"] = str(best[1])

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(N, indent=1, ensure_ascii=False), encoding="utf-8")
    rows = "\n".join(f"| `{k}` | {v} |" for k, v in N.items())
    out.with_suffix(".md").write_text(
        "# Numbers quoted in the paper\n\nGenerated by `pipeline/paper_numbers.py` from `site/data/france.json`. "
        "Do not edit by hand.\n\n| Key | Value |\n|---|---|\n" + rows + "\n", encoding="utf-8")
    print(f"wrote {len(N)} numbers to {out}")


if __name__ == "__main__":
    main(*sys.argv[1:])
