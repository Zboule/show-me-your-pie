"""Consumer prices by household category and pre-committed spending (France).

    python3 -I pipeline/sources/prices.py <raw_dir>      # fetch + load + summary

Standalone: standard library only, imports no project module.
`fetch(raw_dir)` downloads into <raw_dir>/prices/; `load(raw_dir)` parses those
files (plus the hand-compiled CSVs in <raw_dir>/../manual/) into a
JSON-serialisable dict: {key: {"source", "url", "unit", "years", "values",
"notes", ...}}. Time series have values aligned with years; entries with a "shape" key
are not: "by_group" (values = {group: ...}), "by_item" ({item: ...}) or "rows" (list of dicts).

Series (titles are INSEE's own TITLE_FR, re-read from the downloaded file)
---------------------------------------------------------------------------
INSEE BDM, annual consumer price indices (SDMX: bdm.insee.fr/series/sdmx/data/SERIES_BDM/<idbank>)

All households
  011814639  Indice annuel des prix à la consommation - Base 2025 - Ensemble des ménages - France
             - Nomenclature Coicop : 00 - Ensemble                          1996-, 2025=100
  011814653  ... Base 2025 - Ensemble des ménages y compris loyers imputés - France - Coicop 00 - Ensemble
                                                                            1996-, 2025=100
  001764363  ... Base 2015 - Ensemble des ménages - France - Ensemble - Séries arrêtées
                                                                            1990-2025, 2015=100
  001765178  ... Base 2015 - Ensemble des ménages - France métropolitaine - Ensemble - Séries arrêtées
                                                                            1990-2025, 2015=100
  001765177  ... Base 2015 - Ensemble des ménages - France - Ensemble y compris loyers fictifs - Séries arrêtées
                                                                            1990-2025, 2015=100
  011813530  Coefficient de transformation de l'euro ou du franc d'une année, en euro ou en franc
             d'une autre année - Base 2025                                  1901-, 2025=100 (2 decimals:
             coarse before ~1950)
  011814655  ... Base 2025 - Ménages urbains dont le chef est ouvrier ou employé - France - Coicop 00
                                                                            1996-, 2025=100

By decile of niveau de vie (France métropolitaine; same prices, decile-specific weights)
  Base 2015 (Séries arrêtées, 1998-2025, 2015=100):
  010054292  Inférieur au 1er décile        010054297  Entre le 5ème et le 6ème décile
  010054293  Entre le 1er et 2ème décile    010054298  Entre le 6ème et le 7ème décile
  010054294  Entre le 2ème et le 3ème décile 010054299 Entre le 7ème et le 8ème décile
  010054295  Entre le 3ème et le 4ème décile 010054300 Entre le 8ème et le 9ème décile
  010054296  Entre le 4ème et le 5ème décile 010054301 Supérieur au 9ème décile
  Base 2025 (2010-, 2025=100): 011818277 (<D1), 011818278 ... 011818285 (D1-D2 ... D8-D9),
  011818286 (>D9). Title pattern: "Indice annuel des prix à la consommation - Base 2025 -
  Niveau de vie du ménage - <tranche> - France métropolitaine".
  First quintile, *hors tabac*, France: 001766925 (base 2015, 1998-2025),
  011818265 (base 2025, 2015-). Title: "... Ménages du premier quintile de la distribution
  des niveaux de vie - France - Ensemble hors tabac".
By housing tenure / retired (France métropolitaine, base 2015, 1998-2025):
  010054308 Propriétaire, 010054309 Accédant à la propriété, 010054310 Locataire,
  010054291 Retraité.

INSEE does NOT publish a CPI by *quintile* of niveau de vie except the first quintile
(hors tabac); it does publish one by *decile* (above). Built series:
  cpi_decile_<g>   base-2015 decile series rebased to 2025=1 (1998-2025); checked against
                   the base-2025 series over 2010-2025 (ratios identical up to rounding).
  cpi_all          011814639 / 100 (1996-), extended back to 1990 with 001764363 rebased.

Pre-committed spending, national accounts
  INSEE comptes nationaux annuels base 2020, table 2.103 "Dépense de consommation finale
  pré-engagée des ménages à prix courants", 1959-2025 (file of the May-2026 edition,
  https://www.insee.fr/fr/statistiques/8988851 -> fichier/8988851/t_2103_fr.xlsx; the page id
  changes each edition). Rows used: CPDPE, P3, B6G (bn EUR) and the shares _DEP_REVENU
  ("Part de la dépense pré-engagée dans le revenu disponible brut"), _DEP_CONSO,
  _DEP_LOGT_REVENU, _ASSUR_REVENU, _TELE_REVENU, _CANTINE_REVENU (%).
  Cross-check, base 2014 (BDM, Séries arrêtées, 1959-2021):
  010562201 "Comptes nationaux annuels base 2014 - Revenu disponible brut - Ménages y compris EI
             - Ressources ou passifs - Prix courant"
  010562212 "... Revenu disponible brut arbitrable - Ménages y compris E.I. - ... - Prix courant"
  share = 1 - arbitrable / RDB.
  National-accounts definition (INSEE c1358): housing incl. imputed rents, water, energy,
  telecoms, TV, canteens, insurance (excl. life) and financial services incl. FISIM; mortgage
  repayments are NOT included.

Pre-committed spending by income group
  INSEE Première n°1815 (Accardo & Billot, Sept. 2020), data file ip1815.xlsx: 2017, by
  quintile of RDB/UC (national-accounts distribution): Figure 7 share of pre-committed spending
  in consumption *excluding imputed rents*; Figure 6 RDB/UC and consumption/UC; Figure 5
  savings rate 2011-2017.
  Manual: data/manual/precommitted_spending_surveys.csv (DREES ER 1055 / Budget de famille
  2011, % of disposable income; France Stratégie NA 102 / Budget de famille 2001-2017, % of
  total expenditure; deciles of niveau de vie vs arbitrable income per UC, 2017). These
  include mortgage repayments; groups are poor / modest / middle / affluent, not quintiles.

Spatial price levels
  INSEE Première n°1959 (July 2023), donnees_insee_premiere_n1959.xlsx: Fisher price gap,
  Paris urban unit vs province excl. Corsica, 2022 (Tableau complémentaire 1).
  Manual: data/manual/insee_spatial_price_gap.csv (2015 edition, Insee Première n°1590, which
  publishes only an .xls/.pdf).
"""
import csv
import json
import os
import re
import sys
import urllib.request
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

