"""Housing price levels (EUR per m2) and indices: France, Île-de-France / Paris, rest of France.

    python3 -I pipeline/sources/housing.py <raw_dir>     # fetch + load + summary

Standalone: standard library only, imports no project module.
`fetch(raw_dir)` downloads into <raw_dir>/housing/; `load(raw_dir)` parses those files plus
<raw_dir>/../manual/notaires_idf_apartment_prices_m2.csv into a JSON-serialisable dict
{key: {"source", "url", "unit", "years", "values", "notes", ...}}.

Series
------
INSEE BDM, "Indice des prix des logements anciens" (Notaires-INSEE), quarterly, base 100 =
annual average 2015, *série brute* unless stated; turned into annual means of four quarters
(complete years only). Titles are INSEE's TITLE_FR, re-read from the file:
  010567058  France métropolitaine - Ensemble                         1996-
  010567056  France métropolitaine - Appartements                     1996-
  010567060  France métropolitaine - Maisons                          1996-
  010567059  France métropolitaine - Ensemble - CVS (series already used by build_data.py)
  010567118  France (hors Mayotte) - Ensemble                         2010-
  010567012  Paris - Appartements                                     1992-
  010567076  Île-de-France : Appartements                             1996-
  010567078  Île-de-France : Ensemble                                 1996-
  010567090  Île-de-France : Maisons                                  1996-
  010567088  Île-de-France, hors Paris - Ensemble                     1996-
  010567072  Province - Ensemble                                      1995- (from 1994-Q4)
  010567062  Province - Appartements                                  1995-
  010567074  Province - Maisons                                       1995-
These are quality-adjusted (hedonic) indices of existing dwellings: they give changes, not levels.

DVF aggregated statistics (Etalab / data.gouv.fr "Statistiques DVF", dataset 64998de5926530ebcecc7b15)
  https://data-pipeline-open.s3.sbg.io.cloud.ovh.net/dvf/stats_dvf.csv (~280 MB, monthly, all
  geographic levels). fetch() streams it once and keeps only the département and nation rows
  (~6,000 lines). Columns used: nb_ventes_*, moy_prix_m2_*, med_prix_m2_* for appartement, maison,
  apt_maison. Built here, per calendar year:
    mean price per m2 = sum(nb x mean) / sum(nb) over months and départements (exact: in the
      Etalab code, département nb and mean are computed on the same sales);
    "median" = nb-weighted average of monthly département medians: an APPROXIMATION, medians do
      not aggregate.
  Groups: paris (75), idf (75,77,78,91,92,93,94,95), rest_metro (metropolitan départements outside
  Île-de-France), metro, dvf_all (all départements incl. DOM). The Etalab "nation" row is NOT used:
  its nb_ventes counts all sales incl. multi-property ones, which do not enter its mean.
  Coverage: DVF excludes Bas-Rhin, Haut-Rhin, Moselle (Livre foncier) and Mayotte. Sales =
  "Vente", "Vente en l'état futur d'achèvement" (off-plan new build) and "Adjudication",
  single-property transactions, price/m2 < 100,000 EUR; so not "existing dwellings" only.
  The file is a rolling 5-year window (currently 2021-2025): older years drop out on refresh.

Notaires-INSEE price levels, Paris and Île-de-France (manual CSV generated from the PDF)
  data/manual/notaires_idf_apartment_prices_m2.csv, from Paris Notaires Services, "Prix au m² des
  appartements anciens sous-jacents aux indices Notaires-INSEE",
  https://paris.notaires.fr/sites/default/files/Historiquedesprixdesappartementspardep_5.pdf
  Quarterly, Paris 1991-, Île-de-France 1996-, existing flats sold freehold with vacant possession.

Built back-casts (levels before DVF): level(y) = DVF mean(anchor) x index(y) / index(anchor), anchor
= last complete DVF year. Reads "price per m2 in year y of the dwellings sold in the anchor year,
quality held constant". rest_metro uses INSEE "Province" indices (France métropolitaine outside
Île-de-France, which includes Alsace-Moselle and Corsica, unlike DVF).
"""
import csv
import io
import os
import json
import re
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

