"""INSEE official distribution statistics for France: cross-checks for WID.

    python3 -I pipeline/sources/insee.py <raw_dir>

downloads every table below into ``<raw_dir>/insee/``, parses them and prints
a summary. Standard library only; xlsx files are read with zipfile + ElementTree.
This module imports nothing from the project.

Tables used
-----------
A. ERFS, *niveau de vie* (disposable income per consumption unit, OECD-modified
   scale, every person in the household gets the household's niveau de vie).
   Field: France métropolitaine, persons in ordinary housing whose household
   has non-negative declared income and whose reference person is not a
   student. Source: Insee-DGFiP-Cnaf-Cnav-CCMSA, enquêtes Revenus fiscaux et
   sociaux (ERFS).

   ``erfs_indicators``  "Niveau de vie et indicateurs d'inégalités, données
       annuelles de 1975 à 2024", https://www.insee.fr/fr/statistiques/2491918,
       file ``reve-niv-vie-indic-inegalite.xlsx``. D1, median, D9, mean
       (constant 2024 euros), D9/D1, D9/D5, D5/D1, S20, S40, S50, S80, S90 (%),
       (100-S80)/S20, Palma (100-S90)/S40, (100-S90)/S50, Gini (3 decimals).
       Columns 1975-1990 and the first "1996" are the old concept without
       financial income; "1996¹" onwards is the current series.
   ``erfs_deciles``  "Distribution des niveaux de vie, données annuelles de 1996
       à 2024", https://www.insee.fr/fr/statistiques/2416808, file
       ``reve-niv-vie-decile-individu.xlsx``. D1..D9 and P95 thresholds
       (constant 2024 euros), D9/D1.
   ``erfs_mean_by_decile``  "Niveau de vie et revenu disponible - Séries longues
       1996-2023", https://www.insee.fr/fr/statistiques/8731524, file
       ``irsocerfs2023_DNV01_bis.xlsx`` (table DNV01bis): mean niveau de vie
       of each tenth (constant 2023 euros), overall mean, ratio top/bottom tenth.
   ``erfs_decile_shares``  same page, ``irsocerfs2023_DNV02.xlsx`` (DNV02):
       share of the total mass of niveaux de vie held by each tenth (%).
   ``erfs_vingtiles``  same page, ``irsocerfs2023_DNV01.xlsx`` (DNV01): P5..P95
       thresholds every 5 points (constant 2023 euros) and number of persons.
   ``erfs_before_redistribution``  same page, ``irsocerfs2023_IG5.xlsx`` (IG5):
       deciles and mean of niveau de vie *before* redistribution (declared
       income incl. pensions and unemployment benefits, before taxes and
       social benefits), constant 2023 euros, D9/D1.
   ``erfs_ig1``  same page, ``irsocerfs2023_IG1.xlsx`` (IG1): same indicators
       as ``erfs_indicators`` in 2023 euros, with the unrounded Gini.

   ERFS series breaks (columns are kept separate, never spliced):
   2010 (financial income imputed from the Patrimoine 2010 survey), 2012
   (survey renovated: tax paid in the year, pension bonus for 3+ children and
   employer health insurance counted; financial income from Patrimoine
   2014-2015), 2020 (fragile point; from 2020 on, renovated ERFS chain based on
   the new Labour Force Survey). Each break appears as two columns for the
   same year, e.g. "2010" and "2010 (1)". INSEE warns that pre-2020 values
   differ from the retropolated series in Insee Première "Niveau de vie et
   pauvreté en 2024" (not used here).

B. Wealth surveys (Patrimoine 1998-2015, Histoire de vie et Patrimoine 2018-),
   unit = HOUSEHOLD, gross or net wealth, ranked by the same wealth concept,
   survey only (not calibrated to national accounts). Field: France hors
   Mayotte, ordinary housing (France métropolitaine before 2010).

   ``hvp_inequality``  Insee Focus n° 371 (Dec. 2025),
       https://www.insee.fr/fr/statistiques/8672665, file ``IF371.xlsx``,
       sheet "Tableau complémentaire 1": share of total *gross* wealth (and of
       housing, financial, business wealth) held by the top 50/25/10/5/1% of
       households, and Gini, for 2015, 2018, 2021, 2024 (waves re-weighted
       consistently in 2024).
   ``hvp_thresholds``  same file, "Tableau complémentaire 2": D1..D9, P95, P99
       of gross and net wealth, current and constant-2024 euros, 2015-2024.
   ``hvp_long_series``  "Patrimoine et endettement des ménages en 2021 et en
       séries longues", https://www.insee.fr/fr/statistiques/8263048, file
       ``hvp_series_longues_fr.xlsx``: mean *gross wealth excluding residual
       assets* (no cars, durables, jewellery, art) by tenth / P90-95 / P95-99 /
       top 1%, deciles, Gini, mean net wealth hors reste; waves 1998, 2004,
       2010, 2015, 2018, 2021 in current euros. Two 2010 columns (old and new
       method) and two fields (metropolitan France / France hors Mayotte).
       Shares of top 10%, top 1%, bottom 50% are DERIVED here from bracket
       means (each bracket is a fixed share of households).
   ``hvp_net_by_gross_2021``  same publication, https://www.insee.fr/fr/
       statistiques/8262352, file ``hvp_mtmoymed_patbrut_patnet_fr.xlsx``,
       sheet PATBRUT: mean gross and net wealth by tenth of GROSS wealth, 2021.
       Net-wealth shares of the top 10% / bottom 50% by gross wealth are
       DERIVED: they bound the true net-wealth shares (top 10% by net wealth
       holds at least as much; bottom 50% by net wealth holds at most as much).
   ``hvp_lorenz_2021``  Revenus et patrimoine des ménages 2024, vue d'ensemble,
       https://www.insee.fr/fr/statistiques/7941439, file ``RPM2024-VE2.xlsx``,
       figure 2: Lorenz curve of gross wealth hors reste, 2021 (cross-check).

C. Distributed national accounts (comptes nationaux distribués, CND):
   national income (net national income, all sectors) split across persons
   ranked by their usual niveau de vie (ERFS concept), per consumption unit.
   "Before transfers" = extended primary income (pensions and unemployment
   benefits are treated as transfers, NOT primary income); "after transfers"
   = niveau de vie élargi, incl. in-kind transfers and collective spending.
   Field: France.

   ``cnd_2019``  Insee Analyses n° 88 (André, Germain, Sicsic, Sept. 2023),
       https://www.insee.fr/fr/statistiques/7669723, file ``IA88.xlsx``:
       "Tableau complémentaire 1" (pseudo-Gini, Palma, (100-S80)/S20 for each
       income concept) and "Tableau complémentaire 2" (euros per UC by
       twentieth). Group shares are DERIVED with UC counts per twentieth
       recovered as (net transfers in bn) / (net transfers per UC).
   ``cnd_2022``  Insee Première n° 2022 (Nov. 2024),
       https://www.insee.fr/fr/statistiques/8275760, file ``ip2022.xlsx``,
       figure 2 and complementary table: masses in billions by tenth and
       twentieth; shares derived as mass / total.
   ``cnd_2023``  Insee Analyses n° 118 (2026),
       https://www.insee.fr/fr/statistiques/8974371, file ``IA118.xlsx``,
       figures 2b (billions by tenth) and 3a (pseudo-Gini, Palma, S80/S20).
       New conventions (primary income at basic prices, public deficit shown
       separately): not a continuation of the 2019 and 2022 vintages.

   CND groups are ranked by USUAL niveau de vie, not by extended income, so a
   "top 10%" share here is a concentration share (pseudo-Gini logic), lower
   than a share ranked by the measured income itself.

Output conventions
------------------
* Every value is copied from the file; shares are converted from percent to
  fractions (22.5 -> 0.225) and their keys end in ``_share``. Anything not
  printed in the file is under a key containing ``derived`` with its formula.
* Each table has "source", "url", "file", "unit", "field", "columns" (one entry
  per column of the file, with its exact label, so duplicate-year break columns
  survive), "years" (the int year of each column), data arrays aligned with
  "columns", "segments" (runs of columns between breaks) and "breaks"/"notes"
  (the footnotes of the file, verbatim).
* Missing values ("nd", "#N/A", "///", "so") are None.
"""
import hashlib
import json
import re
import sys
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

