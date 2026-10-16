# Code review, round 2: pipeline, site, reproducibility, publishing (2026-10-16)

Scope: `pipeline/` (fetch, build_data, top_tail, paper_numbers, sources/*, tests), `site/index.html`,
README run instructions, licence files, `.gitignore`, `CITATION.cff`, and every relative link in the
Markdown files. Round-1 findings: [review-code.md](review-code.md). Response: [response.md](response.md).

Method:

- I read all the code in scope.
- I rebuilt the project in a clean copy, `<scratch>/review2-code/`, which had no `data/raw`, and
  followed the README literally. I then compared the rebuilt files with the committed ones value by
  value.
- I injected 17 Python mutations and 4 JavaScript mutations with a script.
- I drove the page in headless Chrome over the DevTools protocol: deep links, keyboard, mobile
  emulation and `file://`.
- I ran a link checker over 71 relative Markdown links.
- No project file other than this report was created or changed.

`<scratch>` stands for the session scratchpad. No local paths are given here; see Mi19.

File state reviewed (sha256, checked at the start and again just before writing, 22:49 +04):
`challenges_500.csv` 314bef8f…, `forbes_france_billionaires.csv` 04e547db…, `france.json`
40a70bc5…, `numbers.json` 8c6fbc1f…, `index.html` 5855aa0d…. No file changed while I worked.

## Post-review update (22:55): `index.html` changed while this report was being written

Another agent edited `site/index.html` (sha256 5855aa0d… → fadd798c…), `paper/paper.md` and
`README.md` after my snapshot. I re-tested the new `index.html` in headless Chrome against the same
`france.json`:

- **Ma3, partly fixed.** The catch handler now writes to `#findings`, so a `file://` load shows the
  message. `#constructor` still crashes, now with a *misleading* message: 0 charts, and "The data
  file could not be loaded (Cannot read properties of undefined …)". The own-property check is still
  missing (line 1331).
- **Ma4, still present.** From 1900, three presses of ArrowRight stay on 1900.
- **Ma6, partly fixed.** A hero legend now names every slice with its share, and the "last five
  slices" text is gone. The contrast and min-width points are not re-checked.
- **Mi10, still present.** The static `aria-label` on `#play` is at line 243.

Everything else below refers to the snapshot. `paper.md` changed only in its review-disclosure
wording. The data files and both rich-list CSVs are unchanged: same hashes as above.

## Summary

**Reproduction holds.**

- `fetch.py` downloaded 26 files (73 MB) in 34 s and exited 0.
- The build exited 0, `paper_numbers.py` wrote 54 numbers, and 21 tests passed.
- The rebuilt `france.json` equals the committed one in every value. The only differences are
  `meta.wid_vintage.fetched` and the hash of `raw/wid_vintage.json`, which contains that timestamp.
- `numbers.json` and `numbers.md` are identical to the committed files.
- The WID CSV is byte-identical to the maintainer's copy.
- The round-1 C1 fix (`manual_dir`) holds. Building from `pipeline/` as the working directory, or
  with the raw folder outside `data/`, gives identical values.

**What does not hold up:**

1. **The licensing statements are contradicted by the data being published (Critical).**
   - `DATA_LICENSES.md` and `CHANGELOG.md` say there is no Forbes API data and no Observatoire
     table.
   - `forbes_france_billionaires.csv` cites `forbes.com/forbesapi/...` in 26 of 26 rows.
   - `challenges_500.csv` cites inegalites.fr in 30 of 31 rows.
   - `france.json` copies both tables wholesale.
2. **The tests are better than in round 1, but the main claim is still not true.** The README says
   "every number quoted in the paper is checked against the data by the tests".
   - The check is a substring match, and the paper contains hand-typed numbers that the tests never
     see.
   - In README order, 6 of 17 Python mutants survive (one of them is equivalent). Eight more are
     caught only because the paper happens to quote the affected number.
   - None of the page's JavaScript is tested: 4 of 4 JS mutants survive.
3. **The page's error path is dead.** It writes to `#tiles`, an element that no longer exists. Any
   load failure, including opening the page from `file://`, therefore gives a blank hero with no
   message. The `#constructor` deep link crashes the page the same way.
4. **The hero slider traps keyboard users.** Arrow keys cannot move past any year that is followed
   by a gap in the data (e.g. 1900).
5. **The Pareto / "chain alpha" machinery has no effect on any output.** The method doc and the page
   describe it as shaping the scenarios. It also adds a way for the build to crash.

---

## Verification of round-1 fixes

| # | Round-1 finding | Response | Verdict | Evidence |
|---|---|---|---|---|
| C1 | `manual_dir` resolved two ways | Fixed | **Holds** | From `pipeline/` with no third argument: rich lists, 29 scenario years and IPP all present. Raw folder at `<scratch>/fi/alt/rawdata`: values identical. Only the keys of `inputs_sha256` change; see Mi9. |
| C2 | Upstream failures swallowed | Fixed | **Partially** | See below the table. |
| C3 | Tests could not catch bugs | Fixed | **Partially** | The 3 round-1 mutants are now caught. New mutants still survive; see Ma1. |
| M1 | Doctype, viewport, lang | Fixed | **Holds** | `compatMode = CSS1Compat`. At 390 px with mobile emulation: `scrollWidth = clientWidth = 390`, no element overflows. |
| M2 | CPI step at 1950 | Fixed | **Holds** | `priceFactor` uses `max(y, 1950)` (`index.html:505`). The CPI and WID bases are both 2025 = 1. |
| M3 | Provenance | Fixed | **Partially** | Hashing is recursive, SDMX headers are stripped (identical across my refetch), and ETag / Last-Modified / If-Range are recorded. But `wid_vintage.json` holds a `fetched` timestamp (`fetch.py:109`) and is hashed, so its hash changes on every fetch; it was the only diff in my rebuild. Hash keys also depend on the raw folder's name. |
| M4 | NaN in JSON | Fixed | **Holds** | `allow_nan=False` (`build_data.py:602`). The test parses with `parse_constant` raising. |
| M5 | Fetch robustness | Fixed, rest Open | **Partially** | See below the table. |
| M6 | Smoothing | Fixed | **Holds, one caveat** | The window is year-based (`index.html:510-519`), ends use 2 years, and the page says so. Scenario series still average corrected and uncorrected years at the edges of a run, e.g. `no_cut` 1999/2000. That is inherent; it is not stated. |
| M7 | Prose vs code | Fixed | **Partially** | Much prose is now computed. See below the table. |
| M8 | Licensing / hygiene | Open | **Partially** | LICENSE, LICENSE-DOCS and DATA_LICENSES were added. DATA_LICENSES is contradicted by the CSVs (Cr1). Google Fonts is still loaded on every visit (`index.html:11`). A `git add --dry-run` in a copy stages 49 files, none from `data/raw`, `.playwright-mcp`, `.DS_Store` or `__pycache__`. |
| m1 | Vintage-specific URLs | — | **Open** | Unchanged (`insee.py:137-153`, `prices.py:120`). |
| m2 | `top_n_wealth` guards | — | **Holds** | Sort, coverage and alpha guards exist and are tested. |
| m3, m4 | Rounded shares; inconsistent scenario inputs | Fixed | **Holds** | Layers come from g-percentiles. Max \|layer − published\| = 9.5e-5. |
| m5 | Dead "spread" scenario | Fixed | **Holds** | Exposed as `ggp_central`. It changes 0 years, and the page says so. |
| m6 | `round(None)` in scenarios | — | **Holds** | Fallback years are skipped (`build_data.py:263`). |
| m7 | Encodings | Fixed | **Holds** | Every `open()` in `pipeline/` passes `encoding=`. |
| m8 | DWA `None` arithmetic; `frozen_from` index misalignment | — | **Open** | `dwa.py:174-189` is unchanged. |
| m10 | HPI fetched twice | Fixed | **Holds** | |
| m11 | README | Fixed | **Partially** | The README text is fixed. The message for `file://` users never shows; see Ma3. |
| m13 | Duplicate-year tooltips | Fixed | **Holds** (read in the code: `index.html:640-650`) | |
| m14 | Reversed ranges | Fixed | **Holds** | Invalid options are disabled (`fillYears`). |
| m15 | "Measure" label click | Fixed | **Holds** | `div role=group` with `aria-labelledby`. |
| m16 | Empty series give NaN geometry | — | **Holds** | Early return with "No data". 0 SVG attributes contain NaN or undefined across 9 deep-link states. |
| m17 | Accessibility (tables, keyboard tooltips) | — | **Open** | 4 tables for 27 charts. Nothing inside a chart is focusable. |
| m18 | Resize re-renders everything | — | **Open** | `index.html:1219` re-renders on height changes too (mobile URL bar). |
| m19 | NaN% | — | **Holds** | `pct` returns "n/a" for non-finite values. |
| m21 | "undefined–undefined" | Fixed | **Holds** | |
| m22 | Unescaped `innerHTML` from data | — | **Open** | E.g. `legend()` at `index.html:572`, and `n_billionaires` and labels in `renderTop` / `renderTopIncome`. |

**C2 (partially).** These cases now fail loudly:

- missing source folder: `DataError ... pass --partial`;
- junk INSEE xlsx: `DataError ... _missing: hvp_if371`;
- `fetch.py` exits non-zero on any source error.

These still do not:

- **Empty `rates` CSV.** Exit 0 and `sources_status.rates = "ok"`. `mortgage_rate.years = []`, so the
  repayment charts are empty, and `paper_numbers.py` then crashes with `KeyError: 2000`.
- **DVF file cut to 1,999 rows.** Exit 0, status "ok", and every Paris and rest-of-France price
  silently drops by about 2.7% (Paris 2023: 10,547 → 10,264 €/m²).
- **Malformed housing or prices XML.** A bare `KeyError: '010567058'`.
- **Truncated WID CSV.** A bare `IndexError` in `extrapolated_from`.
- **`sources/__init__.py:15-17` swallows `ModuleNotFoundError`.** A deleted source module silently
  drops out of `SOURCES`, and with it out of the checks.

**M5 (partially).**

- `fetch.py` has timeouts, retries, a 206 check, If-Range and atomic writes.
- The source modules have no retries.
- `prices.py:151` and `housing.py:102` write straight to the final path.
- Data validation still uses `assert` in five places: `prices.py:264,290,333` and
  `insee.py:581,653`.

**M7 (partially).** Still hard-coded:

- "530 people" in the h2 at `index.html:337` and the glossary at `:407`;
- "the 2025 average of recorded sales" at `:366`;
- "since 1988" in the hero caption at `:1138`;
- "38% … against 32%" at `:1016`;
- "so no correction" at `:949`, printed whatever the data say.

Today all of these match the data. Also, `docs/03-method.md` says "Version 0.3" while the README says
0.4.

---

## Critical

### Cr1. The rich-list provenance contradicts the licence statements, and `france.json` republishes it

*Conditional: the task notes these CSVs may be being replaced. The hashes above are the state I
reviewed.*

The docs say:

- `DATA_LICENSES.md`, Forbes row: "Figures quoted from published articles only (no API or scraped
  data)".
- `DATA_LICENSES.md`, closing note: the Observatoire table and the Forbes API data "were removed
  before publication".
- `CHANGELOG.md` 0.4.0 says the same.

The data say:

- `data/manual/forbes_france_billionaires.csv`: 26 of 26 rows have a `source_url` of the form
  `https://www.forbes.com/forbesapi/person/billionaires/<year>/...json?...limit=5000`, with notes
  such as "LOWER BOUND: API list for this year is incomplete".
- `data/manual/challenges_500.csv`: 30 of 31 rows cite `https://www.inegalites.fr/spip.php?page=tableau&num=2646`.
  Some notes read "Total from IdO table only".
- `build_data.load_rich_lists` (`build_data.py:79-92`) copies every non-empty column into
  `france.json → rich_lists`, notes and URLs included. The page's own note (`renderTop`) describes
  Forbes totals as "sums of Forbes's per-person figures".

Why it is Critical: the repository is presented as open and licence-clean. Publishing this state puts
the API-derived and IdO-derived values and their provenance on GitHub and on the live site, next to a
document that says they were removed.

Fix:

- Replace both CSVs as announced and rebuild `france.json`.
- Ship only `year`, the total and the source per row in `rich_lists`.
- Add a test that fails on a stale build. For every `data/manual/*.csv`,
  `D.meta.inputs_sha256["manual/<name>"]` must equal the sha256 of the file on disk. Today nothing
  ties the committed JSON to the committed CSVs.

---

## Major

### Ma1. The test suite still misses realistic bugs, and most "catches" are only drift detection

I ran each mutant through build → tests, in two modes:

- **A:** the README order, where `paper_numbers.py` regenerates `numbers.json` before the tests.
- **B:** keeping the committed `numbers.json`.

The harness is `<scratch>/mut/mutate.py`.

| Mutant | Kind of bug | A (README order) | B (strict) | What catches it |
|---|---|---|---|---|
| M1 | Rich list matched to year y+1 (off by one) | caught | caught | deflation test and method-doc oracle: **a correctness test** |
| M2 | Scenario uses the previous year's adult count | **missed** | caught | B: snapshot only. A: the paper's "21" became "22", which occurs inside "2022"; see Ma2 |
| M3 | DWA top-5% comparison wired to DWA top-10% | caught | caught | drift only (`dwa_top5_gap` is quoted in the paper) |
| M4 | ERFS top 10% plotted as S90 (bottom 90%) instead of 1 − S90 | **missed** | **missed** | — |
| M5 | INSEE 2019 national accounts: top 10% and bottom 50% fields swapped | **missed** | **missed** | — |
| M6 | Chain-alpha rank ratio 8 instead of 5 | equivalent mutant | equivalent mutant | the output is unchanged; see Ma5 |
| M7 | Pareto exponent `1 − alpha` instead of `1 − 1/alpha` | caught | caught | unit tests: **a correctness test** |
| M8 | Projected top threshold uses `2**alpha` | caught | caught | drift only |
| M9 | Housing "bottom 50%" = deciles 1–4 | caught | caught | drift only |
| M10 | ERFS constant-to-nominal conversion inverted | caught | caught | drift only |
| M11 | Pre-1990 CPI splice factor inverted | **missed** | **missed** | — |
| M12 | DWA scenario scales the top 10% instead of the top 5% | caught | caught | build `check` (shares sum): **a correctness check** |
| M13 | Mortgage rate not divided by 100 | caught | caught | drift only |
| M14 | Paper annuity over 20 years instead of 25 | caught | caught | drift only |
| M15 | Housing back-cast anchored on the first DVF year | caught | caught | drift only |
| M16 | IPP amounts for WID not converted to 2016 prices | caught | caught | drift only |
| M17 | `extrapolated_from` off by one year | **missed** | **missed** | — |
| J1 | JS decomposition weights swapped: `growth = s0·ΔT`, `share = Δs·T1` (still sums exactly) | **missed** | **missed** | no JS tests |
| J2 | JS annuity halved | **missed** | **missed** | no JS tests |
| J3 | JS `priceFactor` clamp at 1990 instead of 1950 | **missed** | **missed** | no JS tests |
| J4 | JS `poorestHolding` returns the bin's upper edge | **missed** | **missed** | no JS tests |

How the catches break down:

- **Real correctness tests** caught only 3 of 21 mutants: M1, M7 and M12.
- **Drift only:** 8 more fail only because the paper quotes the affected number. These tests would
  pass if the paper were edited to match the bug. They also fail on every legitimate WID refresh.
- **Vacuous snapshot test.** `test_numbers_file_is_current` cannot fail when run in README order,
  because step 3 has just regenerated the file it compares against.

Proposed tests, one per miss:

- **M2: recompute W_n independently.** For the last Challenges year:
  `top_tail.top_n_wealth(adults_covered/adults[y]*100, bins from gp at y, alpha) / 100 * adults[y]`
  must equal `rich_list_check.ggp_low.wid_top_n_eur[-1]` to within 1 euro. Then recompute
  `scenario_shares` for that year from the JSON and compare all layers.
- **M4 and M5: comparison plausibility.** Every non-WID series must stay within 8 points of the WID
  series of the same indicator in overlapping years. M4 gives 75% against 24%; M5 gives 38% against
  24% for the top 10%. Better still, build `comparison` from a small fixture with known values and
  assert the mapping.
- **M11: CPI continuity at the join.**
  `cpi_all[join−1]/cpi_all[join] == cpi_long[join−1]/cpi_long[join]` to within 1e-6, and
  `cpi_all[join] == cpi[join]`.
- **M17: extrapolation flag, independently.** `quality[extrapolated_from] < quality[extrapolated_from − 1]`,
  and all later years equal `quality[extrapolated_from]`. Add the doc oracle: wealth 2015, income
  2019.
- **J1–J4: test the JavaScript.**
  - Move `decompose`, `annuity`, `priceFactor`, `smooth` and `poorestHolding` into a module and test
    it with `node --test`. This needs no dependencies.
  - Add one headless page test: load the page, then compare the findings text and the hero caption
    to `numbers.json`. All 2024 figures match today (5.6%, 4.8%, 7.7% vs 2.7%, 51.9%, 41 vs 19
    years). That match is a coincidence of two implementations; nothing enforces it.
- **Decomposition invariant.** In JS and in Python: `growth + share == net` for every layer, and
  `growth == (s0+s1)/2·ΔT`. The second assertion kills J1, which the first does not.
- **Run the strict mode in CI.** Run the tests before `paper_numbers.py`, or compare against the
  committed file. Label `test_numbers_file_is_current` as a snapshot test, not a correctness test.

Also:

- `class Paper` is defined after `if __name__ == "__main__": unittest.main()`
  (`pipeline/tests/test_build.py:218-222`). Running `python3 pipeline/tests/test_build.py` therefore
  runs 19 tests and silently drops the two paper tests.
- `test_numbers_file_is_current` does not skip when `france.json` is missing; it errors instead.

### Ma2. "Every number quoted in the paper is checked against the data by the tests" is not true

The claim is in the README and in the docstring of `paper_numbers.py` ("the text cannot drift from
the data"). Three problems:

- **The check is a bare substring match** (`test_build.py:228`). Of the 54 values, 7 also match
  inside other numbers. For example:
  - `scenario_years_ggp_low = "9"` has 5 real occurrences but 86 substring hits;
  - `years_paris_1996 = "19"` has 1 real occurrence but 41 substring hits;
  - `scenario_years_no_cut = "21"` has 3 real occurrences but 5 substring hits.

  M2 above changed "21" to "22", and the test still passed. Presence is checked, not position, so
  two swapped values also pass.
- **The paper contains hand-typed numbers that no test sees** (`paper/paper.md:217, 231, 234, 236`):
  - "5.58% to 5.37%" (correct today);
  - "about 6%": the level effect is 6.6%; the effect on growth is 10%;
  - "from 13% to 30%";
  - "at most 0.00009": the actual maximum is 9.5e-5, so the stated bound is **wrong**.
- **`docs/03-method.md` quotes many numbers that are not checked**, e.g. "€667 bn" and "alpha 1.9".
  Only the 2024 scenario table is tested.

Fix:

- Match on token boundaries: `(?<![\d.,])value(?![\d])`.
- Better: write `{{key}}` placeholders in a paper source and render `paper.md` from `numbers.json`.
  The test then becomes "rendered output equals the committed file".
- Generate the four hand-typed values.
- Either extend the same mechanism to the method doc, or soften the README sentence.

### Ma3. The page's error handler is dead: every load failure shows a blank hero with no message

`index.html:1238`: `document.getElementById("tiles").innerHTML = ...`. No element has `id="tiles"`;
the tiles became `#findings`.

Demonstrated in headless Chrome:

- **`file://…/site/index.html`.** The fetch is blocked, the catch handler throws `TypeError: Cannot
  set properties of null (setting 'innerHTML')`, and the page has 0 SVGs and no `.err` element. The
  README tells readers that the page explains this situation. It does not.
- **`#constructor`.** `D.concepts[tok]` (`index.html:1226`) is not an own-property check, so
  `state.concept = "constructor"`, rendering throws, and the dead handler throws again. Result: 0
  charts and no message. The same happens for `#toString`, `#__proto__` and similar.

Fix:

- Point the handler at `#findings`, or at a dedicated `role="alert"` element.
- Use `Object.hasOwn(D.concepts, tok)` and the same for `params`.
- Listen to `hashchange`. Today a deep link pasted into an open tab does nothing.
- Consider writing the state back into the hash so that links can be shared.

### Ma4. The hero slider traps keyboard users at every year followed by a gap

`index.html:1155` sets `hero.year = +r.value`. `renderHero` then snaps to the nearest earlier
existing year (`nearestYear`, `:1064`) and writes that back to `r.value`.

| Concept | Start | Result of ArrowRight |
|---|---|---|
| Wealth | 1900 | 5 presses stay on 1900/1900, because 1901 does not exist |
| Pre-tax income | 1900 | stuck, because the next year is 1910 |
| Wealth | 1905, 1907, 1909 | same trap |

Only PageUp, End or a mouse drag escape. This fails WCAG 2.1.1 for the page's main control. The
slider also has no `aria-valuetext`.

Fix: make the slider index-based (`min=0`, `max=years.length−1`) and set
`aria-valuetext = years[i]`. Alternatively, snap in the direction the value moved.

### Ma5. The Pareto / chain-alpha step never affects any output, and the docs say otherwise

`top_tail.top_n_wealth` applies the Pareto split only when the list covers *less* than the top bin
(`top_tail.py:86`: `hi == 100 and remaining < width`). The list never does:

- the share of adults covered (`n_pct`) is 0.0017–0.0020% for `ggp_low` and `no_cut`, and
  0.017–0.020% for `ggp_central`;
- the top bin is 0.001% wide.

So alpha has no effect on W_n. Mutant M6 (rank ratio 8) leaves `france.json` byte-for-byte unchanged.
M7 (wrong exponent) changes nothing in the data either; it is caught only by the unit tests.

These texts are therefore wrong or misleading:

- `docs/03-method.md:183` ("Pareto inside the top bin with alpha from the threshold chain") and
  `:228` ("the effect on W_n is under 1%"). The effect is exactly 0.
- The page's top-bin note (`index.html:968`): "The scenarios therefore estimate the shape inside the
  top group from the thresholds below it."

Why it matters beyond the wording:

- `build_scenarios` calls `chain_alpha` unconditionally for every Challenges year
  (`build_data.py:269`). A future vintage with a local alpha ≤ 1 would crash the build over a value
  that is not used.
- The assumption that does matter is the uniform split inside the p99.998–p99.999 bin for the 370
  extra adults. It is not stated anywhere.

Fix: say plainly that the list always covers more than the top bin, so W_n is the top bin plus a
uniform share of the next bin. Then either compute alpha only when it is needed, or drop it.

### Ma6. In the hero chart, three of the labelled shares cannot be attributed to a group

The geometry is correct. Population widths are `width(L)·W` (571, 456.8, 102.8, 10.3 and 1.03 px at
W = 1142). Pie widths are `share·W − 1.5` px. The 2024 wealth segments rebuild to 4.8% / 35.3% /
32.2% / 14.3% / 5.7% / 2.0% / 5.6%, matching `france.json`.

The problems are in labelling and distortion:

- **Unattributed labels.** The pie bar prints "32.2%", "14.3%" and "5.7%" at 2024 wealth with no
  group name. They belong to the top 10–1%, top 1–0.1% and top 0.1–0.01%, whose population segments
  are 103 px, 10 px and 1 px wide; only the first is readable. The only link from a number to a
  group is colour. There is no legend in the hero, and the 2.0% slice (top 0.01–0.001%) has no label
  at all.
- **Wrong annotation.** The bracket says "the last five slices are almost invisible here"
  (`index.html:1117`). The first of those five is a clearly visible 103 px block.
- **Distortions:**
  - the 0.6 px minimum inflates the top-0.001% population segment about 52×;
  - the 1.5 px gaps shrink small pie segments, e.g. the after-tax top 0.001% (0.58%) is drawn 23%
    short (5.1 instead of 6.6 px).

  Both are sub-pixel or small, but neither is stated.
- **Contrast.** Dark labels (`#0b1322`) on s7 reach 3.2:1, on s6 3.8:1 and on s1 4.2:1. That is
  below AA for 13 px text, and it hits the "Richest 0.001%" segment and "Poorest 50%".
  `round2-review-ux.md` covers palette contrast; I add only the hero-label cases.

Fix: name the slices in the bottom-bar labels (or add a compact legend), correct the bracket text, and
state the minimum-width rule in the caption.

---

## Minor

**Pipeline**

- **Mi1.** `fetch.py:109` writes a `fetched` timestamp into `wid_vintage.json`, and that file is
  hashed into `inputs_sha256`, so every refetch changes the provenance hash. Hash the ETag and
  Last-Modified only, or exclude the `fetched` field.
- **Mi2.** `sources/__init__.py:15-17`: a missing source module is skipped silently. Make
  `NAMES` authoritative and fail.
- **Mi3.** The source loaders run no sanity checks: an empty rates CSV or a truncated DVF file
  passes as "ok" (see C2 above). Check at minimum that the year range and row counts are as
  expected, and fail otherwise.
- **Mi4.** Non-atomic writes remain at `prices.py:151` and `housing.py:102`. Data `assert`s remain
  at `prices.py:264,290,333` and `insee.py:581,653`.
- **Mi5.** `dwa.py:174-189`: `None` arithmetic, and `frozen_from` indexes `quarters` (unfiltered)
  with a position from `hh_q` (filtered). This is round-1 m8, unchanged.
- **Mi6.** The Notaires loader is dead code. `housing.py:7,47-51,87,216-237,272-277` load a manual
  CSV that was removed for licensing reasons. `docs/notes/prices-housing.md:8` still lists
  `data/manual/notaires_idf_apartment_prices_m2.csv`, and the table at line 79 quotes values that
  can no longer be rebuilt. Remove the loader, or document it as optional and unused.
- **Mi7.** The `sources/__init__.py` docstring still describes `load(raw_dir)`; several loaders take
  `manual_dir`.
- **Mi8.** `paper_numbers.py` hard-codes the years 1900, 1950, 1980, 1990 and 2014, the repayment
  year 2000 (`:127`) and B = 1990. With the next vintage these keys go stale or crash, as the
  empty-rates case showed (`KeyError: 2000`).
- **Mi9.** The keys of `inputs_sha256` contain the raw folder's name: `raw/...` versus
  `rawdata/...` for identical inputs. Key them relative to the raw folder itself.

**Front end**

- **Mi10.** `#play` has a static `aria-label="Play the years"` while its visible text switches to
  "❚❚ Pause" (`index.html:226`). The accessible name and the visible label disagree (WCAG 2.5.3).
  While playing, `#hero-caption` (`aria-live="polite"`) is rewritten every 110 ms; pause live
  updates during playback.
- **Mi11.** `.term` tooltips are CSS `::after` content with no `aria-describedby`. Screen readers do
  not reliably announce them.
- **Mi12.** The top-wealth summary prints "so no correction" whatever the data say
  (`index.html:949`). It is true today because `ggp_central` corrects 0 years. Derive it from
  `corrected_years`.
- **Mi13.** These remain open from round 1: m17 (no data table for 23 of 27 charts; nothing in a
  chart is focusable), m18 (resize on height change), m22 (unescaped `innerHTML`).
- **Mi14.** On the band chart (`renderTop`), the four scenario lines are told apart by colour only.
  Under deuteranopia simulation, s1 and s7 (blue and purple) drop to ΔE 12, and they are the WID and
  ECB lines. Add direct end labels, or dash the alternatives.
- **Mi15.** The Sources section says everything "can be rebuilt … with three commands". The README
  has five.

**Publishing and docs**

- **Mi16.** Broken anchor at `docs/notes/rich-lists.md:42`: `../03-method.md#37-top-tail-check`. The
  heading is "3.7 The very top: calibration, rich lists, scenarios", whose anchor is
  `#37-the-very-top-calibration-rich-lists-scenarios`. The other 70 relative links resolve.
- **Mi17.** Licence scope. `LICENSE:25` puts all of `site/` under MIT, including
  `site/data/france.json`, which holds third-party derived data and quoted rich-list rows. Nothing
  states a licence for `data/manual/`. Exclude `site/data/` and `data/manual/` from the MIT scope
  and point them to `DATA_LICENSES.md`.
- **Mi18.** `CITATION.cff`:
  - it uses `type: software` and `license: MIT` only, although the text is CC BY 4.0;
  - there is no `preferred-citation` for the working paper;
  - the author is an anonymous entity.
- **Mi19.** `docs/reviews/review-numbers.md:42,64` contain absolute local scratch paths, including
  the maintainer's account name. Redact them before publishing.
- **Mi20.** The page loads Google Fonts on every visit (`index.html:11`); this is round-1 M8, still
  open. Self-host the two fonts.

---

## Reproduction log (clean copy, README order)

```
python3 -I pipeline/fetch.py data/raw                     -> 26 files, 73 MB, 34 s, exit 0
python3 -I pipeline/build_data.py data/raw site/data/france.json
                                                          -> 476 KB, exit 0, all 5 sources "ok"
python3 -I pipeline/paper_numbers.py ...                  -> 54 numbers, exit 0
python3 -m unittest discover -s pipeline/tests            -> Ran 21 tests, OK
value diff vs committed france.json                       -> 2 fields: meta.wid_vintage.fetched,
                                                             inputs_sha256["raw/wid_vintage.json"]
value diff vs committed numbers.json / numbers.md         -> none
WID_data_FR.csv                                           -> byte-identical to the local copy
data/manual/*.csv                                         -> unchanged during the review
```

Front end, served from the clean copy with `python3 -m http.server -d site` and driven in headless
Chrome over the DevTools protocol:

- **Deep links** (fresh navigation each time): `#ptinc`, `#diinc`, `#hweal~no_cut~smooth3`,
  `#diinc~cpi`, `#ptinc~cpi`, `#hweal~dwa_lower~cpi~smooth3`, `#hweal~ggp_central`, `#bogus`. Each
  gave the right controls and status, 27 SVGs, no console errors, and no NaN, undefined or Infinity
  in visible text or SVG attributes. `#constructor` crashed the page; see Ma3.
- **Hero vs data.** The hero and findings figures equal `numbers.json` and an independent Python
  recomputation for wealth (2024, 1990, 1950, 1913, 1900), pre-tax income (2024, 1900) and after-tax
  income (2024, 1980).
- **Keyboard.**
  - Tab order is logical: glossary term → chips → Play → slider → measure → From/To → Expert
    settings → chapter rail → "How to read" toggles.
  - Every control shows a 2 px focus outline.
  - Enter and Space work on Play and the chips. Expert settings opens with Enter and closes with
    Escape, and focus returns to its summary.
  - The slider fails; see Ma4.
- **Mobile.** At 390 × 844 with mobile emulation there is no horizontal overflow and no hero label
  overlaps (also checked at 1280 px, years 2024, 1990 and 1950).