BDM = "https://bdm.insee.fr/series/sdmx/data/SERIES_BDM/"
UA = {"User-Agent": "show-me-your-pie/0.1 (open data research)"}

DECILES = ["lt_d1", "d1_d2", "d2_d3", "d3_d4", "d4_d5", "d5_d6", "d6_d7", "d7_d8", "d8_d9", "gt_d9"]
CPI_SERIES = {
    "cpi_all_b2025": "011814639",
    "cpi_all_incl_imputed_rents_b2025": "011814653",
    "cpi_all_b2015": "001764363",
    "cpi_all_metro_b2015": "001765178",
    "cpi_all_incl_imputed_rents_b2015": "001765177",
    "cpi_long_coefficient_b2025": "011813530",
    "cpi_urban_workers_b2025": "011814655",
    "cpi_q1_excl_tobacco_b2015": "001766925",
    "cpi_q1_excl_tobacco_b2025": "011818265",
    "cpi_owner_b2015": "010054308",
    "cpi_owner_with_mortgage_b2015": "010054309",
    "cpi_tenant_b2015": "010054310",
    "cpi_retired_b2015": "010054291",
}
CPI_SERIES.update({f"cpi_decile_{g}_b2015": f"{10054292 + i:09d}" for i, g in enumerate(DECILES)})
CPI_SERIES.update({f"cpi_decile_{g}_b2025": f"{11818277 + i:09d}" for i, g in enumerate(DECILES)})
CNA2014 = {"rdb_b2014": "010562201", "rdb_arbitrable_b2014": "010562212"}

T2103_PAGE = "https://www.insee.fr/fr/statistiques/8988851"
T2103 = "https://www.insee.fr/fr/statistiques/fichier/8988851/t_2103_fr.xlsx"
IP1815_PAGE = "https://www.insee.fr/fr/statistiques/4764600"
IP1815 = "https://www.insee.fr/fr/statistiques/fichier/4764600/ip1815.xlsx"
IP1959_PAGE = "https://www.insee.fr/fr/statistiques/7649921"
IP1959 = "https://www.insee.fr/fr/statistiques/fichier/7649921/donnees_insee_premiere_n1959.xlsx"

FILES = {
    "insee_cpi_annual.xml": BDM + "+".join(CPI_SERIES.values()),
    "insee_cna2014_rdb.xml": BDM + "+".join(CNA2014.values()),
    "insee_t_2103.xlsx": T2103,
    "insee_ip1815.xlsx": IP1815,
    "insee_ip1959.xlsx": IP1959,
}