BDM = "https://bdm.insee.fr/series/sdmx/data/SERIES_BDM/"
UA = {"User-Agent": "show-me-your-pie/0.1 (open data research)"}
HPI = {
    "hpi_france_metro_all": "010567058",
    "hpi_france_metro_apartments": "010567056",
    "hpi_france_metro_houses": "010567060",
    "hpi_france_metro_all_sa": "010567059",
    "hpi_france_excl_mayotte_all": "010567118",
    "hpi_paris_apartments": "010567012",
    "hpi_idf_apartments": "010567076",
    "hpi_idf_all": "010567078",
    "hpi_idf_houses": "010567090",
    "hpi_idf_excl_paris_all": "010567088",
    "hpi_province_all": "010567072",
    "hpi_province_apartments": "010567062",
    "hpi_province_houses": "010567074",
}
DVF_URL = "https://data-pipeline-open.s3.sbg.io.cloud.ovh.net/dvf/stats_dvf.csv"
DVF_PAGE = "https://www.data.gouv.fr/fr/datasets/statistiques-dvf/"
NOTAIRES_URL = "https://paris.notaires.fr/sites/default/files/Historiquedesprixdesappartementspardep_5.pdf"
IDF = {"75", "77", "78", "91", "92", "93", "94", "95"}
TYPES = {"apartments": "appartement", "houses": "maison", "all": "apt_maison"}


def _get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300)


def fetch(raw_dir):
    out = Path(raw_dir) / "housing"
    out.mkdir(parents=True, exist_ok=True)
    data = _get(BDM + "+".join(HPI.values())).read()
    if b"<Series" not in data:
        raise RuntimeError("INSEE BDM: no series in response")
    part = out / "insee_hpi_regions.xml.part"
    part.write_bytes(data)
    os.replace(part, out / "insee_hpi_regions.xml")
    print("wrote", out / "insee_hpi_regions.xml", f"({len(data):,} bytes)")

    kept = 0
    part = out / "dvf_stats_departements.csv.part"  # renamed only once complete
    with _get(DVF_URL) as r, open(part, "w", newline="", encoding="utf-8") as f:
        reader = csv.reader(io.TextIOWrapper(r, encoding="utf-8", newline=""))
        header = next(reader)
        col = header.index("echelle_geo")
        w = csv.writer(f)
        w.writerow(header)
        for row in reader:
            if len(row) > col and row[col] in ("departement", "nation"):
                w.writerow(row)
                kept += 1
    if kept < 1000:
        raise RuntimeError(f"DVF stats: only {kept} département/nation rows kept")
    os.replace(part, out / "dvf_stats_departements.csv")
    print("wrote", out / "dvf_stats_departements.csv", f"({kept:,} rows kept)")


def parse_bdm(path):
    text = Path(path).read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"<Series ([^>]*?)>(.*?)</Series>", text, re.S):
        attrs = dict(re.findall(r'([A-Z_][A-Z_0-9\-]*)="([^"]*)"', m.group(1)))
        obs = {}
        for o in re.finditer(r"<Obs ([^>]*?)/>", m.group(2)):
            a = dict(re.findall(r'([A-Z_]+)="([^"]*)"', o.group(1)))
            if a.get("OBS_VALUE", "") not in ("", "NaN"):
                obs[a["TIME_PERIOD"]] = float(a["OBS_VALUE"])
        out[attrs["IDBANK"]] = {"title": attrs.get("TITLE_FR", "").strip(), "attrs": attrs, "obs": obs}
    return out


def _series(source, url, unit, values, notes, **extra):
    years = sorted(values)
    d = {"source": source, "url": url, "unit": unit, "years": years,
         "values": [values[y] for y in years], "notes": notes}
    d.update(extra)
    return d


def _annual_from_quarters(obs):
    q = defaultdict(list)
    for p, v in obs.items():
        m = re.fullmatch(r"(\d{4})-Q[1-4]", p)
        if m:
            q[int(m.group(1))].append(v)
    return {y: round(sum(v) / 4, 3) for y, v in q.items() if len(v) == 4}


def _load_hpi(raw):
    bdm = parse_bdm(raw / "insee_hpi_regions.xml")
    out = {}
    for key, idb in HPI.items():
        s = bdm[idb]
        out[key] = _series(f"INSEE BDM idbank {idb}", BDM + idb, "index, 2015 = 100 (annual mean of quarters)",
                           _annual_from_quarters(s["obs"]), s["title"], idbank=idb, title=s["title"],
                           last_update=s["attrs"].get("LAST_UPDATE"))
    return out


