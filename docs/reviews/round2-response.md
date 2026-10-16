# Response to the second review round (version 0.4)

Five reviews were run on version 0.4, each by a separate AI reviewer agent
with an adversarial brief (see [README.md](README.md)). Below, every critical
and major finding and what was done. "Fixed" means the change is in the
code, the page, the paper and the docs; "Stated" means it is now an explicit
limitation; "Open" means it remains to do.

## Code and reproducibility ([round2-review-code.md](round2-review-code.md))

| Finding | Action |
|---|---|
| Licensing statements contradicted the CSVs (Forbes API and Observatoire rows) | **Fixed.** Both series rebuilt from article quotes only ([notes/rich-lists-sources.md](../notes/rich-lists-sources.md)); dataset rebuilt; new test `Provenance.test_built_from_current_manual_files` fails if the dataset was built from older hand-entered files. |
| Page JavaScript untested (4/4 JS mutants survived) | **Fixed.** Pure calculations moved to `site/core.js` (decomposition, annuity, poorest-holding comparison, smoothing, CPI factor, slider stepping) and tested against hand-computed cases in `pipeline/tests/test_core.mjs`, run by the Python suite. |
| Paper-number check was a substring match ("22" inside "2022") and several paper figures were typed by hand | **Fixed.** Whole-number matching on normalised text; the hand-typed figures (precision, pre-committed spending, CPI gaps, start-year runs, smoothing, peaks) are now generated in `paper/numbers.json`. |
| Empty rates file built "ok"; truncated DVF shifted prices silently | **Fixed.** Housing needs ≥ 20 years of rates and income; a DVF year counts only if all 12 months have ≥ 90 départements. |
| Non-atomic writes and `assert` data checks in source modules | **Fixed** (prices, housing, insee). |
| `#constructor` deep link crashed the page | **Fixed** (own-property checks). |
| Hero slider trapped keyboard users at 1900 | **Fixed** (`stepYear` moves to the next year with data in the direction moved; tested). |
| Pareto/alpha step never used but documented as used | **Fixed.** Alpha is computed only if needed; docs and page say the scenarios take WID's top group whole. |
| Local paths in review files; Google Fonts on every visit; MIT scope over data; broken anchor | **Fixed.** Paths redacted; fonts self-hosted with OFL licences; licence scope clarified; anchor fixed. |
| `test_numbers_file_is_current` cannot fail in README order | **Stated.** It guards against forgetting to regenerate; the paper-quote test is the substantive check. |

## Plain language and accessibility ([round2-review-ux.md](round2-review-ux.md))

| Finding | Action |
|---|---|
| Hero: no colour key, unlabeled slices, wrong "last five slices" text, light-mode contrast | **Fixed.** Legend with every slice's share; corrected text; hero colours fixed to its dark theme; lighter secondary text. |
| 2024 shown without saying it is an estimate | **Fixed.** "Estimate" badge and note on extrapolated years. |
| Caption lacked context and range | **Fixed.** Range across estimates, and "many of the poorest own very little or owe more than they own". |
| Uncertainty shown too late | **Fixed.** "How sure are we?" finding and "What this page does not say" box under the findings. |
| Jargon; only one tooltip; tooltips unreadable by screen readers | **Fixed** (term dictionary for WID, INSEE, ECB/BdF, IPP, DVF; aria labels; glossary). |
| Too technical for the main page | **Fixed.** Start-year sensitivity, growth by rank, IPP table, four cross-check panels, fixed costs and asset mix moved into "For experts" sections. |
| Light-mode contrast; unordered rainbow for ranked slices; same colours for different meanings | **Fixed.** Darker muted text; ordered cool-to-warm ramp for slices and income groups everywhere; dashed lines for alternative sources and scenarios. |
| Values only on hover | **Fixed.** "Show the numbers" table under every chart. |
| Titles and wording not following the chosen measure | **Fixed.** Chapter 03 title follows the measure; "yearly income" for income; note that both income views share one total; settings bar labelled for chapters 01–04; 100% line on repayment charts. |
| Play animation and screen readers; reduced motion; load error target; skip link | **Fixed.** |
| "Independent reviews" suggested human experts | **Fixed.** Page, README, paper and this folder say the reviews are by separate AI agents, not external peer review. |
| French version | **Open.** The page is in English; a French version is the main remaining barrier for a French audience. |

## Methodology ([round2-review-methodology.md](round2-review-methodology.md))