BASE = "https://www.insee.fr/fr/statistiques/fichier/"
FILES = {
    # key: (page, file)
    "erfs_indicators": ("2491918", "reve-niv-vie-indic-inegalite.xlsx"),
    "erfs_deciles": ("2416808", "reve-niv-vie-decile-individu.xlsx"),
    "erfs_ig1": ("8731524", "irsocerfs2023_IG1.xlsx"),
    "erfs_vingtiles": ("8731524", "irsocerfs2023_DNV01.xlsx"),
    "erfs_mean_by_decile": ("8731524", "irsocerfs2023_DNV01_bis.xlsx"),
    "erfs_decile_shares": ("8731524", "irsocerfs2023_DNV02.xlsx"),
    "erfs_before_redistribution": ("8731524", "irsocerfs2023_IG5.xlsx"),
    "hvp_if371": ("8672665", "IF371.xlsx"),
    "hvp_long_series": ("8263048", "hvp_series_longues_fr.xlsx"),
    "hvp_net_by_gross_2021": ("8262352", "hvp_mtmoymed_patbrut_patnet_fr.xlsx"),
    "hvp_lorenz_2021": ("7941439", "RPM2024-VE2.xlsx"),
    "cnd_2019": ("7669723", "IA88.xlsx"),
    "cnd_2022": ("8275760", "ip2022.xlsx"),
    "cnd_2023": ("8974371", "IA118.xlsx"),
}
PAGE = "https://www.insee.fr/fr/statistiques/"
UA = "Mozilla/5.0 (show_me_your_pie data pipeline; python urllib)"
MISSING = {"", "nd", "#n/a", "///", "so", "-", "n.d."}

ERFS_FIELD = ("France métropolitaine, persons in ordinary housing, household declared "
              "income >= 0, reference person not a student")
ERFS_UNIT_NOTE = ("niveau de vie = household disposable income / consumption units "
                  "(1 + 0.5 per other person aged 14+ + 0.3 per child under 14); "
                  "every person is ranked by and counted with the niveau de vie of "
                  "their household")


# --------------------------------------------------------------------------- download

def _dir(raw_dir):
    return Path(raw_dir) / "insee"


def fetch(raw_dir):
    """Download every file into <raw_dir>/insee/. Returns {key: error} for failures."""
    out = _dir(raw_dir)
    out.mkdir(parents=True, exist_ok=True)
    errors = {}
    for key, (page, name) in FILES.items():
        url = BASE + page + "/" + name
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            data = urllib.request.urlopen(req, timeout=60).read()
            tmp = out / (name + ".part")
            tmp.write_bytes(data)
            if not zipfile.is_zipfile(tmp):
                tmp.unlink()
                raise ValueError("not an xlsx (zip) file, %d bytes" % len(data))
            tmp.replace(out / name)
            print("wrote", out / name, len(data), "bytes")
        except Exception as exc:  # keep going; load() reports what is missing
            errors[key] = "%s: %s" % (url, exc)
            print("FAILED", url, exc, file=sys.stderr)
    return errors


# --------------------------------------------------------------------------- xlsx reading

_NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
       "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
_T = "{%s}t" % _NS["m"]


def _colnum(ref):
    n = 0
    for ch in re.match(r"[A-Z]+", ref).group():
        n = n * 26 + ord(ch) - 64
    return n - 1


