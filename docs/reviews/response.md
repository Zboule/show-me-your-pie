# Response to the reviews (version 0.2 → 0.3)

Four reviews were run on version 0.2, each by a separate AI reviewer agent
(Claude) asked to be as critical as possible, working from its own brief and
its own computations. They are adversarial checks, not peer review by outside
experts:

| Review | File | Verdict |
|---|---|---|
| Methodology (referee) | [review-methodology.md](review-methodology.md) | Major revision |
| Numbers (independent recomputation) | [review-numbers.md](review-numbers.md) | No critical error; all headline numbers reproduce from raw data |
| Code and reproducibility | [review-code.md](review-code.md) | Reproducible, but fragile and weakly tested |
| Sources and framing | [review-sources.md](review-sources.md) | Numbers match sources; framing, citations and licensing need work |

Below, every critical and major finding and what was done. "Fixed" means the
change is in the code, the page and the docs; "Open" means it is listed as a
limit or planned extension.

## Methodology

| # | Finding | Action |
|---|---|---|
| C1 | "Transfers" (Δshare × end-year total) read as euros moving between groups; the bottom 50%'s real wealth actually rose | **Fixed.** Replaced by an exact growth/share decomposition with average weights (§3.5), plus the share of total growth each layer received. "Moved", "changed layer", "lost" and "each" are gone. The start-year valuation and end-year valuation are shown for comparison. |
| C2 | Scenarios could only raise the top; "1 adult per family" below the literature's floor; neutral scenario hidden; ECB evidence never became a scenario | **Fixed.** Families converted with 1.8 adults per member; all scenarios selectable including the neutral one (`ggp_central`, changes nothing); new `dwa_lower` scenario lowers the top to the ECB / Banque de France level; `W_n` vs list shown every year; the one-sided rich-list rule is justified (a list is a lower bound). |
| C3 | WID's Forbes calibration starts in 1988, so 1980 → 2024 crosses a break | **Fixed.** Default start year 1990; 1988 marked on charts; warning when the start is earlier; "largest jumps" claim corrected; 2014 jump described as a Forbes coverage change. **Open:** WID's uncorrected series is not public. |
| M1 | Top-bin threshold inconsistency over-read ("thin €100M–€800M") and used for alpha | **Fixed.** Inference withdrawn; alpha now from the threshold chain p99.99 → p99.998; the jump is computed every year and shown (5.9× in 2024). Coherence test added (no violation of t ≤ a ≤ t_next). |
| M2 | IPP comparison mixed denominators ("4×") | **Fixed.** Compared in euros, with IPP's dividend-imputed variant: WID ≈ dividend-imputed; ownership-based 2.7× (top 0.001%), 1.7× (0.01%), 1.13× (0.1%), 0.87× (1%). Wording made indicative. |
| M3 | Post-tax allocation of public spending misstated; 2019+ mechanical | **Fixed.** Health close to lump-sum, education and other spending proportional (DINA Guidelines 2025, Bozio et al. 2024); source of the French series (Fisher-Post & Gethin 2023) cited; 2019+ fixed-ratio extrapolation stated; INSEE gap explained by unranked hypotheses. |
| M4 | Century series treated as one method; artifacts | **Fixed.** Shading by WID's quality flag for all years; method breaks table (§3.11); artifacts named (1975, 1984, 1961 = 1963); "one methodology" withdrawn. |
| M5 | Housing metric used pre-tax income, inconsistent across files, no financing cost | **Fixed.** Cash disposable income per consumption unit (INSEE ERFS) by group; yearly repayment at the ECB mortgage rate added; all files aligned. **Open:** deposit, insurance, notary fees. |
| M6 | Page text contradicted its own controls | **Fixed.** Method text rewritten to describe the scenario selector. |
| m1 | CPI step at 1950 | **Fixed.** 1950 ratio held for earlier years. |
| m2 | Smoothing left the end year raw | **Fixed.** Year-based window; ends use the two available years, stated on the page. |
| m3 | Billionaire tile mixes units | **Fixed.** Caption says citizens, some abroad; "~" kept. |
| m5 | Population growth and ageing | **Fixed** (stated). **Open:** within-age shares. |
| m7 | Challenges July vs WID yearly | **Fixed** (stated); ±3% uncertainty of the series stated. |
| C1 (price/volume) | Wealth changes mostly revaluation | **Open:** planned (§3.13). |

## Numbers