| Finding | Action |
|---|---|
| "Bottom and middle are robust across sources" contradicted by the data | **Fixed.** Agreement is stated for the poorest half's level only; the middle 40% (WID 4.7–6.8 points lower than ECB/BdF) is added to the main comparison and the paper. |
| "Share of total growth" breaks when the total falls or barely moves | **Fixed.** Shown only when the total rose by at least 5%; defined in §3.5 of the method. |
| The ECB-based 4.8% is our construction, not a published estimate; it lifts the poorest half above the accounts; not independent of Challenges | **Fixed.** Labelled illustrative everywhere; caveats stated; the headline lower bound is now the Forbes floor (what Forbes counts for French billionaires as a share of total wealth, 4.3% in 2024). |
| Top numbers given as points | **Fixed.** Top 0.001% share 4.3%–6.5%; share of the wealth rise 5.8%–9.0%; "as much as the poorest X%" 48.3%–54.1%; all generated from the data. |
| 2024 income headline contains no 2024 information | **Fixed.** The headline uses 2018, the last year WID does not extrapolate; 2024 values are labelled extrapolated; WID 2019 (32.1%) is compared with INSEE 2019 (38%). |
| Flow language ("went to", "got") | **Fixed.** "Holdings rose by an amount equal to…". |
| Most of the wealth rise is revaluation; post-2014 shares largely mechanical | **Stated** in the abstract, results and limitations. |
| Start-year sentence wrong | **Fixed** and generated from the data. |
| "Housing, not inflation" unsupported | **Fixed.** Replaced by: consumer price indices exclude house purchases. |
| Housing caveats (single person, regional prices, peak, estimated rates) | **Stated**, with the 272% peak in 2012. |
| IPP ratios depend on the measure; households vs adults bias | **Stated.** |
| Scenario years with no rich-list total fall back to WID | **Fixed.** Interpolated between neighbouring published years and flagged. |
| Ten missing limitations | **Fixed.** Paper §7 now lists them. |
| WID's uncorrected series; price/volume split | **Open** (planned extensions). |

## Numbers ([round2-review-numbers.md](round2-review-numbers.md))

| Finding | Action |
|---|---|
| CPI robustness figure stated three ways, none right | **Fixed.** Generated: real growth of mean wealth per adult 1980–2024 is 181% with WID prices, 163% with consumer prices. |
| Start-year sentences incomplete | **Fixed** (generated runs). |
| Ranges inconsistent (growth-share range without the Forbes floor) | **Fixed.** Both ranges use the same set of estimates. |
| IPP double rounding | **Fixed** (stored with three decimals). |
| Forbes totals on mixed bases | **Stated** (euros when quoted, else dollars converted; 2021 a lower bound; 2024 from a July article). |
| "Whole g-percentiles" wording | **Fixed** (the next bin is split uniformly; a Pareto shape there moves 2024 by at most 0.02 points). |
| Smaller items (0.000095, growth-curve exclusion rule, ERFS method segments, plus signs, "0.90%", appendix H citation, DVF/Notaires comparison) | **Fixed.** |
| Five page cells off by one unit in the last digit | **Stated.** Shares are stored with six decimals; differences are below display precision. |

## Sources ([round2-review-sources.md](round2-review-sources.md))

| Finding | Action |
|---|---|
| "Removed before publication" not true (old figures in CSV notes, notes, README; archived reviews quote them) | **Fixed.** Old secondary-compilation values removed from CSV notes and notes; the Notaires rows and comparison removed from the prices note; README, DATA_LICENSES and the changelog now say the tables are not in the repository and that the round-1 reports, kept as written, quote some figures from them. |
| IPP ratios presented as IPP's own; IPP's own comparison omitted | **Fixed.** Labelled as our ratios from IPP's published means; IPP's own ratios (3.03, 1.82, Table A2) and its higher top-1% share (13.8% vs 10.8%, pp. 3 and 13) added; conclusion for the top 1% qualified. |
| Bottom and middle also revised between vintages | **Fixed.** Garbinti et al. (2016) table 1 read and added (poorest half 6.3% vs 5.0% today; middle 40% 38.4% vs 36.3%), in the data, the page's comparison table and the paper. |
| AI disclosure weakly placed; "peer review" and "independent" labels; same model for author and reviewers | **Fixed.** Labels changed; the page states the analysis was built with Claude; the shared-blind-spot caveat is in the paper, the reviews README and the page; CITATION.cff names the maintainer alias, both licences and the AI assistance. |
| Appendix H citation still "2021" | **Fixed** (WID WP 2016/6, 2016 rev. 2017). |
| No licence for the project's own data | **Fixed.** `data/manual/` and `site/data/france.json` under CC BY 4.0 as our compilation; quoted facts attributed to producers. |
| Self-hosted fonts never loaded (wrong relative path) | **Fixed.** |
| WP 2016/5 title; unverifiable Landais English version; health allocation described two ways; weak rich-list sources; stale lines; outdated data inventory | **Fixed.** Title corrected; English version removed; health described as close to lump-sum everywhere; weak sources flagged in the rich-list note; stale lines removed; inventory rewritten. |
| Repository and Pages not yet public | Published with this version. |
