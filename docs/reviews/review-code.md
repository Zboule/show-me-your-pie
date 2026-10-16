# Code review: pipeline, site, reproducibility (2026-10-16)

Scope: `pipeline/` (fetch, build_data, top_tail, sources/*, tests), `site/index.html`, `README.md`.
Method: I read every file in scope. I reproduced the README in a fresh copy that had no `data/raw`
(scratchpad `codereview/`, Python 3.9.6, macOS). I ran failure-injection and mutation tests, and I drove
the page in Playwright. No project file outside `docs/reviews/` was modified.

## Summary

The happy path reproduces. In a clean copy, `fetch.py` took 33 s, `build_data.py` took 2.5 s and the
14 tests passed. The rebuilt `france.json` is identical to the committed one in every value. The one
difference is the recorded `inputs_sha256` of `insee_hpi.xml`; see M3.

The problems are elsewhere:

- The build depends on the directory layout and on the current working directory. In one case it
  degrades silently; in another it crashes.
- Upstream failures are swallowed and then surface as an unrelated `KeyError`.
- The test suite is mostly tautological. It caught **none of three injected bugs**.
- On the front end there is no doctype and no viewport meta. The CPI option has a 6.4% step at 1950.
  Several prose claims no longer match the data or the code.

---

## Critical

### C1. Two inconsistent "manual dir" mechanisms. Outside `data/` the build crashes; from another cwd it silently drops the rich lists, the scenarios and IPP.

- `pipeline/build_data.py:367`: `main(raw_dir, out_path, manual_dir="data/manual")`. This path is
  relative to the **cwd**.
- `pipeline/sources/prices.py:455` and `pipeline/sources/housing.py:252`: when no manual dir is
  given, they use `Path(raw_dir).resolve().parent / "manual"`. This path is relative to **raw_dir**.
- `build_data.load_crosschecks` (`build_data.py:224`) calls `module.load(raw_dir)` and never
  passes the manual dir.

Evidence:

```
# raw dir outside data/ (manual dir given explicitly and correct):
$ python3 -I pipeline/build_data.py ../alt/rawdata ../alt/out.json data/manual
  File ".../build_data.py", line 303, in build_purchasing
    "paris_flat_eur_m2": series(housing, "notaires_paris_apartments_eur_m2"),
KeyError: 'notaires_paris_apartments_eur_m2'          -> exit 1

# run from pipeline/ without the 3rd argument (exit 0, no warning):
$ cd pipeline && python3 -I build_data.py ../data/raw out.json
wrote out.json (405 KB)
  -> rich_lists {}, ipp_top_income None, hweal.scenarios.years []
```

In the second case the tests still pass on the degraded file, because the scenario tests loop over
an empty list. The page then shows "changes 0 years (undefined–undefined)" in scenario mode, and
the IPP section is blank.

Fix:

- Resolve `manual_dir` against the repository root:
  `Path(__file__).resolve().parents[1] / "data" / "manual"`.
- Pass it explicitly to every `module.load(raw_dir, manual_dir)`.
- Make the absence of any expected manual file a hard error, or require an explicit `--allow-missing`
  flag.

### C2. A failed or partial upstream fetch is swallowed and then crashes the build far from the cause

- `pipeline/sources/insee.py:189`: `fetch` catches every `Exception` per file and returns an
  `errors` dict.
- `pipeline/fetch.py:67-69` ignores that return value. It prints
  `fetched cross-check source insee` and exits 0.
- `insee.load` (`insee.py:983`) also turns parse errors into `_missing`.
- `build_comparison` (`build_data.py:336, 360`) then indexes `insee["hvp_inequality"]` and
  `insee["cnd_2019"]` unconditionally.

Evidence: one INSEE xlsx replaced with junk.

```
  File ".../build_data.py", line 336, in build_comparison
    hvp = insee["hvp_inequality"]
KeyError: 'hvp_inequality'
```

A stale file from an earlier run also stays in place and is reused silently when a re-download fails.

The other direction fails silently too. If a whole source folder is missing (I deleted
`data/raw/dwa`), the build prints `skipped dwa` and succeeds. The DWA line just disappears from the
cross-check charts.

The internal consistency checks are computed and thrown away. `insee.load()["_checks"]` and
`["_missing"]` never reach the output or the console. They are both empty today, which I verified,
but nobody would notice when they stop being empty.

Fix:

- `fetch.py` should fail with a non-zero exit when any source returns errors.
- `build_data` should raise when a loaded source has a non-empty `_missing` or `_checks`.
- Add a `--partial` flag only if degraded builds are really wanted.
- Write `meta.sources_loaded` and `meta.checks` into the JSON.

### C3. The test suite cannot detect real bugs: three injected mutations all pass

I applied these mutations to a scratch copy:

1. `build_data.py:207`: scenario uses the **previous year's** mean and adult count, and the rich list
   is multiplied by 3.
2. `build_data.py:322`: the comparison `wealth_top10` uses WID `p99p100` instead of `p90p100`.
3. `top_tail.py:56`: `alpha = b` instead of `b / (b - 1)`.

```
$ python3 -I pipeline/build_data.py ... && python3 -m unittest discover -s pipeline/tests
Ran 14 tests in 0.002s
OK
```

Why each test misses them (`pipeline/tests/test_build.py`):

- **`test_shares_sum_to_one_every_year` (l.27) and the `assert` at `build_data.py:122` are
  tautologies.** Differencing telescopes: Σ(top(a) − top(b)) = top(0) = 1 for any input.
- **`test_layer_averages_rebuild_the_mean` (l.33) is a tautology too.** avg = share·mean/width,
  so Σ avg·width = mean by construction.
- **`test_pareto_inside_top_bin` (l.102) uses b = 2.** That is the only value where b/(b−1) = b,
  so it cannot see mutation 3.
- **`test_correction_preserves_total_and_hits_the_list` (l.118) never checks that the top hits the
  list.** It asserts `out[1] > top_share`. The expected value, 2 × 0.05 = 0.10, is never checked.
- **No test recomputes anything from inputs.** Year alignment, deflation, rich-list conversion and
  comparison wiring are all untested.
- **`g_percentiles_match_group_average` checks 2024 only.**
- **`DATA = json.loads(...)` runs at import (l.16).** A missing JSON therefore also kills the pure
  `top_tail` unit tests.

Proposed tests:

- **Pareto with a closed form at other parameters.**
  `half/full == 0.5 ** (1 - 1/alpha)` for b = 1.5 (α = 3) and b = 3 (α = 1.5).
- **Exact hit.** In the two-layer toy, `out[1] == rl_adj / total` (0.10) to 1e-9, and
  `out[0] == (total - rl_adj) / total`.
- **Straddling.** n_pct inside the second layer; check that the straddling layer equals
  `listed·ratio + (wealth − listed)·scale` against a hand calculation.
- **Oracle from the method doc.** `docs/03-method.md` §3.7 scenario table, "Top 0.001% share, 2024":
  assert the JSON scenario values match it within rounding. It also asserts `corrected_years["spread"] == []`.
- **Independent check of the differencing.** WID publishes `s…p50p90` directly; assert
  |derived middle 40% − published| < 2e-4 every year. Today the maximum is 1.0e-4.
- **Wiring.** `comparison.wealth_top10[source startswith WID].values == concepts.hweal.share.p90p100`.
  Do the same for each WID comparison series.
- **Deflation.** `rich_lists` → scenario conversion equals `total_eur_bn·1e9/deflator[y]` for one
  pinned year.
- **Builder unit tests on a tiny synthetic WID CSV.** Build them in a temporary directory, run
  `main()`, and assert every concept, layer and year with hand values. This also covers C1 and C2.
- **Load the JSON lazily** in `setUpClass`, and skip dataset tests with a clear message when it is
  missing.
- **Run the JSON through a strict parser**, e.g. `json.loads(text, parse_constant=raise)`; see M4.

---

## Major

### M1. No doctype, no viewport meta, no `lang`. The page renders in quirks mode, and on phones as a zoomed-out ~980px desktop page.

`site/index.html:1-6` starts with `<meta charset>`. There is no `<!doctype html>`, no `<html lang>` and
no `<meta name="viewport">`. `claude:viewport-fit-sides` means nothing on GitHub Pages.

Playwright: `document.compatMode === "BackCompat"`, `viewport: false`, `lang: ""`.

Without a viewport meta, a real phone lays the page out at about 980 CSS px. The
`@media (max-width:560px)` rules therefore never fire: no narrow bar chart, no static filter row. Text
renders tiny. Note that my 390px desktop-viewport check cannot show this, because a desktop viewport
ignores the meta.

Fix:

```html
<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
```

Re-test the table and line-height styling after leaving quirks mode.

### M2. The CPI price option creates a 6.4% step at 1950 and biases any growth computed across 1950

`site/index.html:330-334`: `priceFactor(y)` returns 1 for `y < 1950`, and
`deflator_wid(y)/cpi(y) ≈ 1.064` from 1950 to 1989. The data:

```
1949 factor 1.0642 (but forced to 1), 1950 1.0644, 1970 1.0881, 1990 1.0578, 2000 1.0136, 2024 0.9977
bottom-50% wealth avg: 1949 = 1023, 1950 = 1086 (WID prices) -> 1156 in CPI mode
```

The jump is visible in the levels chart. The transfer table's "real growth / yr" and the GIC
(`index.html:686`) mix two deflators whenever the start year is before 1950.

Fix: for `y < 1950`, use the 1950 factor. That chains WID's deflator onto the CPI at 1950, so
`f(y) = f(1950)`. Also say in the method text what "CPI" means pre-1990: INSEE's long coefficient,
rescaled at 1990.

### M3. Provenance is mostly not recorded, and the bulk WID file is a moving target

- **Most inputs are not hashed.** `inputs_sha256` (`build_data.py:385-389`) uses a non-recursive
  `raw.glob("*")`. No DWA, INSEE, prices or housing file is hashed. It does hash
  `WID_metadata_FR.csv`, which is never read.
- **The SDMX hash changes on every fetch.** The response header carries
  `<message:Prepared>2026-10-16T19:37:51</message:Prepared>` and a fresh `message:ID`, so
  `insee_hpi.xml` gets a new hash each time even though the data is identical. That was the only
  difference in my clean rebuild.
- **The WID zip is overwritten in place, with no version recorded.** Nobody can rebuild a past
  `france.json`. `HttpRangeFile` (`fetch.py:25-55`) also does not pin an ETag. If WID republishes
  during the ~70 range reads, the file assembled is a silent mix of two versions.
- **DVF and INSEE are moving targets too.** `stats_dvf.csv` is a rolling 5-year window on an OVH
  bucket, so the anchor year of the "rest of France" back-cast moves every refresh. INSEE files carry
  vintage-specific names (see m1).

Fix:

- Hash recursively.
- For SDMX, hash the parsed `(series, period, value)` tuples, or strip the header first.
- Record the WID zip's `ETag` and `Last-Modified`, and send `If-Range`.
- Optionally archive raw inputs (e.g. a Zenodo deposit or a release asset) and document the vintage
  in `meta`.

### M4. Latent invalid JSON: NaN would make the whole page fail to load

`build_data.py:265` substitutes `float("nan")` for a missing IPP group. `json.dumps` writes
`allow_nan=True` by default (`build_data.py:408`), so the file would contain `NaN`. Browsers'
`JSON.parse` rejects that, and the page would show only "The data file could not be loaded".

Today's data has no NaN; I checked with `grep -c NaN` → 0. The next CSV edit could change that.

Fix: use `None`, and call `json.dumps(out, separators=..., allow_nan=False)`.

### M5. Fetch is not robust: no timeouts, no retries, no status checks, non-atomic writes

- **No timeouts.** `fetch.py:30, 52, 65`: none of the `urlopen` calls has a `timeout`, so a stalled
  connection hangs forever.
- **No retry.** This matters for about 70 sequential range requests plus a ~280 MB DVF stream.
- **No 206 check.** `readinto` (`fetch.py:47-55`) never checks for status `206` or `Content-Range`.
  A server or proxy that answers `200` would send the whole 900 MB per read. That would end in a
  `ValueError` on `buf[:len(data)] = data`, or in silently wrong bytes.
- **Writes go straight to final paths.** `fetch.py:63,65`, `prices.py:151` and `housing.py:101,105`
  write directly. An interrupted DVF stream leaves a truncated CSV that `load()` accepts. The
  `kept < 1000` check runs after the file is already written.
- **Validation uses `assert`.** There are 28 `assert`s for data validation in `pipeline/`, and
  `python -O` strips them.

Fix:

- Add one `_get(url, retries=3, timeout=60)` helper with exponential backoff, shared by all modules.
- Check `resp.status == 206` and the `Content-Range` total.
- Write to `*.part` and then `os.replace`.
- Replace data asserts with `raise ValueError(...)`.

### M6. Smoothing does less than it claims and mixes non-adjacent years

`site/index.html:357-364`:

- **The end year is never averaged, because the window needs 3 values.** In the default
  1980 → latest view, the "3-year average" therefore does not touch the endpoint. That is exactly
  where the Forbes-driven jumps (2014, 2021) sit, so the robustness option does not do its job there.
- **The window is index-based, not year-based.** `hweal` years have gaps (1900, 1902, 1905, 1907,
  1909…) and `ptinc` jumps 1900 → 1910 → 1915, so 1910 is averaged with 1900 and 1915.
- **Scenario years are mixed with WID years.** The overrides only cover some years: for "upper",
  1996, 1999 and 2003 are uncorrected. Smoothing then averages WID and scenario values together.

Fix:

- Average over years `y-1..y+1` that actually exist.
- For the endpoint, use a trailing average or say plainly that it is unsmoothed.
- In the summary line, say how many points the end year used.

### M7. Prose and method text contradict the code or the data

- **The method list says "We do not adjust further" (`index.html:259`).** The page has a scenario
  selector that does adjust the top.
- **Housing is described one way and computed another.** Method item 7 (`index.html:260`) and
  `docs/03-method.md` §3.8 describe an HPI index over **post-tax** income, normalised to 1996 = 100.
  The code computes years of **pre-tax** income for a 70 m² flat from Notaires/DVF price levels
  (`index.html:743-756`). `docs/03-method.md` §3.8c contradicts §3.8.
- **`D.hpi` is shipped but never used.**
- **"5–7 points" is wrong in four years.** `cc-notes` (`index.html:812`) says "WID puts 5–7 points
  more in the top 5% than the ECB accounts in every year since 2009". Data: 2010 = 7.6, 2011 = 7.3,
  2018 = 7.2, 2022 = 7.5.
- **"Within about one to two points" is wrong in 1996.** For WID versus ERFS top 10%, 1996 is
  25.7% vs 22.2–22.5%, a gap of 3.2–3.5 points.
- **Hard-coded values will go stale with the next vintage.** Examples: "constant 2025 euros" (hero,
  levels, top, table notes), "about 530 people", "2025 DVF transaction average" (the anchor is
  computed in `housing._backcast`), the fixed `1998, 2024` in the prices note (`index.html:766`), and
  `xDomain: [from, 2025]` in the cross-checks (`index.html:810`), which will clip 2026 data.
- **`docs/03-method.md` line 34 still lists CPI as a "planned extension".** It is implemented.

Fix:

- Generate the numbers in the prose from `D`, as is already done for the summaries.
- Rewrite method item 6 to describe the scenarios.
- Reconcile §3.8 with §3.8c and with the code.
- Drop `hpi` from the JSON, or use it.

### M8. Licensing and publishing hygiene

- **There is no LICENSE file for the code.**
- **`france.json` re-publishes third-party data:**
  - WID series;
  - INSEE-derived series;
  - ECB DWA;
  - DVF aggregates;
  - the Notaires quarterly price table (transcribed from a Paris Notaires Services PDF);
  - every row of the Challenges and Forbes lists (`rich_lists` is copied wholesale, including notes
    and source URLs).
- **I did not check any producer's licence terms**, so this review states none from memory. Record
  each producer's actual terms (URL and date) in `docs/02-data-france.md`, and put an attribution
  line per source in the page footer.
- **Verify before publishing** these items:
  - the Notaires table, which comes from a commercial data producer;
  - the Forbes figures, which come from `forbes.com/forbesapi/...` JSON endpoints (see `source_url`
    in `forbes_france_billionaires.csv`); check the site's terms on automated access;
  - the Challenges figures, which are press content. Consider shipping only the per-year totals.
- **Clean up the working tree.** It holds `.playwright-mcp/` (screenshots and console logs, 780 KB).
  It is in `.gitignore`, but the folder is not yet a git repository, so check `git status` after
  `git init`.
- **No secrets found** (grep for key, token, secret, password and local paths).
- **Third-party request on every visit.** Google Fonts loads from fonts.googleapis.com, which sends
  visitors' IPs to Google (a GDPR point raised in German case law). Consider self-hosting the two
  fonts.

---

## Minor

### Code and pipeline

- **m1. Vintage-specific names and URLs** will 404 or go stale on the next edition:
  - `insee.py:137-153`: `irsocerfs2023_*`, page ids `8731524`, `8672665`, `8974371`;
  - `prices.py:120-121`: `8988851/t_2103_fr.xlsx` (the docstring itself says the page id changes);
  - `housing.py:86`: `..._5.pdf`.

  Put them in one `VINTAGES` table with a "last checked" date, and fail loudly with the page URL to
  update.
- **m2. `top_tail.top_n_wealth` (`top_tail.py:39-63`) has unguarded edge cases:**

  | Input | Result |
  |---|---|
  | `n_share` larger than the bins provided | silently truncates: 0.011 returns the same as 0.01 |
  | avg/threshold = 1 | `ZeroDivisionError` |
  | avg/threshold = 0.99 | α = −99, a plausible-looking wrong number |
  | negative threshold | the top half holds **more** than the whole bin (0.2035 > 0.2) |
  | bins not sorted top-down | silently wrong (0.025 vs 0.141) |

  Current data is safe: 1996–2024 has b between 1.68 and 1.93, and the spread scenario's n reaches
  0.0112% (in 1997) against a 0.1% bin range. But 1975 has b = 1.04, so a future vintage could hit
  the edge.

  Fix: assert sorted bins, `n_share <= sum(widths)`, and `b > 1`, and raise otherwise.
- **m3. Layer shares are differences of WID shares rounded to 4 decimals.** Each layer carries up to
  ±1e-4 of rounding error, about ±0.5% of the top-0.01–0.001% layer. That is roughly ±€1.5 bn in
  transfers, or ±€3 M per adult in the top 0.001%. The g-percentile averages, which are published at
  full precision, agree within 0.5% for wealth and 1.6% for pre-tax income (1982).

  Option: derive layer shares from the `a…` g-percentile averages, and use the shares only as a
  check.
- **m4. `scenario_shares` with inconsistent inputs.** `listed = w_n - above` (`top_tail.py:88`) mixes
  g-percentile-based `w_n` with share-based `above`. Totals are always preserved, but the straddling
  layer can absorb the inconsistency.

  Fix: compute both from the same source.
- **m5. The "spread" scenario is computed but dead.** It is the GGP default (k = 10, c = 20%). It
  corrects 0 years, and the page does not offer it (`index.html:150-154`). Either expose it, so
  readers see that the default assumption changes nothing, or drop it.
- **m6. `build_scenarios` falls back to `shares` when there is no correction (`build_data.py:210`).**
  If a layer share is None, `round(None)` raises. Missing g-percentile bins or adult counts for a
  year that has a Challenges row raise a bare `KeyError`.
- **m7. Missing encodings.** `build_data.py:54, 65, 80, 250` call `open()`/`read_text()` without
  `encoding=`, which breaks under non-UTF-8 locales such as Windows cp1252. `build_data.py:250` also
  leaves its file handle open.
- **m8. DWA `load` (`dwa.py:174-181`) does arithmetic on `col()` results that can be None.** A missing
  Q4 for one series raises `TypeError`. `hh_q` indexes quarters filtered by `q in nh`, but
  `frozen_from` reads `quarters[k+1]` from the unfiltered list, so the indices can misalign.
- **m9. Concept mixing in the comparison.** The INSEE wealth-survey line in the comparison
  (`build_data.py:338-345`) joins two concepts under one legend entry: "hors reste" (long series)
  and gross wealth including residual assets (IF371). It is split by a None, but the labels do not
  say so. The ERFS old-concept columns (1975–1996, no financial income) are drawn with the same
  colour and label as the current series.
- **m10. INSEE HPI 010567059 is fetched twice**, by `fetch.py` and by `housing.py`. Only the unused
  `hpi` field consumes the first copy.
- **m11. README.**
  - "Requires Python 3" should say ≥ 3.8; nothing newer is used, and 3.9.6 is verified.
  - It should state disk use: 73 MB in `data/raw`, of which the WID CSV is 69 MB uncompressed.
  - It should say that tests read the built JSON, so the build must run first.
  - It should explain that `file://` will not work. The error message ("Run the pipeline")
    misleads a user who opened `index.html` directly.
- **m12. JSON size is 439 KB.** 375 KB of it is the 127 g-percentile arrays (125 KB per concept).
  That is acceptable over gzip. Rounding the g-percentile averages to 3 significant figures, or
  shipping only `hweal`/`ptinc`, would halve it.

### Front end

- **m13. Duplicate-year tooltips show the pre-break value only.** `lineChart` hover uses
  `s.xs.indexOf(best)` (`index.html:491`), so ERFS points at 1996, 2010, 2012 and 2020 (each
  appears twice) show the first, old-method value. The `allX` Set also merges them.

  Fix: collect every index `j` with `xs[j] === best` and show both, labelled "(old)" and "(new)".
- **m14. Reversed year ranges are accepted.** The `from`/`to` change handlers (`index.html:836-837`)
  do not validate the order. From = 2024, To = 1980 renders: "Between 2024 and 1980, €396 bn …
  measured against the 2024 split…". Only the GIC guards against it.

  Fix: disable the invalid options, or swap the two values.
- **m15. Clicking the word "Measure" switches the concept to Net wealth.** The `<label>` at
  `index.html:141` wraps the button group, and the label activates its first labelable descendant.
  Reproduced: `c-ptinc` → click on the label → `c-hweal`.

  Fix: use `<div role="group" aria-labelledby>` with a `<span>`.
- **m16. Empty or all-null series produce NaN geometry** (`Math.min()` = Infinity in `lineChart`,
  `index.html:417-430`) and console errors, with no "no data" message. This happens when
  `purchasing` is null (C2 path) or every GIC bin is filtered out.

  Fix: early-return with a message when `vals.length === 0`.
- **m17. Accessibility.**
  - Data tables exist only for transfers, the very top and IPP. The stack, levels, GIC, cross-check
    and housing charts have none.
  - Tooltips are pointer-only, with no keyboard access.
  - Legends are colour-only, with 7 adjacent bands.
  - The `aria-label`s are generic.

  Fix: add a "Show the table" `<details>` to each chart (the transfer one is the pattern to copy),
  and focusable points or a data table for keyboard users.
- **m18. Resize re-renders all 20+ charts on every height change**, which on mobile means every time
  the URL bar shows or hides (`index.html:841`). Fix: re-render only when the width changes.
- **m19. CAGR on non-positive averages returns NaN.** `cagr` uses `Math.pow(g, 1/yrs)` with
  g = a1/a0 (`index.html:628-631`), so a negative or zero layer average gives NaN and renders as
  "NaN%". Not reachable with today's layers. The same applies to `pct(NaN)` generally.
- **m20. The GIC floor is 1% of the mean (`index.html:680`).** Bins just above it still produce huge
  growth rates; the floor removes only near-zero bins. Consider 5%, or label the excluded and
  near-floor bins explicitly.
- **m21. The scenario note gives a misleading range.** "It changes 26 years (1997–2024)" hides the
  uncorrected years (1999, 2003). With zero corrected years it prints "undefined–undefined"
  (`index.html:595`).
- **m22. Unescaped `innerHTML` from data files.** Labels, `n_billionaires`, sources and notes go into
  `innerHTML` without escaping. The data is self-hosted, so the risk is low, but a stray `<` in a
  manual CSV would break the markup.
- **m23. Price-level mismatch between the two housing cards.** "Average price of existing flats" is
  true for Paris (Notaires). The "rest of France" level is a DVF mean that includes VEFA (off-plan
  new build), back-cast with an existing-dwellings index whose area includes Alsace-Moselle and
  Corsica, which DVF excludes. The two cards are therefore not level-comparable. Say so on the page.

---

## Reproduction log (fresh copy, no `data/raw`)

```
python3 -I pipeline/fetch.py data/raw          -> 25 files, 33 s wall, exit 0
python3 -I pipeline/build_data.py data/raw site/data/france.json data/manual
                                               -> 439 KB, 2.5 s, exit 0
python3 -m unittest discover -s pipeline/tests -> Ran 14 tests OK
diff vs committed france.json                  -> only meta.inputs_sha256["insee_hpi.xml"]
WID_data_FR.csv sha256 identical to the local copy (64429f6b…)
```

## Suggested order of work

1. C1, C2: centralise paths, make failures fatal, and surface `_checks`.
2. C3: add the tests listed, then re-run the three mutations; each should now fail.
3. M1 (doctype and viewport), M4 (`allow_nan=False`), M2 (CPI chaining): each is a one-line fix.
4. M3, M5: provenance and fetch robustness before the first public release.
5. M7, M8: prose generated from data, licence notes and LICENSE file.