def _load_dvf(raw):
    acc = defaultdict(lambda: [0, 0.0, 0.0])        # (group, type, year) -> [nb, sum nb*mean, sum nb*median]
    months = defaultdict(set)
    depts = defaultdict(set)                         # (year, month) -> départements seen
    with open(raw / "dvf_stats_departements.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["echelle_geo"] != "departement":
                continue
            year, month = r["annee_mois"].split("-")
            year = int(year)
            months[year].add(month)
            code = r["code_geo"]
            depts[(year, month)].add(code)
            groups = ["dvf_all"]
            if not code.startswith("97"):
                groups.append("metro")
                groups.append("idf" if code in IDF else "rest_metro")
            if code == "75":
                groups.append("paris")
            for t, col in TYPES.items():
                nb, mean, med = r[f"nb_ventes_{col}"], r[f"moy_prix_m2_{col}"], r[f"med_prix_m2_{col}"]
                if not nb or not mean or not med:
                    continue
                nb = int(float(nb))
                for g in groups:
                    a = acc[(g, t, year)]
                    a[0] += nb
                    a[1] += nb * float(mean)
                    a[2] += nb * float(med)
    # A year counts only if all 12 months are present for (almost) every
    # département: a truncated download would otherwise shift the averages.
    full = {y for y, m in months.items() if len(m) == 12 and all(len(depts[(y, mm)]) >= 90 for mm in m)}
    if not full:
        raise RuntimeError("DVF statistics: no complete year (file truncated?)")
    out = {}
    labels = {"paris": "Paris (75)", "idf": "Île-de-France (8 départements)",
              "rest_metro": "metropolitan France outside Île-de-France, excl. Bas-Rhin, Haut-Rhin, Moselle",
              "metro": "metropolitan France excl. Bas-Rhin, Haut-Rhin, Moselle",
              "dvf_all": "all DVF départements (metropolitan excl. Alsace-Moselle, plus 971-974)"}
    for g, label in labels.items():
        for t in TYPES:
            ys = [y for y in sorted(full) if (g, t, y) in acc]
            mean = {y: round(acc[(g, t, y)][1] / acc[(g, t, y)][0]) for y in ys}
            med = {y: round(acc[(g, t, y)][2] / acc[(g, t, y)][0]) for y in ys}
            nb = {y: acc[(g, t, y)][0] for y in ys}
            common = (f"{label}; {t}. Etalab DVF statistics, single-property sales (incl. VEFA and "
                      f"auctions), price/m2 = sale value / built surface. Complete calendar years only. "
                      f"Dataset page: {DVF_PAGE}")
            out[f"dvf_{g}_{t}_mean_eur_m2"] = _series("Etalab, Statistiques DVF (monthly, by département)", DVF_URL,
                                                      "EUR per m2, current", mean, "Sales-weighted mean. " + common,
                                                      n_sales=[nb[y] for y in ys])
            out[f"dvf_{g}_{t}_median_approx_eur_m2"] = _series(
                "Etalab, Statistiques DVF (monthly, by département)", DVF_URL, "EUR per m2, current", med,
                "APPROXIMATE annual median: sales-weighted average of monthly département medians. " + common)
    return out


def _load_notaires(manual):
    path = manual / "notaires_idf_apartment_prices_m2.csv"
    if not path.exists():
        return {}
    q = defaultdict(lambda: defaultdict(list))
    cols = None
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        cols = [c for c in reader.fieldnames if c.endswith("_eur_m2")]
        for r in reader:
            for c in cols:
                if r[c]:
                    q[c][int(r["year"])].append(float(r[c]))
    out = {}
    for c in cols:
        vals = {y: round(sum(v) / 4) for y, v in q[c].items() if len(v) == 4}
        out["notaires_" + c.replace("_eur_m2", "") + "_apartments_eur_m2"] = _series(
            "Paris Notaires Services, prix au m2 des appartements anciens sous-jacents aux indices Notaires-INSEE "
            "(manual: " + path.name + ")", NOTAIRES_URL, "EUR per m2, current (annual mean of 4 quarters)", vals,
            "Existing flats, sold freehold with vacant possession by mutual agreement. Price level consistent "
            "with the Notaires-INSEE quality-adjusted index (not a raw median of the year's sales).")
    return out


def _backcast(out, dvf_key, hpi_key, key, label):
    dvf = dict(zip(out[dvf_key]["years"], out[dvf_key]["values"]))
    idx = dict(zip(out[hpi_key]["years"], out[hpi_key]["values"]))
    anchor = max(y for y in dvf if y in idx)
    vals = {y: round(dvf[anchor] * v / idx[anchor]) for y, v in idx.items()}
    out[key] = _series(
        f"Derived: {dvf_key} in {anchor} x {out[hpi_key]['idbank']} index", out[hpi_key]["url"],
        "EUR per m2, current", vals,
        f"{label}. Back-cast = DVF mean price/m2 in anchor year {anchor} x INSEE index(y) / index({anchor}). "
        "Quality-constant level of the anchor-year mix, not an observed average of each year's sales.",
        anchor_year=anchor, anchor_value=dvf[anchor])


def load(raw_dir, manual_dir=None):
    raw = Path(raw_dir) / "housing"
    manual = Path(manual_dir) if manual_dir else Path(raw_dir).resolve().parent / "manual"
    out = {}
    out.update(_load_hpi(raw))
    out.update(_load_dvf(raw))
    out.update(_load_notaires(manual))
    _backcast(out, "dvf_rest_metro_apartments_mean_eur_m2", "hpi_province_apartments",
              "backcast_rest_metro_apartments_eur_m2", "Flats, metropolitan France outside Île-de-France")
    _backcast(out, "dvf_rest_metro_houses_mean_eur_m2", "hpi_province_houses",
              "backcast_rest_metro_houses_eur_m2", "Houses, metropolitan France outside Île-de-France")
    _backcast(out, "dvf_rest_metro_all_mean_eur_m2", "hpi_province_all",
              "backcast_rest_metro_all_eur_m2", "Flats and houses, metropolitan France outside Île-de-France")
    _backcast(out, "dvf_metro_all_mean_eur_m2", "hpi_france_metro_all",
              "backcast_metro_all_eur_m2", "Flats and houses, metropolitan France")
    _backcast(out, "dvf_idf_all_mean_eur_m2", "hpi_idf_all",
              "backcast_idf_all_eur_m2", "Flats and houses, Île-de-France")
    _backcast(out, "dvf_paris_apartments_mean_eur_m2", "hpi_paris_apartments",
              "backcast_paris_apartments_eur_m2", "Flats, Paris (cross-check of the Notaires level)")
    if "notaires_paris_apartments_eur_m2" in out:
        n = dict(zip(out["notaires_paris_apartments_eur_m2"]["years"], out["notaires_paris_apartments_eur_m2"]["values"]))
        d = dict(zip(out["dvf_paris_apartments_mean_eur_m2"]["years"], out["dvf_paris_apartments_mean_eur_m2"]["values"]))
        out["check_paris_dvf_mean_over_notaires"] = _series(
            "Derived", DVF_URL + " | " + NOTAIRES_URL, "ratio", {y: round(d[y] / n[y], 4) for y in d if y in n},
            "DVF mean price/m2 of Paris flats divided by the Notaires-INSEE Paris level, same year.")
    json.dumps(out)
    return out


def _summary(d):
    def at(k, y):
        return dict(zip(d[k]["years"], d[k]["values"])).get(y)

    print(f"{len(d)} series")
    for k, s in d.items():
        ys = s["years"]
        print(f"  {k:52s} {ys[0] if ys else '-'}-{ys[-1] if ys else '-'}  [{s['unit']}]")
    y = d["dvf_metro_all_mean_eur_m2"]["years"][-1]
    print(f"DVF {y}, flats, mean EUR/m2: Paris {at('dvf_paris_apartments_mean_eur_m2', y)}, "
          f"IDF {at('dvf_idf_apartments_mean_eur_m2', y)}, rest of metro {at('dvf_rest_metro_apartments_mean_eur_m2', y)}")
    if "notaires_paris_apartments_eur_m2" in d:
        print(f"Notaires Paris flats EUR/m2: 1991 {at('notaires_paris_apartments_eur_m2', 1991)}, "
              f"{y} {at('notaires_paris_apartments_eur_m2', y)}")


if __name__ == "__main__":
    fetch(sys.argv[1])
    _summary(load(sys.argv[1]))
