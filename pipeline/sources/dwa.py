"""ECB Distributional Wealth Accounts (DWA), France: net wealth by wealth group.

Source
------
ECB / Banque de France "Distributional Wealth Accounts" (DWA), published by the
ECB as experimental statistics since 8 January 2024 (ECB dataflow ``DWA``,
data structure ``ECB_DWA1``) and by the Banque de France on Webstat as
"Comptes distributionnels de patrimoine des menages - series France (DWA1)".
DWA combine the Household Finance and Consumption Survey (HFCS; for France the
INSEE / Banque de France "Histoire de vie et Patrimoine" survey) with the
household-sector balance sheet of the national accounts. The survey top tail is
completed with a press rich list (for France, Challenges according to ECB
WP 2687 Table 1, which refers to the third survey wave; the Banque de France
note does not name the list) and synthetic Pareto households, then every instrument is scaled so the totals
match the national accounts. See docs/notes/dwa.md.

Download
--------
One CSV from the ECB Data Portal SDMX REST API (no key needed)::

    https://data-api.ecb.europa.eu/service/data/DWA/<KEY>?format=csvdata

with KEY (10 dimensions: FREQ.REF_AREA.REF_SECTOR.ACCOUNT_ENTRY.STO.
INSTR_ASSET.DWA_GRP.UNIT_MEASURE.VALUATION.TRANSFORMATION)::

    Q.FR.S14.N+_Z.LE+_Z.NWA.B50+D6+D7+D8+D9+D10+T10+T5+_Z.
      EUR+EUR_R_NH+EUR_R_POP+EUR_MN+EUR_MD+EUR_T+PT+GI.S.N

The series it returns (all quarterly, France, households S14, adjusted net
wealth NWA, standard valuation, non transformed):

    DWA.Q.FR.S14.N.LE.NWA._Z.EUR.S.N        total net wealth, EUR millions
    DWA.Q.FR.S14.N.LE.NWA._Z.EUR_R_NH.S.N   per household, EUR thousands
    DWA.Q.FR.S14.N.LE.NWA._Z.EUR_R_POP.S.N  per capita, EUR thousands
    DWA.Q.FR.S14.N.LE.NWA._Z.EUR_MN.S.N     mean per household, EUR
    DWA.Q.FR.S14.N.LE.NWA._Z.EUR_MD.S.N     median per household, EUR
    DWA.Q.FR.S14.N.LE.NWA.<g>.EUR.S.N       group total, EUR millions,
                                            g in B50, D6, D7, D8, D9, D10
    DWA.Q.FR.S14.N.LE.NWA.<g>.EUR_R_NH.S.N  group mean per household in
                                            the group, EUR thousands
    DWA.Q.FR.S14.N.LE.NWA.<d>.EUR_T.S.N     lower threshold of decile d,
                                            EUR thousands, d in D6..D10
    DWA.Q.FR.S14._Z._Z.NWA.<g>.PT.S.N       share of net wealth, percent,
                                            g in B50, T10, T5
    DWA.Q.FR.S14._Z._Z.NWA._Z.GI.S.N        Gini coefficient, percent

Units are scaled with each series' UNIT_MULT attribute (6 = millions,
3 = thousands, 0 = units), read from the file, never assumed.

Choices
-------
* Unit: the HOUSEHOLD, ranked by household net wealth. Not adults, not equal
  split: the top 10% of households is not the top 10% of adults (WID).
* Annual value = Q4 value. DWA are closing stocks (STO = LE), so Q4 is the
  position on 31 December, the date national balance sheets use. The series
  starts in 2009-Q4, so an annual mean is impossible for 2009 anyway. Years
  without a Q4 observation are dropped; the latest quarter is reported in
  ``latest_quarter``.
* Shares are fractions of total net wealth (0.5445, not 54.45), as in
  site/data/france.json. bottom50, top10, top5 are the published share
  series (PT); D6..D10, middle40 (D6+..+D9) and p90p95 (top10 - top5) are
  derived here from group totals (EUR) or from published shares.
* Households and population are NOT published as such: derived as
  total EUR / per-household EUR and total EUR / per-capita EUR. In the
  vintage ending 2026-Q1 both counts are held constant from 2023-Q3 (the
  reference quarter of the last survey wave); ``load`` reports the quarter
  from which the count stops changing as ``households_constant_from``.
* Money values are NOMINAL euros (current prices, not deflated), as published.
* Decile threshold EUR_T for decile Dk is its LOWER bound (D6 threshold =
  median; D10 threshold = P90).

Standard library only; no import from the rest of the project.
Run:  python3 -I pipeline/sources/dwa.py data/raw
"""