| # | Finding | Action |
|---|---|---|
| 1 | CPI step at 1950 | Fixed (above). |
| 2 | Housing text vs charts | Fixed (above). |
| 3 | "5–7 points" and "1–2 points" ranges contradicted | **Fixed.** Ranges are now computed from the data on the page (5.8–7.6; −1.8 to +3.5). |
| 4 | Bottom-half growth sentence averaged bin rates | **Fixed.** Uses the layer's own average growth. |
| 5 | 1 adult per family | Fixed (above). |
| 6–10 | IPP ratio wording; jumps; DWA total range; table omissions; corrected-years wording | Fixed in §3.7–3.10. |
| 11 | Tile ignored smoothing | Tiles are explicitly "WID as published, each year"; the note says so. |
| 12 | Asset-composition series inconsistent with net wealth; 2025 base partly projected | Stated on the page and in §3.3/§3.9. |

## Code

| # | Finding | Action |
|---|---|---|
| C1 | `manual_dir` resolved two ways | **Fixed.** Resolved from the repository; passed to every source; missing files are an error. |
| C2 | Upstream failures swallowed | **Fixed.** `fetch.py` exits non-zero on any source failure; build stops on missing sources or failed source checks unless `--partial`; status recorded in `meta.sources_status`. |
| C3 | Tests could not catch bugs | **Fixed.** Tautological tests removed; closed-form Pareto tests at several alphas; exact-hit and straddling toy cases; layers vs WID's published shares; wiring; deflation; scenario direction; oracle against the method doc; strict JSON. |
| M1 | No doctype / viewport / lang | **Fixed** in `site/index.html`. |
| M2 | CPI step | Fixed. |
| M3 | Provenance | **Fixed.** Recursive input hashes (SDMX headers stripped); WID ETag / Last-Modified recorded. |
| M4 | Possible NaN in JSON | **Fixed.** `None` and `allow_nan=False`. |
| M5 | Fetch robustness | **Fixed** in `fetch.py` (timeouts, retries, 206 check with If-Range, atomic writes) and the DVF stream. **Open:** source modules still use their own download helpers. |
| M6 | Smoothing | Fixed. |
| M7 | Prose vs code | Fixed; most numbers in the page prose are computed from the data. |
| M8 | Licensing | **Open**, listed in the README publishing checklist (decisions for the owner). |
| m3–m4 | Rounded shares; inconsistent scenario inputs | **Fixed.** Layers summed from full-precision g-percentiles, so scenarios and layers use the same totals. |
| m5 | Dead "spread" scenario | Fixed (exposed as `ggp_central`). |
| m7 | Encodings | Fixed in the build. |
| m10 | HPI fetched twice | Fixed (removed from `fetch.py`). |
| m13 | Duplicate-year tooltips | Fixed (both methods shown). |
| m14 | Reversed year ranges | Fixed (invalid options disabled). |
| — | Clicking "Measure" switched the measure | Fixed (no longer a label). |

## Sources

| # | Finding | Action |
|---|---|---|
| C1 | Health allocation contradicted | Fixed (above). |
| C2 | Calibration reach; 2014 coverage change | Fixed (above). |
| C3 | 30% pre-committed figure cited to the wrong document | **Fixed.** Cited to INSEE definition c1358 and national accounts table 2.103; missing items added. |
| C4 | Transfer vocabulary | Fixed (above). |
| M1 | `diinc` source misattributed | Fixed. |
| M2 | "One methodology" | Fixed. |
| M3 | GGP appendix H citation; "values GGP use" | **Fixed.** Cited as WID WP 2016/6 (2016, rev. 2017); scenarios "inspired by". |
| M4 | IPP overclaim | Fixed (above). |
| M5 | Counter-evidence less prominent | **Fixed.** The ECB gap is stated next to the tiles; the scenario range is in the first tile. |
| M6 | Missing sources | **Fixed.** Bozio et al. 2024, Blanchet–Chancel–Gethin 2022, Auten & Splinter 2024 with the Saez–Zucman reply, Landais 2007, France Stratégie's capital-tax committee, INSEE Références added to the references; Auten & Splinter and Bozio et al. on the page. |
| M7 | Discontinuity presented as a finding | Fixed (labelled as our analysis, both readings). |
| M8 | Contradictions between docs | **Fixed** in rich-lists.md and 01-concepts. |
| M9 | Licensing | **Open**, publishing checklist. |
| M10 | Challenges series from one undocumented table | **Fixed** (stated, ±3%). **Open:** rebuild from primary press articles. |
| M11 | Undefined citation keys | Fixed. |
| Minor | Bibliographic fields, links, "Paris urban unit", DVF single-property sales | Fixed in references.md, 01-concepts, prices-housing. |