# ---------------------------------------------------------------- download
def _get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
        return r.read()


def fetch(raw_dir):
    out = Path(raw_dir) / "prices"
    out.mkdir(parents=True, exist_ok=True)
    for name, url in FILES.items():
        data = _get(url)
        if name.endswith(".xml") and b"<Series" not in data:
            raise RuntimeError(f"{url}: no series in response: {data[:300]!r}")
        if name.endswith(".xlsx") and not data.startswith(b"PK"):
            raise RuntimeError(f"{url}: not an xlsx file")
        part = out / (name + ".part")
        part.write_bytes(data)
        os.replace(part, out / name)
        print("wrote", out / name, f"({len(data):,} bytes)")


# ---------------------------------------------------------------- parsers
def parse_bdm(path):
    """SDMX StructureSpecificData -> {idbank: {"title", "attrs", "obs": {period: float}}}."""
    text = Path(path).read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"<Series ([^>]*?)>(.*?)</Series>", text, re.S):
        attrs = dict(re.findall(r'([A-Z_][A-Z_0-9\-]*)="([^"]*)"', m.group(1)))
        obs = {}
        for o in re.finditer(r"<Obs ([^>]*?)/>", m.group(2)):
            a = dict(re.findall(r'([A-Z_]+)="([^"]*)"', o.group(1)))
            v = a.get("OBS_VALUE", "")
            if v not in ("", "NaN"):
                obs[a["TIME_PERIOD"]] = float(v)
        out[attrs["IDBANK"]] = {"title": attrs.get("TITLE_FR", "").strip(), "attrs": attrs, "obs": obs}
    return out


def _loc(tag):
    return tag.rsplit("}", 1)[-1]


def _text(el):
    return "".join(t.text or "" for t in el.iter() if _loc(t.tag) == "t")


def read_xlsx(path):
    """Minimal xlsx reader (any OOXML namespace): [(sheet_name, [[cell, ...], ...]), ...]."""
    z = zipfile.ZipFile(path)
    names = z.namelist()
    shared = []
    if "xl/sharedStrings.xml" in names:
        shared = [_text(si) for si in ET.fromstring(z.read("xl/sharedStrings.xml")) if _loc(si.tag) == "si"]
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    target = {r.get("Id"): r.get("Target") for r in rels}
    sheets = []
    for s in wb.iter():
        if _loc(s.tag) != "sheet":
            continue
        rid = next(v for k, v in s.attrib.items() if _loc(k) == "id")
        t = target[rid].lstrip("/")
        part = t if t.startswith("xl/") else "xl/" + t
        rows = []
        for r in ET.fromstring(z.read(part)).iter():
            if _loc(r.tag) != "row":
                continue
            row = {}
            for c in r:
                if _loc(c.tag) != "c":
                    continue
                col = re.match(r"[A-Z]+", c.get("r")).group()
                idx = 0
                for ch in col:
                    idx = idx * 26 + ord(ch) - 64
                v = [x for x in c if _loc(x.tag) == "v"]
                inline = [x for x in c if _loc(x.tag) == "is"]
                if v:
                    val = v[0].text
                    if c.get("t") == "s":
                        val = shared[int(val)]
                elif inline:
                    val = _text(inline[0])
                else:
                    continue
                row[idx - 1] = val
            rows.append([row.get(i) for i in range(max(row) + 1)] if row else [])
        sheets.append((s.get("name"), rows))
    return sheets


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _series(source, url, unit, values, notes, **extra):
    years = sorted(values)
    d = {"source": source, "url": url, "unit": unit, "years": years,
         "values": [values[y] for y in years], "notes": notes}
    d.update(extra)
    return d


def _annual(obs):
    return {int(p): v for p, v in obs.items() if re.fullmatch(r"\d{4}", p)}