def read_xlsx(path):
    """{sheet name: [(row number, {col index: text})]} with cell values as strings."""
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", _NS):
            shared.append("".join(t.text or "" for t in si.iter(_T)))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = {r.get("Id"): r.get("Target")
            for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
    sheets = {}
    for sh in wb.find("m:sheets", _NS):
        target = rels[sh.get("{%s}id" % _NS["r"])].lstrip("/")
        if not target.startswith("xl/"):
            target = "xl/" + target
        rows = []
        for row in ET.fromstring(z.read(target)).iter("{%s}row" % _NS["m"]):
            cells = {}
            for c in row.findall("m:c", _NS):
                v, kind = c.find("m:v", _NS), c.get("t")
                if kind == "s" and v is not None:
                    val = shared[int(v.text)]
                elif kind == "inlineStr":
                    val = "".join(t.text or "" for t in c.iter(_T))
                elif v is not None:
                    val = v.text
                else:
                    continue
                cells[_colnum(c.get("r"))] = val
            if cells:
                rows.append((int(row.get("r")), cells))
        sheets[sh.get("name")] = rows
    return sheets


def _norm(text):
    """Lower case, no accents, superscripts folded, single spaces."""
    t = unicodedata.normalize("NFKD", str(text))
    t = "".join(ch for ch in t if not unicodedata.combining(ch))
    return " ".join(t.lower().replace("’", "'").split())


def _num(text):
    if text is None:
        return None
    s = str(text).strip()
    if _norm(s) in MISSING:
        return None
    try:
        return float(s.replace(" ", "").replace(" ", "").replace(",", "."))
    except ValueError:
        return None


def _clean(x, digits=6):
    """Round float noise from xlsx storage (0.64500000000000002 -> 0.645)."""
    if x is None:
        return None
    r = round(x, digits)
    return int(r) if r == int(r) and abs(r) >= 1 else r


class Sheet:
    def __init__(self, rows, name):
        self.rows, self.name = rows, name

    def find(self, *needles, col=None, start=0, exact=False):
        """Index of the first row (from `start`) whose label contains all needles
        (or, with exact=True, equals the single needle)."""
        needles = [_norm(n) for n in needles]
        for i in range(start, len(self.rows)):
            cells = self.rows[i][1]
            cols = [col] if col is not None else sorted(c for c in cells if c <= 2)
            for c in cols:
                lab = _norm(cells.get(c, ""))
                if lab and (lab == needles[0] if exact else all(n in lab for n in needles)):
                    return i
        raise KeyError("%s: no row matching %r" % (self.name, needles))

    def cells(self, i):
        return self.rows[i][1]

    def notes(self, after):
        """Footnote texts (column A, no numbers in the row) after row index `after`."""
        out = []
        for _, cells in self.rows[after + 1:]:
            if 0 in cells and len(cells) == 1:
                out.append(" ".join(str(cells[0]).split()))
        return out


def _sheet(sheets, *needles):
    for name, rows in sheets.items():
        if all(_norm(n) in _norm(name) for n in needles):
            return Sheet(rows, name)
    raise KeyError("no sheet matching %r in %s" % (needles, list(sheets)))


_YEAR = re.compile(r"^\s*((?:19|20)\d\d)")


def _year_columns(sheet, header_idx):
    """[(col, label, year)] for every cell of the header row that starts with a year."""
    out = []
    for c, lab in sorted(sheet.cells(header_idx).items()):
        m = _YEAR.match(str(lab))
        if m:
            out.append((c, " ".join(str(lab).split()), int(m.group(1))))
    if not out:
        raise KeyError("%s: no year columns in header row" % sheet.name)
    return out


def _segments(cols):
    """Runs of columns between series breaks: a break starts where a year repeats."""
    segs, start = [], 0
    for i in range(1, len(cols)):
        if cols[i][2] == cols[i - 1][2]:
            segs.append({"from": cols[start][1], "to": cols[i - 1][1],
                         "index": [start, i - 1]})
            start = i
    segs.append({"from": cols[start][1], "to": cols[-1][1], "index": [start, len(cols) - 1]})
    return segs


def _row_values(sheet, i, cols, share=False):
    vals = []
    for c, _, _ in cols:
        v = _num(sheet.cells(i).get(c))
        if v is not None and share:
            v = round(v / 100, 6)
        vals.append(_clean(v))
    return vals


def _table(sheet, header_idx, cols, spec, start=None):
    """spec: [(key, needles, is_share)]; rows searched from the header down."""
    data = {}
    for key, needles, share in spec:
        i = sheet.find(*needles, start=header_idx + 1 if start is None else start)
        data[key] = _row_values(sheet, i, cols, share)
    return data


def _meta(key, unit, field, sheet, cols, notes, **extra):
    page, name = FILES[key]
    d = {"source": extra.pop("source"), "url": BASE + page + "/" + name,
         "page": PAGE + page, "file": name, "sheet": sheet.name, "unit": unit,
         "field": field, "columns": [{"label": l, "year": y} for _, l, y in cols],
         "years": [y for _, _, y in cols], "segments": _segments(cols), "breaks": notes}
    d.update(extra)
    return d


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# --------------------------------------------------------------------------- ERFS

def _erfs_indicators(path):
    s = _sheet(read_xlsx(path), "Donn")
    h = s.find("Indicateur", col=0, exact=True)
    cols = _year_columns(s, h)
    spec = [("D1", ["1er decile de niveau de vie"], False),
            ("median", ["niveau de vie median"], False),
            ("D9", ["9e decile de niveau de vie"], False),
            ("mean", ["niveau de vie annuel moyen"], False),
            ("D9_D1", ["d9/d1"], False), ("D9_D5", ["d9/d5"], False),
            ("D5_D1", ["d5/d1"], False),
            ("S20_share", ["inferieur au 2e decile"], True),
            ("S40_share", ["inferieur au 4e decile"], True),
            ("S50_share", ["inferieur au 5e decile"], True),
            ("S80_share", ["inferieur au 8e decile"], True),
            ("S90_share", ["inferieur au 9e decile"], True),
            ("S80_S20_ratio", ["(100-s80)/s20"], False),
            ("palma", ["(100-s90)/s40"], False),
            ("T10_S50_ratio", ["(100-s90)/s50"], False),
            ("gini", ["indice de gini"], False)]
    d = _table(s, h, cols, spec)
    d["top10_share_derived"] = [None if v is None else round(1 - v, 6) for v in d["S90_share"]]
    d["top20_share_derived"] = [None if v is None else round(1 - v, 6) for v in d["S80_share"]]
    notes = s.notes(s.find("indice de gini"))
    return _meta("erfs_indicators", "D1/median/D9/mean: constant 2024 euros per year per "
                 "consumption unit; shares: fraction of total niveau de vie; ratios, Gini",
                 ERFS_FIELD, s, cols, notes, data=d,
                 source="INSEE, Niveau de vie et indicateurs d'inégalités, 1975-2024 (ERFS)",
                 concept=ERFS_UNIT_NOTE,
                 derived={"top10_share_derived": "1 - S90", "top20_share_derived": "1 - S80"},
                 warning="Columns before '1996¹' exclude financial income (old concept); "
                         "they are not comparable with later columns.")


def _erfs_deciles(path):
    s = _sheet(read_xlsx(path), "Donn")
    h = s.find("Indicateur", col=0, exact=True)
    cols = _year_columns(s, h)
    spec = [("D%d" % k, ["%s decile" % ("1er" if k == 1 else "%de" % k)], False)
            for k in (1, 2, 3, 4, 6, 7, 8, 9)]
    spec += [("median", ["mediane"], False), ("P95", ["95e centile"], False),
             ("D9_D1", ["d9/d1"], False)]
    d = _table(s, h, cols, spec)
    d = {k: d[k] for k in ["D1", "D2", "D3", "D4", "median", "D6", "D7", "D8", "D9",
                           "P95", "D9_D1"]}
    return _meta("erfs_deciles", "constant 2024 euros per year per consumption unit",
                 ERFS_FIELD, s, cols, s.notes(s.find("d9/d1")), data=d,
                 source="INSEE, Distribution des niveaux de vie, 1996-2024 (ERFS)",
                 concept=ERFS_UNIT_NOTE)


def _erfs_ig1(path):
    s = _sheet(read_xlsx(path), "IG1")
    h = s.find("unites")
    cols = _year_columns(s, h)
    spec = [("D1", ["(d1)"], False), ("median", ["(d5)"], False), ("D9", ["(d9)"], False),
            ("mean", ["niveau de vie annuel moyen"], False), ("D9_D1", ["d9/d1"], False),
            ("S20_share", ["(s20)"], True), ("S40_share", ["(s40)"], True),
            ("S50_share", ["(s50)"], True), ("S80_share", ["(s80)"], True),
            ("S90_share", ["(s90)"], True), ("S80_S20_ratio", ["(100-s80)/s20"], False),
            ("palma", ["(100-s90)/s40"], False), ("gini", ["indice de gini"], False)]
    d = _table(s, h, cols, spec)
    return _meta("erfs_ig1", "constant 2023 euros per consumption unit; shares as fractions",
                 ERFS_FIELD, s, cols, s.notes(s.find("indice de gini")), data=d,
                 source="INSEE, ERFS séries longues 1996-2023, table IG1",
                 concept=ERFS_UNIT_NOTE)


def _erfs_vingtiles(path):
    s = _sheet(read_xlsx(path), "DNV01")
    h = s.find("Centile")
    cols = _year_columns(s, h)
    spec = [("P%d" % p, ["%deme centile" % p], False) for p in range(5, 100, 5) if p != 50]
    spec.append(("P50", ["mediane"], False))
    spec.append(("persons_thousands", ["nombre d'individus"], False))
    d = _table(s, h, cols, spec)
    order = ["P%d" % p for p in range(5, 100, 5)] + ["persons_thousands"]
    d = {k: d[k] for k in order}
    return _meta("erfs_vingtiles", "constant 2023 euros per consumption unit; persons in thousands",
                 ERFS_FIELD, s, cols, s.notes(s.find("nombre d'individus")), data=d,
                 source="INSEE, ERFS séries longues 1996-2023, table DNV01",
                 concept=ERFS_UNIT_NOTE)


_TENTHS = [("d1", ["1er decile (a)"]), ("d2", ["entre le 1er et le 2e"]),
           ("d3", ["entre le 2e et le 3e"]), ("d4", ["entre le 3e et le 4e"]),
           ("d5", ["entre le 4e et le 5e"]), ("d6", ["entre le 5e et le 6e"]),
           ("d7", ["entre le 6e et le 7e"]), ("d8", ["entre le 7e et le 8e"]),
           ("d9", ["entre le 8e et le 9e"]), ("d10", ["9e decile (b)"])]


def _erfs_mean_by_decile(path):
    s = _sheet(read_xlsx(path), "DNV01")
    h = s.find("Situation par rapport")
    cols = _year_columns(s, h)
    spec = [("mean_" + k, n, False) for k, n in _TENTHS]
    spec += [("mean_all", ["ensemble"], False), ("ratio_d10_d1", ["rapport (b)/(a)"], False)]
    d = _table(s, h, cols, spec)
    d["ratio_d10_d1"] = [None if v is None else round(v, 4) for v in d["ratio_d10_d1"]]
    return _meta("erfs_mean_by_decile", "constant 2023 euros per consumption unit",
                 ERFS_FIELD, s, cols, s.notes(s.find("rapport (b)/(a)")), data=d,
                 source="INSEE, ERFS séries longues 1996-2023, table DNV01bis",
                 concept=ERFS_UNIT_NOTE)


def _erfs_decile_shares(path):
    s = _sheet(read_xlsx(path), "DNV02")
    h = s.find("Niveau de vie annuel")
    cols = _year_columns(s, h)
    names = [("d1", ["inferieur au 1er decile"]), ("d2", ["entre le 1er et le 2eme"]),
             ("d3", ["entre le 2eme et le 3eme"]), ("d4", ["entre le 3eme et le 4eme"]),
             ("d5", ["entre le 4eme et le 5eme"]), ("d6", ["entre le 5eme et le 6eme"]),
             ("d7", ["entre le 6eme et le 7eme"]), ("d8", ["entre le 7eme et le 8eme"]),
             ("d9", ["entre le 8eme et le 9eme"]), ("d10", ["superieur au 9eme"])]
    d = _table(s, h, cols, [(k + "_share", n, True) for k, n in names])
    d["bottom50_share_derived"] = [
        _clean(round(sum(d["d%d_share" % k][j] for k in range(1, 6)), 6))
        for j in range(len(cols))]
    return _meta("erfs_decile_shares", "fraction of total niveau de vie (published in % "
                 "with one decimal)", ERFS_FIELD, s, cols,
                 s.notes(s.find("ensemble")), data=d,
                 source="INSEE, ERFS séries longues 1996-2023, table DNV02",
                 concept=ERFS_UNIT_NOTE,
                 derived={"bottom50_share_derived": "d1+..+d5 (rounded inputs; prefer S50 "
                          "from erfs_indicators)"})


def _erfs_before(path):
    s = _sheet(read_xlsx(path), "IG5")
    h = s.find("Deciles de niveaux de vie avant")
    cols = _year_columns(s, h)
    spec = [("D1", ["(d1)"], False), ("D2", ["(d2)"], False), ("D3", ["(d3)"], False),
            ("D4", ["(d4)"], False), ("median", ["(d5)"], False), ("D6", ["(d6)"], False),
            ("D7", ["(d7)"], False), ("D8", ["(d8)"], False), ("D9", ["(d9)"], False),
            ("mean", ["moyenne"], False), ("D9_D1", ["(d9/d1)"], False)]
    d = _table(s, h, cols, spec)
    return _meta("erfs_before_redistribution",
                 "constant 2023 euros per consumption unit (niveau de vie before taxes and "
                 "social benefits; pensions and unemployment benefits included)",
                 ERFS_FIELD, s, cols, s.notes(s.find("(d9/d1)")), data=d,
                 source="INSEE, ERFS séries longues 1996-2023, table IG5",
                 concept=ERFS_UNIT_NOTE)


# --------------------------------------------------------------------------- wealth

HVP_FIELD = "France hors Mayotte, households in ordinary housing"


def _hvp_if371(path):
    sheets = read_xlsx(path)
    s = _sheet(sheets, "Tableau compl", "1")
    h = s.find("Indicateur", col=0, exact=True)
    cols = _year_columns(s, h)
    data, block = {}, None
    labels = {"immobilier": "housing", "financier": "financial",
              "professionnel": "business", "brut": "gross"}
    groups = {"les 50 %": "top50", "les 25 %": "top25", "les 10 %": "top10",
              "les 5 %": "top5", "les 1%": "top1"}
    gini = {}
    for i in range(h + 1, len(s.rows)):
        cells = s.cells(i)
        lab0 = _norm(cells.get(0, ""))
        if lab0.startswith("part de la masse de patrimoine"):
            block = next(v for k, v in labels.items() if "patrimoine " + k in lab0)
        elif lab0.startswith("indice de gini du patrimoine"):
            what = next(v for k, v in labels.items() if lab0.endswith(k))
            gini[what] = _row_values(s, i, cols)
            continue
        elif lab0:
            break
        lab1 = _norm(cells.get(1, ""))
        g = next((v for k, v in groups.items() if lab1.startswith(k)), None)
        if block and g:
            data["%s_%s_share" % (block, g)] = _row_values(s, i, cols, share=True)
    for comp in labels.values():
        top50 = data.get("%s_top50_share" % comp)
        if top50:
            data["%s_bottom50_share_derived" % comp] = [
                None if v is None else round(1 - v, 6) for v in top50]
    for k, v in gini.items():
        data["gini_" + k] = v
    if "gross_top10_share" not in data or "gross" not in gini:
        raise KeyError("IF371 TC1 layout changed")
    inequality = _meta("hvp_if371", "fraction of total gross wealth (published as whole "
                       "percent); Gini", HVP_FIELD, s, cols,
                       s.notes(s.find("indice de gini du patrimoine prof")), data=data,
                       source="INSEE, Insee Focus n° 371, Tableau complémentaire 1 "
                              "(Patrimoine 2014-2015, HVP 2017-2018, 2020-2021, 2023-2024)",
                       concept="household gross wealth (financial + housing + business + "
                               "residual); households ranked by the same component",
                       derived={"*_bottom50_share_derived": "1 - top50"})

    s2 = _sheet(sheets, "Tableau compl", "2")
    h2 = s2.find("Decile")
    yrow = s2.cells(h2 + 1)
    blocks = [(c, _norm(lab)) for c, lab in s2.cells(h2).items() if c >= 1]
    blocks.sort()
    names = [("D1", "1er decile"), ("D2", "2e decile"), ("D3", "3e decile"),
             ("D4", "4e decile"), ("median", "mediane"), ("D6", "6e decile"),
             ("D7", "7e decile"), ("D8", "8e decile"), ("D9", "9e decile"),
             ("P95", "95e centile"), ("P99", "99e centile")]
    th = {}
    for bi, (c0, blab) in enumerate(blocks):
        c1 = blocks[bi + 1][0] if bi + 1 < len(blocks) else max(yrow) + 1
        concept = ("gross" if "brut" in blab else "net") + "_" + (
            "current" if "courants" in blab else "const2024")
        bcols = [(c, str(yrow[c]), int(_num(yrow[c]))) for c in range(c0, c1) if c in yrow]
        for key, needle in names:
            i = s2.find(needle, col=0, start=h2 + 2)
            th.setdefault(concept, {"years": [y for _, _, y in bcols]})[key] = \
                _row_values(s2, i, bcols)
    years = th["gross_current"]["years"]
    if not all(v["years"] == years for v in th.values()):
        raise ValueError("IF371 TC2 years differ by block")
    thresholds = {"source": "INSEE, Insee Focus n° 371, Tableau complémentaire 2",
                  "years": years, "columns": [{"label": str(y), "year": y} for y in years],
                  "url": BASE + "8672665/IF371.xlsx", "page": PAGE + "8672665",
                  "file": "IF371.xlsx", "sheet": s2.name,
                  "unit": "euros per household (current, or constant 2024 euros)",
                  "field": HVP_FIELD, "data": th,
                  "breaks": s2.notes(s2.find("99e centile", col=0)),
                  "concept": "gross and net wealth thresholds; households ranked separately "
                             "by gross and by net wealth"}
    return inequality, thresholds


def _hvp_long(path):
    sheets = read_xlsx(path)

    def columns(s):
        h = s.find("Annuel", col=0)
        geo = s.cells(s.find("Geographie", col=0))
        comp = s.cells(s.find("Indicateur de comparabilite", col=0))
        cols = []
        for c, lab in sorted(s.cells(h).items()):
            if c == 0:
                continue
            y = int(_num(lab))
            g = "metro" if "metropolitaine" in _norm(geo[c]) else "hors_mayotte"
            m = "pre2010_method" if "anterieures" in _norm(comp[c]) else "post2010_method"
            cols.append((c, "%d %s %s" % (y, g, m), y))
        return h, cols

    s = _sheet(sheets, "MT_MOY_PATBRUT_HR")
    h, cols = columns(s)
    brackets = [("d1", "inferieur au 1er decile"), ("d2", "entre le 1er et le 2e"),
                ("d3", "entre le 2e et le 3e"), ("d4", "entre le 3e et le 4e"),
                ("d5", "entre le 4e et le 5e"), ("d6", "entre le 5e et le 6e"),
                ("d7", "entre le 6e et le 7e"), ("d8", "entre le 7e et le 8e"),
                ("d9", "entre le 8e et le 9e"), ("d10", "entre le 9e et le 10e"),
                ("p90p95", "entre le 9e decile et le 95e"), ("p95p99", "entre le 95e et le 99e"),
                ("p99p100", "superieur au 99e"), ("all", "total")]
    means = {"mean_" + k: _row_values(s, s.find(n, col=0, start=h + 1), cols)
             for k, n in brackets}

    def share(keys_weights, j):
        tot = means["mean_all"][j]
        vals = [means["mean_" + k][j] for k, _ in keys_weights]
        if tot is None or any(v is None for v in vals):
            return None
        return round(sum(v * w for v, (_, w) in zip(vals, keys_weights)) / tot, 4)

    derived = {
        "top10_share_derived": [share([("d10", 0.1)], j) for j in range(len(cols))],
        "top1_share_derived": [share([("p99p100", 0.01)], j) for j in range(len(cols))],
        "bottom50_share_derived": [share([("d%d" % k, 0.1) for k in range(1, 6)], j)
                                   for j in range(len(cols))],
    }
    sd = _sheet(sheets, "D_PATBRUT_HR")
    hd, colsd = columns(sd)
    dec = {}
    for k, n in [("D%d" % i, "decile_%d" % i) for i in range(1, 10)] + \
            [("P95", "centile_95"), ("P99", "centile_99")]:
        dec[k] = _row_values(sd, sd.find(n, col=0, start=hd + 1), colsd)
    sg = _sheet(sheets, "GINI")
    hg, colsg = columns(sg)
    gini = {"gini_gross_hors_reste": _row_values(sg, sg.find("brut hors reste", col=0,
                                                             start=hg + 1), colsg),
            "gini_gross": _row_values(sg, sg.find("indice de gini patrimoine brut", col=0,
                                                  start=hg + 2), colsg)}
    sc = _sheet(sheets, "COMP")
    hc, colsc = columns(sc)
    comp = {"mean_net_hors_reste": _row_values(sc, sc.find("patrimoine net hors reste",
                                                           col=0, start=hc + 1), colsc),
            "mean_debt": _row_values(sc, sc.find("endettement", col=0, start=hc + 1), colsc)}
    if not ([c[1] for c in cols] == [c[1] for c in colsd] == [c[1] for c in colsg] ==
            [c[1] for c in colsc]):
        raise ValueError("column layout differs across sheets")
    d = dict(means)
    d.update(dec)
    d.update(gini)
    d.update(comp)
    d.update(derived)
    return {"source": "INSEE, Patrimoine et endettement des ménages en 2021 et en séries "
                      "longues (enquêtes Patrimoine 1998-2015, HVP 2018, 2021)",
            "url": BASE + "8263048/hvp_series_longues_fr.xlsx", "page": PAGE + "8263048",
            "file": "hvp_series_longues_fr.xlsx", "sheet": "MT_MOY_PATBRUT_HR, D_PATBRUT_HR, "
            "GINI, COMP",
            "unit": "current euros per household; shares as fractions",
            "field": "households in ordinary housing; 'metro' = France métropolitaine, "
                     "'hors_mayotte' = France hors Mayotte",
            "concept": "gross wealth HORS RESTE (excludes residual assets: cars, durables, "
                       "jewellery, art); households ranked by it",
            "columns": [{"label": l, "year": y} for _, l, y in cols],
            "years": [y for _, _, y in cols], "data": d,
            "derived": {"top10_share_derived": "0.1 * mean(D9-D10) / mean(all)",
                        "top1_share_derived": "0.01 * mean(P99-P100) / mean(all)",
                        "bottom50_share_derived": "0.1 * sum(mean of tenths 1-5) / mean(all)"},
            "breaks": ["2010 appears twice: old method (comparable with 1998-2004) and new "
                       "method (comparable with 2015+); chain through 2010, never compare "
                       "across directly.",
                       "Residual assets measured differently since 2014-2015, hence 'hors "
                       "reste' for long comparisons.",
                       "Weights re-computed with the 2020-2021 method for 2010-2018; numbers "
                       "differ from earlier publications."] + sd.notes(sd.find("centile_99",
                                                                              col=0))}


def _hvp_net_by_gross(path):
    s = _sheet(read_xlsx(path), "PATBRUT")
    h = s.find("Montant moyen du patrimoine brut", col=1)
    hdr = s.cells(h)
    cg = next(c for c, v in hdr.items() if "moyen du patrimoine brut" in _norm(v))
    cn = next(c for c, v in hdr.items() if "moyen du patrimoine net" in _norm(v))
    brackets = [("d1", "inferieur au 1er", .1), ("d2", "entre le 1er et le 2e", .1),
                ("d3", "entre le 2e et le 3e", .1), ("d4", "entre le 3e et le 4e", .1),
                ("d5", "entre le 4e et le 5e", .1), ("d6", "entre le 5e et le 6e", .1),
                ("d7", "entre le 6e et le 7e", .1), ("d8", "entre le 7e et le 8e", .1),
                ("d9", "entre le 8e et le 9e", .1), ("p90p95", "entre le 9e decile et le 95e", .05),
                ("p95p99", "entre le 95e et le 99e", .04), ("p99p100", "superieur au 99e", .01),
                ("all", "total", 1.0)]
    gross, net = {}, {}
    for k, n, _ in brackets:
        i = s.find(n, col=0, start=h + 1)
        gross[k], net[k] = _clean(_num(s.cells(i)[cg])), _clean(_num(s.cells(i)[cn]))

    def sh(m, keys):
        return round(sum(m[k] * w for k, _, w in brackets if k in keys) / m["all"], 4)

    top10 = ("p90p95", "p95p99", "p99p100")
    bot50 = ("d1", "d2", "d3", "d4", "d5")
    return {"source": "INSEE, Patrimoine et endettement des ménages en 2021, tableau "
                      "'Montants moyen et médian de patrimoine brut et net', onglet PATBRUT "
                      "(HVP 2020-2021)",
            "url": BASE + "8262352/hvp_mtmoymed_patbrut_patnet_fr.xlsx",
            "page": PAGE + "8262352", "file": "hvp_mtmoymed_patbrut_patnet_fr.xlsx",
            "sheet": s.name, "unit": "euros per household; shares as fractions",
            "field": HVP_FIELD, "years": [2021],
            "concept": "households ranked by GROSS wealth; mean gross and mean net wealth "
                       "within each bracket",
            "data": {"mean_gross": gross, "mean_net": net,
                     "gross_top10_share_derived": sh(gross, top10),
                     "gross_top1_share_derived": sh(gross, ("p99p100",)),
                     "gross_bottom50_share_derived": sh(gross, bot50),
                     "net_top10_by_gross_share_derived": sh(net, top10),
                     "net_top1_by_gross_share_derived": sh(net, ("p99p100",)),
                     "net_bottom50_by_gross_share_derived": sh(net, bot50)},
            "derived": {"*_share_derived": "sum(bracket weight * bracket mean) / overall mean",
                        "net_*_by_gross_*": "net-wealth share of households ranked by GROSS "
                        "wealth: lower bound of the true top share of net wealth, upper "
                        "bound of the true bottom-50% share"},
            "breaks": []}


def _hvp_lorenz(path):
    s = _sheet(read_xlsx(path), "Figure 2")
    h = s.find("Part cumulee des menages", col=0)
    hdr = s.cells(h + 1)
    c = next(c for c, v in hdr.items() if "brut hors reste" in _norm(v))
    pts = {}
    for i in range(h + 2, len(s.rows)):
        x, y = _num(s.cells(i).get(0)), _num(s.cells(i).get(c))
        if x is None or y is None:
            break
        pts[round(x, 1)] = round(y / 100, 4)
    return {"source": "INSEE, Revenus et patrimoine des ménages 2024, vue d'ensemble "
                      "patrimoine, figure 2 (HVP 2020-2021)",
            "url": BASE + "7941439/RPM2024-VE2.xlsx", "page": PAGE + "7941439",
            "file": "RPM2024-VE2.xlsx", "sheet": s.name,
            "unit": "cumulative fraction of gross wealth hors reste held by the poorest x%",
            "field": "France hors Mayotte, households in ordinary housing",
            "years": [2021],
            "data": {"lorenz": {str(k): v for k, v in pts.items()},
                     "top10_share_derived": round(1 - pts[90.0], 4),
                     "top1_share_derived": round(1 - pts[99.0], 4),
                     "bottom50_share_derived": pts[50.0]},
            "derived": {"top10_share_derived": "1 - L(90)", "top1_share_derived": "1 - L(99)",
                        "bottom50_share_derived": "L(50)"},
            "breaks": []}


# --------------------------------------------------------------------------- CND

CND_FIELD = "France; all institutional sectors (net national income)"
CND_RANK = ("persons ranked by the USUAL niveau de vie (ERFS concept) of their household; "
            "amounts per consumption unit")


def _row_by_label(s, needle, cols, start=0):
    i = s.find(needle, col=0, start=start)
    return [_num(s.cells(i).get(c)) for c in cols]


def _cnd_2019(path):
    sheets = read_xlsx(path)
    s = _sheet(sheets, "Tableau compl", "2")
    h = s.find("Nature des revenus", col=0)
    vc = sorted(c for c in s.cells(h) if c >= 1)
    labels = [" ".join(str(s.cells(h)[c]).split()) for c in vc]
    rows = {"primary_extended_rnn_per_uc": "revenus primaires elargis (rnn)",
            "before_transfers_per_uc": "revenus avant transferts aux prix de base",
            "after_transfers_per_uc": "revenus apres transferts aux prix de base",
            "disposable_income_per_uc": "revenu disponible"}
    per_uc = {k: [_clean(v) for v in _row_by_label(s, n, vc, h + 1)] for k, n in rows.items()}
    net_uc = _row_by_label(s, "transferts nets, en euros par uc", vc, h + 1)
    net_bn = _row_by_label(s, "transferts nets, en milliards", vc, h + 1)
    uc_m = [round(b * 1e3 / u, 4) for b, u in zip(net_bn, net_uc)]  # millions of UC
    shares = {}
    for k, vals in per_uc.items():
        mass = [v * u for v, u in zip(vals, uc_m)]
        tot = sum(mass)
        name = k.replace("_per_uc", "")
        shares[name] = {"top5_share_derived": round(mass[19] / tot, 4),
                        "top10_share_derived": round(sum(mass[18:]) / tot, 4),
                        "bottom50_share_derived": round(sum(mass[:10]) / tot, 4),
                        "total_bn_derived": round(tot / 1e3, 1)}
    t = _sheet(sheets, "Tableau compl", "1")
    ht = t.find("Nature des revenus", col=0)
    ind = {}
    for key, needle in [("primary_extended_rnn", "revenus primaires elargis (rnn)"),
                        ("before_transfers", "revenu avant transferts"),
                        ("after_transfers", "revenus apres transferts"),
                        ("disposable_income", "revenu disponible")]:
        cells = t.cells(t.find(needle, col=0, start=ht + 1))
        ind[key] = {"pseudo_gini": _clean(_num(cells.get(2))), "palma": _clean(_num(cells.get(5))),
                    "S80_S20_ratio": _clean(_num(cells.get(6)))}
    f1 = _sheet(sheets, "Figure 1")
    tot_bn = _num(f1.cells(f1.find("revenus avant transferts aux prix de base", col=0))[1])
    tot_uc = _num(f1.cells(f1.find("revenus avant transferts aux prix de base", col=0))[2])
    return {"source": "INSEE, Insee Analyses n° 88 (André, Germain, Sicsic 2023), comptes "
                      "nationaux distribués 2019",
            "url": BASE + "7669723/IA88.xlsx", "page": PAGE + "7669723", "file": "IA88.xlsx",
            "sheet": "Tableau complémentaire 1, Tableau complémentaire 2, Figure 1",
            "unit": "euros per consumption unit; shares as fractions", "field": CND_FIELD,
            "concept": CND_RANK + ". Before transfers excludes pensions and unemployment "
                       "benefits (treated as transfers); after transfers includes in-kind "
                       "transfers (health, education, housing...) and collective spending.",
            "years": [2019], "columns": [{"label": l, "year": 2019} for l in labels],
            "data": {"per_uc": per_uc, "uc_millions_derived": uc_m,
                     "shares": shares, "published_indicators": ind,
                     "check_total_before_transfers_bn": tot_bn,
                     "check_total_uc_millions_derived": round(tot_bn * 1e3 / tot_uc, 3)},
            "derived": {"uc_millions_derived": "net transfers (bn) / net transfers (EUR per UC)",
                        "shares": "per-UC mean x UC count of each twentieth / sum"},
            "breaks": ["Pseudo-Gini, Palma and S80/S20 are computed with persons ranked by "
                       "usual niveau de vie (no re-ranking)."]}


def _cnd_masses(s, h, rows, start=None, extra_header=None):
    """Masses by group; column labels from row h (plus row extra_header, e.g. a
    two-row header whose 'Ensemble' sits on the first row)."""
    hdr = dict(s.cells(extra_header)) if extra_header is not None else {}
    hdr.update(s.cells(h))
    cols = sorted(c for c in hdr if c >= 1)
    labels = [" ".join(str(hdr[c]).split()) for c in cols]
    out = {}
    for k, n in rows.items():
        out[k] = [_clean(v) for v in _row_by_label(s, n, cols, h + 1 if start is None else start)]
    return labels, out


def _shares_from_masses(masses, labels):
    """masses: list incl. a final 'Ensemble' column."""
    groups, total = masses[:-1], masses[-1]
    n = len(groups)
    res = {"sum_of_groups_bn": round(sum(groups), 1), "published_total_bn": total,
           "group_shares": [round(g / total, 4) for g in groups],
           "top10_share_derived": round(sum(groups[-(n // 10):]) / total, 4),
           "bottom50_share_derived": round(sum(groups[:n // 2]) / total, 4)}
    if n == 20:
        res["top5_share_derived"] = round(groups[-1] / total, 4)
    return res


def _cnd_2022(path):
    sheets = read_xlsx(path)
    s = _sheet(sheets, "Figure 2")
    h = s.find("Nature des revenus", col=0)
    rows = {"primary_extended_bn": "revenu primaire elargi (avant transferts)",
            "extended_niveau_de_vie_bn": "niveau de vie elargi (apres transferts)"}
    labels, m = _cnd_masses(s, h, rows)
    t = _sheet(sheets, "Tableau compl")
    ht = t.find("Nature des revenus", col=0) + 1
    rows_v = {"primary_extended_bn": "rnn avant transferts",
              "extended_niveau_de_vie_bn": "rnn apres transferts",
              "disposable_income_bn": "revenu disponible"}
    labels_v, mv = _cnd_masses(t, ht, rows_v, start=ht + 1, extra_header=ht - 1)
    if len(labels_v) != 21 or "ensemble" not in _norm(labels_v[-1]):
        raise KeyError("ip2022 twentieths header changed: %r" % labels_v)
    return {"source": "INSEE, Insee Première n° 2022, Comptes nationaux par catégories de "
                      "ménages en 2022 (CND 2022, base 2020)",
            "url": BASE + "8275760/ip2022.xlsx", "page": PAGE + "8275760", "file": "ip2022.xlsx",
            "sheet": "Figure 2, Tableau complémentaire", "unit": "billions of euros; shares "
            "as fractions", "field": CND_FIELD, "concept": CND_RANK, "years": [2022],
            "data": {"deciles": {"columns": labels, "masses": m,
                                 "shares": {k: _shares_from_masses(v, labels)
                                            for k, v in m.items()}},
                     "twentieths": {"columns": labels_v, "masses": mv,
                                    "shares": {k: _shares_from_masses(v, labels_v)
                                               for k, v in mv.items()}}},
            "derived": {"shares": "group mass / published total"},
            "breaks": ["Primary income at market prices in the twentieths table; ranking by "
                       "usual niveau de vie."]}


def _cnd_2023(path):
    sheets = read_xlsx(path)
    s = _sheet(sheets, "Figure 2b")
    h = s.find("Nature des revenus", col=0)
    rows = {"primary_extended_bn": "revenu primaire elargi (avant transferts publics)",
            "extended_niveau_de_vie_bn": "niveau de vie elargi (apres transferts publics)",
            "extended_net_of_debt_bn": "niveau de vie elargi net de l'endettement"}
    labels, m = _cnd_masses(s, h, rows)
    t = _sheet(sheets, "Figure 3a")
    ht = t.find("Nature des revenus", col=0)
    ind = {}
    for key, needle in [("primary_extended", "revenus primaires elargis"),
                        ("extended_niveau_de_vie", "niveaux de vie elargis")]:
        cells = t.cells(t.find(needle, col=0, start=ht + 1))
        ind[key] = {"pseudo_gini": _clean(_num(cells.get(2))), "palma": _clean(_num(cells.get(5))),
                    "S80_S20_ratio": _clean(_num(cells.get(6)))}
    return {"source": "INSEE, Insee Analyses n° 118, Revenus des ménages élargis à "
                      "l'ensemble de l'économie en 2023 (CND 2023 semi-définitif, base 2020)",
            "url": BASE + "8974371/IA118.xlsx", "page": PAGE + "8974371", "file": "IA118.xlsx",
            "sheet": "Figure 2b, Figure 3a", "unit": "billions of euros; shares as fractions",
            "field": CND_FIELD, "concept": CND_RANK, "years": [2023],
            "data": {"deciles": {"columns": labels, "masses": m,
                                 "shares": {k: _shares_from_masses(v, labels)
                                            for k, v in m.items()}},
                     "published_indicators": ind},
            "derived": {"shares": "group mass / published total"},
            "breaks": ["New conventions vs 2019/2022 vintages: primary income of general "
                       "government at basic prices; national public redistribution balance "
                       "(deficit) shown separately ('net of debt' row). Not spliceable."]}


# --------------------------------------------------------------------------- entry points

PARSERS = [
    ("erfs_indicators", _erfs_indicators), ("erfs_deciles", _erfs_deciles),
    ("erfs_ig1", _erfs_ig1), ("erfs_vingtiles", _erfs_vingtiles),
    ("erfs_mean_by_decile", _erfs_mean_by_decile), ("erfs_decile_shares", _erfs_decile_shares),
    ("erfs_before_redistribution", _erfs_before),
    ("hvp_if371", _hvp_if371), ("hvp_long_series", _hvp_long),
    ("hvp_net_by_gross_2021", _hvp_net_by_gross), ("hvp_lorenz_2021", _hvp_lorenz),
    ("cnd_2019", _cnd_2019), ("cnd_2022", _cnd_2022), ("cnd_2023", _cnd_2023),
]


def _checks(out):
    """Consistency checks between tables; returns list of strings (empty = all good)."""
    problems = []

    def col(t, label):
        return [c["label"] for c in out[t]["columns"]].index(label)

    if "erfs_indicators" in out and "erfs_ig1" in out:
        a, b = out["erfs_indicators"]["data"], out["erfs_ig1"]["data"]
        ia, ib = col("erfs_indicators", "2023"), col("erfs_ig1", "2023")
        for k in ("S20_share", "S50_share", "S90_share", "D9_D1", "S80_S20_ratio"):
            if a[k][ia] != b[k][ib]:
                problems.append("2023 %s: 1975-2024 table %s vs IG1 %s" % (k, a[k][ia], b[k][ib]))
        if abs(round(b["gini"][ib], 3) - a["gini"][ia]) > 0.0005:
            problems.append("2023 Gini mismatch")
    if "erfs_decile_shares" in out:
        d = out["erfs_decile_shares"]["data"]
        for j, c in enumerate(out["erfs_decile_shares"]["columns"]):
            s = sum(d["d%d_share" % k][j] for k in range(1, 11))
            if abs(s - 1) > 0.003:
                problems.append("DNV02 %s deciles sum to %.3f" % (c["label"], s))
    if "cnd_2019" in out:
        d = out["cnd_2019"]["data"]
        tot = sum(d["uc_millions_derived"])
        if abs(tot - d["check_total_uc_millions_derived"]) > 0.5:
            problems.append("CND 2019 UC sum %.2f vs %.2f" % (tot, d["check_total_uc_millions_derived"]))
        bt = d["shares"]["before_transfers"]["total_bn_derived"]
        if abs(bt - d["check_total_before_transfers_bn"]) > 5:
            problems.append("CND 2019 before-transfers total %s vs %s" % (bt, d["check_total_before_transfers_bn"]))
    for t in ("cnd_2022", "cnd_2023"):
        if t in out:
            for part in ("deciles", "twentieths"):
                for k, v in out[t]["data"].get(part, {}).get("shares", {}).items():
                    if abs(v["sum_of_groups_bn"] - v["published_total_bn"]) > 1:
                        problems.append("%s %s %s: groups sum %s vs total %s" % (
                            t, part, k, v["sum_of_groups_bn"], v["published_total_bn"]))
    if "hvp_long_series" in out and "hvp_lorenz_2021" in out:
        ls = out["hvp_long_series"]
        j = [c["label"] for c in ls["columns"]].index("2021 hors_mayotte post2010_method")
        a = ls["data"]["top10_share_derived"][j]
        b = out["hvp_lorenz_2021"]["data"]["top10_share_derived"]
        if abs(a - b) > 0.01:
            problems.append("2021 top10 gross hors reste: long series %s vs Lorenz %s" % (a, b))
    return problems


def load(raw_dir):
    d = _dir(raw_dir)
    out, missing = {}, {}
    for key, parser in PARSERS:
        page, name = FILES[key]
        path = d / name
        if not path.exists():
            missing[key] = "file not found: %s" % path
            continue
        try:
            res = parser(path)
        except Exception as exc:
            missing[key] = "parse error: %r" % (exc,)
            continue
        sha = _sha(path)
        if key == "hvp_if371":
            out["hvp_inequality"], out["hvp_thresholds"] = res
            out["hvp_inequality"]["sha256"] = out["hvp_thresholds"]["sha256"] = sha
        else:
            res["sha256"] = sha
            out[key] = res
    out["_missing"] = missing
    out["_checks"] = _checks(out)
    return out


def _summary(data):
    def at(t, key, label):
        tb = data[t]
        j = [c["label"] for c in tb["columns"]].index(label)
        return tb["data"][key][j]

    lines = []
    for k, v in data.items():
        if k.startswith("_"):
            continue
        cols = v.get("columns")
        span = ("%s .. %s (%d columns)" % (cols[0]["label"], cols[-1]["label"], len(cols))
                if cols else ", ".join(map(str, v.get("years", []))))
        lines.append("%-28s %s" % (k, span))
    if "erfs_indicators" in data:
        e = data["erfs_indicators"]
        last = e["columns"][-1]["label"]
        lines.append("ERFS %s: top10 %.3f  bottom50 %.3f  D9/D1 %s  Gini %s" % (
            last, at("erfs_indicators", "top10_share_derived", last),
            at("erfs_indicators", "S50_share", last), at("erfs_indicators", "D9_D1", last),
            at("erfs_indicators", "gini", last)))
    if "hvp_inequality" in data:
        h = data["hvp_inequality"]
        lines.append("HVP %s gross wealth: top10 %s  top1 %s  bottom50 %s" % (
            h["columns"][-1]["label"], h["data"]["gross_top10_share"][-1],
            h["data"]["gross_top1_share"][-1], h["data"]["gross_bottom50_share_derived"][-1]))
    if "cnd_2019" in data:
        s = data["cnd_2019"]["data"]["shares"]["after_transfers"]
        lines.append("CND 2019 after transfers (ranked by usual niveau de vie): top10 %s "
                     "bottom50 %s" % (s["top10_share_derived"], s["bottom50_share_derived"]))
    lines.append("missing: %s" % (data["_missing"] or "none"))
    lines.append("checks: %s" % (data["_checks"] or "all passed"))
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python3 -I pipeline/sources/insee.py <raw_dir>")
    errs = fetch(sys.argv[1])
    result = load(sys.argv[1])
    if errs:
        result["_fetch_errors"] = errs
    json.dumps(result)  # must be JSON-serializable
    print(_summary(result))