import csv
import json
import os
import sys
import urllib.request

SOURCE = (
    "ECB / Banque de France, Distributional Wealth Accounts (DWA), France, "
    "households (S14), adjusted net wealth (NWA); ECB Data Portal dataflow DWA"
)
API = "https://data-api.ecb.europa.eu/service/data/DWA/"
KEY = (
    "Q.FR.S14.N+_Z.LE+_Z.NWA.B50+D6+D7+D8+D9+D10+T10+T5+_Z."
    "EUR+EUR_R_NH+EUR_R_POP+EUR_MN+EUR_MD+EUR_T+PT+GI.S.N"
)
URL = API + KEY + "?format=csvdata"
FILENAME = "DWA_FR_NWA.csv"
DOC_URLS = [
    "https://www.ecb.europa.eu/press/pr/date/2024/html/ecb.pr240108~ae6f7ef287.en.html",
    "https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp2687~a91d434d45.en.pdf",
    "https://www.banque-france.fr/system/files/2026-09/F26z_note_methodologique_DWA.pdf",
]
USER_AGENT = "Mozilla/5.0 (compatible; show-me-your-pie/0.1; +stdlib urllib)"
DECILES = ["D6", "D7", "D8", "D9", "D10"]


def _path(raw_dir):
    return os.path.join(raw_dir, "dwa", FILENAME)