# ---------------------------------------------------------------- loaders
def _load_cpi(raw):
    bdm = parse_bdm(raw / "insee_cpi_annual.xml")
    out = {}
    for key, idb in CPI_SERIES.items():
        s = bdm[idb]
        base = re.search(r"Base (\d{4})", s["title"])
        out[key] = _series(
            "INSEE BDM idbank " + idb, BDM + idb,
            f"index, {base.group(1)}=100" if base else "index", _annual(s["obs"]),
            s["title"], idbank=idb, title=s["title"], last_update=s["attrs"].get("LAST_UPDATE"))

    def rebased(key):
        v = dict(zip(out[key]["years"], out[key]["values"]))
        return {y: x / v[2025] for y, x in v.items()}

    # chained all-household CPI, 2025 = 1
    b25 = {y: v / 100 for y, v in zip(out["cpi_all_b2025"]["years"], out["cpi_all_b2025"]["values"])}
    b15 = rebased("cpi_all_b2015")
    for y in set(b25) & set(b15):
        if not (abs(b25[y] / b15[y] - 1) < 0.003):
            raise ValueError(("CPI base 2015 vs 2025 mismatch", y))
    chained = dict(b15)
    chained.update(b25)
    out["cpi_all"] = _series(
        "INSEE BDM 011814639 (1996-), 001764363 rebased to 2025=1 (1990-1995)",
        BDM + "011814639", "index, 2025=1", chained,
        "All households, France. Annual average CPI. Base-2015 and base-2025 series agree to "
        "<0.3% over their overlap, so the splice is a plain rebase.")
    for key in ("cpi_all_incl_imputed_rents", ):
        v = rebased(key + "_b2015")
        v.update({y: x / 100 for y, x in zip(out[key + "_b2025"]["years"], out[key + "_b2025"]["values"])})
        out[key] = _series("INSEE BDM 011814653 (1996-), 001765177 rebased (1990-1995)", BDM + "011814653",
                           "index, 2025=1", v, "All households incl. imputed rents, France.")
    lc = out["cpi_long_coefficient_b2025"]
    out["cpi_long"] = _series(
        "INSEE BDM idbank 011813530", BDM + "011813530", "index, 2025=1",
        {y: v / 100 for y, v in zip(lc["years"], lc["values"])},
        "INSEE euro/franc purchasing-power coefficient (consumer prices), 1901-. Published with two "
        "decimals on a 2025=100 scale, so values before ~1950 are very coarse (e.g. 0.03).")

    # deciles: base 2015 rebased to 2025 = 1, checked against base 2025
    for g in DECILES:
        v15 = rebased(f"cpi_decile_{g}_b2015")
        k25 = out[f"cpi_decile_{g}_b2025"]
        v25 = {y: x / 100 for y, x in zip(k25["years"], k25["values"])}
        worst = max(abs(v15[y] / v25[y] - 1) for y in set(v15) & set(v25))
        if not (worst < 0.002):
            raise ValueError(("decile base mismatch", g, worst))
        out[f"cpi_decile_{g}"] = _series(
            f"INSEE BDM {CPI_SERIES[f'cpi_decile_{g}_b2015']} rebased to 2025=1",
            BDM + CPI_SERIES[f"cpi_decile_{g}_b2015"], "index, 2025=1", v15,
            f"Households of decile group {g} of niveau de vie, France métropolitaine. Max gap vs "
            f"base-2025 series {CPI_SERIES[f'cpi_decile_{g}_b2025']} over 2010-2025: {worst:.4%}.")
    return out


def _load_precommitted_macro(raw):
    def is_header(r):
        return sum(1 for c in r if c and re.fullmatch(r"\d{4}", str(c))) > 20

    rows = next(rows for _, rows in read_xlsx(raw / "insee_t_2103.xlsx") if any(is_header(r) for r in rows))
    hdr = next(r for r in rows if is_header(r))
    years = {i: int(c) for i, c in enumerate(hdr) if c and re.fullmatch(r"\d{4}", str(c))}
    title = rows[0][0].strip()
    wanted = {
        "_DEP_REVENU": ("precommitted_share_of_rdb", "% of household gross disposable income"),
        "_DEP_CONSO": ("precommitted_share_of_consumption", "% of household final consumption"),
        "_DEP_LOGT_REVENU": ("precommitted_housing_share_of_rdb", "% of household gross disposable income"),
        "_ASSUR_REVENU": ("precommitted_insurance_finance_share_of_rdb", "% of household gross disposable income"),
        "_TELE_REVENU": ("precommitted_tv_telecom_share_of_rdb", "% of household gross disposable income"),
        "_CANTINE_REVENU": ("precommitted_canteen_share_of_rdb", "% of household gross disposable income"),
        "CPDPE": ("precommitted_consumption_eur_bn", "bn EUR, current prices"),
        "P3": ("household_consumption_eur_bn", "bn EUR, current prices"),
        "B6G": ("household_rdb_eur_bn", "bn EUR, current prices"),
    }
    out = {}
    for r in rows:
        if r and r[0] in wanted:
            key, unit = wanted[r[0]]
            label = r[1] if len(r) > 1 else r[0]
            vals = {y: _num(r[i]) for i, y in years.items() if i < len(r) and _num(r[i]) is not None}
            out[key] = _series(
                f"INSEE comptes nationaux annuels base 2020, {title}", T2103, unit, vals,
                f"Row {r[0]} '{label}'. Households (S14), France. National-accounts definition "
                "(INSEE c1358): includes imputed rents, excludes mortgage repayments. Page: " + T2103_PAGE)
    s = out["precommitted_share_of_rdb"]
    v = dict(zip(s["years"], s["values"]))
    a = dict(zip(out["precommitted_consumption_eur_bn"]["years"], out["precommitted_consumption_eur_bn"]["values"]))
    b = dict(zip(out["household_rdb_eur_bn"]["years"], out["household_rdb_eur_bn"]["values"]))
    for y in v:
        if not (abs(100 * a[y] / b[y] - v[y]) < 0.05):
            raise ValueError(("t_2103 share inconsistent", y))

    cna = parse_bdm(raw / "insee_cna2014_rdb.xml")
    rdb, arb = _annual(cna["010562201"]["obs"]), _annual(cna["010562212"]["obs"])
    out["precommitted_share_of_rdb_b2014"] = _series(
        "INSEE BDM 010562201 and 010562212 (comptes nationaux base 2014, séries arrêtées)",
        BDM + "010562201+010562212", "% of household gross disposable income",
        {y: round(100 * (1 - arb[y] / rdb[y]), 3) for y in sorted(set(rdb) & set(arb))},
        "1 - RDB arbitrable / RDB, base 2014. Older national-accounts base, kept as a cross-check.")
    return out


def _find_sheet(sheets, pattern):
    for name, rows in sheets:
        for r in rows[:3]:
            if any(c and re.search(pattern, str(c)) for c in r):
                return rows
    raise KeyError(pattern)


def _load_ip1815(raw):
    sheets = read_xlsx(raw / "insee_ip1815.xlsx")
    q = ["q1", "q2", "q3", "q4", "q5"]
    labels = ["1er quintile", "2e quintile", "3e quintile", "4e quintile", "5e quintile"]
    src = "INSEE Première n°1815 (Accardo & Billot, 2020), data file"
    out = {}

    rows = _find_sheet(sheets, r"^Figure 7")
    vals = {}
    for r in rows:
        if r and r[0]:
            for k, lab in zip(q, labels):
                if r[0].strip().startswith(lab):
                    vals[k] = {"precommitted": _num(r[1]), "hardly_compressible": _num(r[2]), "compressible": _num(r[3])}
            if r[0].strip() == "Ensemble":
                vals["all"] = {"precommitted": _num(r[1]), "hardly_compressible": _num(r[2]), "compressible": _num(r[3])}
    out["ip1815_consumption_structure_2017"] = {
        "source": src + " Figure 7", "url": IP1815, "unit": "% of consumption excluding imputed rents",
        "years": [2017], "groups": q + ["all"], "values": vals, "shape": "by_group",
        "notes": "Quintiles of RDB per consumption unit (national accounts distributed with ERFS/BdF), "
                 "ordinary households, France. Pre-committed = housing and related charges, water, "
                 "energy, insurance (excl. life), financial services; share of consumption *excluding "
                 "imputed rents*, so not directly a share of disposable income. Page: " + IP1815_PAGE}

    rows = _find_sheet(sheets, r"^Figure 6")
    vals = {}
    for r in rows:
        if r and r[0]:
            for k, lab in zip(q + ["all"], labels + ["Ensemble"]):
                if r[0].strip() == lab:
                    vals[k] = {"consumption_per_uc": _num(r[1]), "rdb_per_uc": _num(r[2])}
    out["ip1815_rdb_consumption_per_uc_2017"] = {
        "source": src + " Figure 6", "url": IP1815, "unit": "EUR per consumption unit per year, 2017",
        "years": [2017], "groups": q + ["all"], "values": vals, "shape": "by_group",
        "notes": "Consumption per UC includes imputed rents (national-accounts consumption)."}

    rows = _find_sheet(sheets, r"Figure 5")
    yrs, series = [], {k: [] for k in q + ["all"]}
    for r in rows:
        cells = [c for c in r if c is not None]
        if cells and re.fullmatch(r"\d{4}", str(cells[0])):
            yrs.append(int(cells[0]))
            for k, v in zip(q + ["all"], cells[1:7]):
                series[k].append(_num(v))
    out["ip1815_savings_rate"] = {
        "source": src + " Figure 5", "url": IP1815, "unit": "% of RDB", "years": yrs,
        "groups": q + ["all"], "values": series, "shape": "by_group",
        "notes": "Savings rate by quintile of RDB/UC, national accounts base 2014."}
    return out