def fetch(raw_dir: str) -> None:
    """Download the France DWA net-wealth CSV into <raw_dir>/dwa/."""
    out_dir = os.path.join(raw_dir, "dwa")
    os.makedirs(out_dir, exist_ok=True)
    req = urllib.request.Request(
        URL, headers={"User-Agent": USER_AGENT, "Accept": "text/csv"}
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        body = resp.read()
    # The ECB firewall answers some requests with an HTML "access blocked"
    # page; accept only an SDMX CSV whose header starts with KEY.
    if not body.startswith(b"KEY,"):
        raise RuntimeError(
            "ECB API did not return SDMX CSV (first bytes: %r)" % body[:80]
        )
    tmp = _path(raw_dir) + ".part"
    with open(tmp, "wb") as f:
        f.write(body)
    os.replace(tmp, _path(raw_dir))


def _read(raw_dir):
    """Return {(group, unit): {period: value in units}} and UNIT_MULT map."""
    series = {}
    with open(_path(raw_dir), newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("REF_AREA") != "FR" or row.get("INSTR_ASSET") != "NWA":
                continue
            val = row.get("OBS_VALUE", "")
            if val == "":
                continue
            mult = int(row.get("UNIT_MULT") or 0)
            key = (row["DWA_GRP"], row["UNIT_MEASURE"])
            series.setdefault(key, {})[row["TIME_PERIOD"]] = float(val) * 10 ** mult
    if not series:
        raise RuntimeError("no France NWA rows found in " + _path(raw_dir))
    return series


def load(raw_dir: str) -> dict:
    """Parse the downloaded CSV into a JSON-serializable dict (annual = Q4)."""
    s = _read(raw_dir)

    def get(group, unit):
        if (group, unit) not in s:
            raise KeyError("missing DWA series %s.%s" % (group, unit))
        return s[(group, unit)]

    total = get("_Z", "EUR")
    quarters = sorted(total)
    years = sorted(int(q[:4]) for q in quarters if q.endswith("-Q4"))
    q4 = ["%d-Q4" % y for y in years]

    def col(group, unit, scale=1.0, nd=None):
        d = get(group, unit)
        out = []
        for q in q4:
            v = d.get(q)
            v = None if v is None else v * scale
            out.append(v if (v is None or nd is None) else round(v, nd))
        return out

    tot = col("_Z", "EUR")
    share = {
        "bottom50": col("B50", "PT", 0.01, 6),
        "top10": col("T10", "PT", 0.01, 6),
        "top5": col("T5", "PT", 0.01, 6),
    }
    share["p90p95"] = [round(a - b, 6) for a, b in zip(share["top10"], share["top5"])]
    for d in DECILES:
        share[d] = [round(v / t, 6) for v, t in zip(col(d, "EUR"), tot)]
    share["middle40"] = [
        round(sum(share[d][i] for d in DECILES[:4]), 6) for i in range(len(years))
    ]

    households = [round(t / v) for t, v in zip(tot, col("_Z", "EUR_R_NH"))]

    # First quarter from which the derived household count no longer changes
    # (relative tolerance 1e-4, i.e. rounding of the published values).
    nh = get("_Z", "EUR_R_NH")
    hh_q = [total[q] / nh[q] for q in quarters if q in nh]
    frozen_from = None
    for k in range(len(hh_q) - 2, -1, -1):
        if abs(hh_q[k] - hh_q[-1]) > 1e-4 * hh_q[-1]:
            frozen_from = quarters[k + 1] if k + 1 < len(hh_q) - 1 else None
            break
    population = [round(t / v) for t, v in zip(tot, col("_Z", "EUR_R_POP"))]

    avg_per_household = {"all": col("_Z", "EUR_R_NH", nd=0)}
    for g in ["B50"] + DECILES:
        avg_per_household[g] = col(g, "EUR_R_NH", nd=0)
    thresholds = {
        "p50": col("D6", "EUR_T", nd=0),
        "p60": col("D7", "EUR_T", nd=0),
        "p70": col("D8", "EUR_T", nd=0),
        "p80": col("D9", "EUR_T", nd=0),
        "p90": col("D10", "EUR_T", nd=0),
    }

    # Gap between the Q4 value and the four-quarter mean of the top 10% share,
    # to document the cost of the Q4 choice.
    t10 = get("T10", "PT")
    gaps = []
    for y in years:
        qs = ["%d-Q%d" % (y, k) for k in range(1, 5)]
        if all(q in t10 for q in qs):
            mean = sum(t10[q] for q in qs) / 4
            gaps.append((abs(t10["%d-Q4" % y] - mean), y))
    max_gap = max(gaps) if gaps else (None, None)

    return {
        "source": SOURCE,
        "urls": [URL] + DOC_URLS,
        "series_key": "DWA." + KEY,
        "unit": "household (not adult); groups ranked by household net wealth",
        "currency": "EUR, nominal (current prices, not deflated)",
        "frequency_note": (
            "Quarterly source; annual value = Q4 (closing stock at 31 December). "
            "Years without Q4 dropped. Largest |Q4 - four-quarter mean| of the "
            "top 10%% share over complete years: %.2f percentage points (%s)."
            % (max_gap[0], max_gap[1]) if max_gap[0] is not None else
            "Quarterly source; annual value = Q4 (closing stock at 31 December)."
        ),
        "first_quarter": quarters[0],
        "latest_quarter": quarters[-1],
        "years": years,
        "share": share,
        "share_note": (
            "Fractions of total net wealth. bottom50, top10, top5 = published "
            "PT series; D6..D10 = group EUR / total EUR; middle40 = D6+..+D9; "
            "p90p95 = top10 - top5 (all derived)."
        ),
        "total_net_wealth_eur": [round(v) for v in tot],
        "households": households,
        "households_constant_from": frozen_from,
        "population": population,
        "mean_net_wealth_per_household_eur": col("_Z", "EUR_MN", nd=0),
        "median_net_wealth_per_household_eur": col("_Z", "EUR_MD", nd=0),
        "avg_per_household_eur": avg_per_household,
        "thresholds_eur": thresholds,
        "gini": col("_Z", "GI", 0.01, 4),
        "notes": (
            "Households and population are derived (total / per-household and "
            "total / per-capita); see households_constant_from for the quarter "
            "from which the count is frozen (2023-Q3, the last HFCS wave, in "
            "the vintage ending 2026-Q1). Survey anchors for France (Banque de "
            "France note, 2026-09): 2009-Q4, 2014-Q4, 2017-Q4, 2021-Q1, 2023-Q3; "
            "other quarters are inter/extrapolated per decile and calibrated to "
            "quarterly national accounts. Wealth concept excludes most pension "
            "entitlements, durables, valuables and currency (about 90% of the "
            "household balance sheet, Banque de France). Experimental ECB "
            "statistics; post-2023 quarters will be revised with the next wave."
        ),
    }


def main(argv):
    if len(argv) != 2:
        print("usage: python3 -I pipeline/sources/dwa.py <raw_dir>", file=sys.stderr)
        return 2
    raw_dir = argv[1]
    fetch(raw_dir)
    d = load(raw_dir)
    print("DWA France: %s .. %s, %d annual points (Q4)" % (
        d["first_quarter"], d["latest_quarter"], len(d["years"])))
    print("year  top10  top5   p90-95 bottom50 total_bn  households  median")
    for i, y in enumerate(d["years"]):
        print("%d  %.4f %.4f %.4f %.4f   %8.0f  %10d  %7.0f" % (
            y, d["share"]["top10"][i], d["share"]["top5"][i],
            d["share"]["p90p95"][i], d["share"]["bottom50"][i],
            d["total_net_wealth_eur"][i] / 1e9, d["households"][i],
            d["median_net_wealth_per_household_eur"][i]))
    print(d["frequency_note"])
    print("Household count constant from:", d["households_constant_from"])
    json.dumps(d)  # assert serializable
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