def _load_spatial(raw, manual):
    rows = _find_sheet(read_xlsx(raw / "insee_ip1959.xlsx"), r"Tableau complémentaire 1")
    items = {}
    for r in rows:
        if r and r[0] and len(r) >= 4 and _num(r[3]) is not None:
            items[r[0].strip()] = {"province_basket": _num(r[1]), "paris_basket": _num(r[2]), "fisher": _num(r[3])}
    out = {"spatial_price_gap_2022": {
        "source": "INSEE Première n°1959 (July 2023), Tableau complémentaire 1", "url": IP1959,
        "unit": "% price gap, Paris urban unit vs province excl. Corsica", "years": [2022],
        "values": items, "shape": "by_item",
        "notes": "Survey March-April 2022. 'Région parisienne' = unité urbaine de Paris (not "
                 "Île-de-France). Fisher = geometric mean of the gaps on the province and Paris "
                 "baskets. Page: " + IP1959_PAGE}}
    path = manual / "insee_spatial_price_gap.csv"
    if path.exists():
        items, urls = {}, set()
        with open(path, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                items[r["item"]] = {k: _num(r[k]) for k in ("province_basket", "paris_basket", "fisher")}
                urls.add(r["source_url"])
        out["spatial_price_gap_2015"] = {
            "source": "INSEE Première n°1590 (April 2016), Figure 1 (manual: " + path.name + ")",
            "url": " | ".join(sorted(urls)), "unit": "% price gap, Paris urban unit vs province excl. Corsica",
            "years": [2015], "values": items, "shape": "by_item",
            "notes": "Survey March 2015. Basket-specific gaps published only for the total "
                     "(+9.2% province basket, -7.8% for a Paris household moving to province)."}
    return out


def _load_manual_precommitted(manual):
    path = manual / "precommitted_spending_surveys.csv"
    if not path.exists():
        return {}
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            r["value"] = _num(r["value"])
            rows.append(r)
    return {"precommitted_surveys": {
        "source": "Hand-compiled: DREES Études et Résultats n°1055 (2018); France Stratégie Note "
                  "d'analyse n°102 (2021)", "url": " | ".join(sorted({r['source_url'] for r in rows})),
        "unit": "see 'unit' per row", "years": sorted({int(r["year"]) for r in rows}), "values": rows,
        "shape": "rows",
        "notes": "Survey (Budget de famille) definition: includes mortgage repayments, gross rents. "
                 "Groups: poor (<60% median niveau de vie), modest non-poor (poverty line to D4), "
                 "middle (D4 to Q3), affluent (>Q3). Do not mix the 'disposable income' and "
                 "'total expenditure' denominators."}}


def load(raw_dir, manual_dir=None):
    raw = Path(raw_dir) / "prices"
    manual = Path(manual_dir) if manual_dir else Path(raw_dir).resolve().parent / "manual"
    out = {}
    out.update(_load_cpi(raw))
    out.update(_load_precommitted_macro(raw))
    out.update(_load_ip1815(raw))
    out.update(_load_spatial(raw, manual))
    out.update(_load_manual_precommitted(manual))
    json.dumps(out)  # must be serialisable
    return out


def _summary(d):
    def at(key, y):
        s = d[key]
        return dict(zip(s["years"], s["values"])).get(y)

    print(f"{len(d)} series")
    for k, s in d.items():
        ys = s["years"]
        print(f"  {k:48s} {ys[0] if ys else '-'}-{ys[-1] if ys else '-'}  [{s['unit']}]")
    c = d["cpi_all"]
    print("CPI all households 2024/1996: %.4f" % (at("cpi_all", 2024) / at("cpi_all", 1996)))
    print("CPI decile <D1 vs >D9, 2024/1998: %.4f vs %.4f" % (
        at("cpi_decile_lt_d1", 2024) / at("cpi_decile_lt_d1", 1998),
        at("cpi_decile_gt_d9", 2024) / at("cpi_decile_gt_d9", 1998)))
    s = d["precommitted_share_of_rdb"]
    print("Pre-committed share of RDB (base 2020): %s %.1f%% ... %s %.1f%%" % (s["years"][0], s["values"][0], s["years"][-1], s["values"][-1]))


if __name__ == "__main__":
    fetch(sys.argv[1])
    _summary(load(sys.argv[1]))
