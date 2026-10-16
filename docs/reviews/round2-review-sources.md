# Round 2 source, provenance and framing review

Review date: 2026-10-16. The repository is at version 0.4.

**Scope.**
- Top-level files: `README.md`, `paper/paper.md`, `DATA_LICENSES.md`, `LICENSE`, `LICENSE-DOCS.md`, `CITATION.cff`, `CONTRIBUTING.md`.
- Docs: `docs/*.md` and `docs/notes/*.md`, including the new `docs/notes/rich-lists-sources.md`.
- Page: the static text of `site/index.html` and the sentences its JavaScript generates.
- Data: `data/manual/*.csv` and the `rich_lists` block of `site/data/france.json`.

The reviewer is a separate AI agent (Claude). It had the round-1 report (`review-sources.md`) and the response (`response.md`). Nothing outside this file was modified.

**Method.**
- **Citations.** Bibliographic fields were checked against Crossref (`api.crossref.org/works/<doi>`), the NBER page, or the title page of the working-paper PDF.
- **Claims.** Each was checked against the passage in the source; the verdict names the URL and quotes the passage.
- **Rich-list rows.** Every `source_url` / `quote` pair in both CSVs (48 pairs) was fetched and matched against the page text by script. Then 16 rows were read by hand to confirm that the number in the cell is the one in the quote and that it belongs to the right edition.
- **robots.txt.** Each host's robots.txt was read before its pages were fetched. Hosts that disallow Claude agents were consulted only through web.archive.org copies already cited in the CSV.
- **Rebuild.** `pipeline/build_data.py` was run on the existing `data/raw/` and the output compared with the committed files; the test suite was run.

**Not done.**
- `pipeline/fetch.py` was **not** run, so the downloads themselves were not re-tested.
- This is not legal advice. Statements about licences describe what the producers' published terms say.

Verdicts: **V** verified · **P** partially verified or worded more strongly than the source · **NF** not found · **C** contradicted · **NC** not checked.

---

## Verdict in one paragraph

The rich-list rebuild is real and careful.
- No API- or IdO-derived value is left in any value cell of either rich-list CSV or of `france.json` `rich_lists`. The JSON matches the CSVs cell for cell. Three `note` cells still mention old IdO totals (C1).
- All 48 quotes appear verbatim on their pages (47 exactly, 1 after removing punctuation).
- Every value host allows Claude agents in its robots.txt.
- `build_data.py` on the current raw files reproduces `site/data/france.json` and `paper/numbers.json` byte for byte (apart from the build date), and the 23 Python tests plus the node test pass.
- Every new reference checks out against Crossref or its title page, except one wrong title and one unverified English edition.

The problems are elsewhere.
1. **The public statement that Forbes-API, Observatoire and Notaires data "were removed before publication" is not true of the published repository.** The review reports in `docs/reviews/` still contain dozens of figures computed from the Forbes API and the Observatoire table. A Notaires price row is still in `docs/notes/prices-housing.md`. The README still says Challenges figures come "via the Observatoire des inégalités".
2. **The IPP comparison is misattributed, and its top-1% conclusion leaves out IPP's own reading.** The WID/IPP ratios are the project's own calculation, not IPP's. In shares, IPP find their top 1% (2016) 27% *higher* than Garbinti et al.'s series (2014).
3. **"The bottom and middle are robust" leaves out evidence the project already holds.** The same team's 2016 estimate for 2014 puts the poorest half at 6.3%, against 5.0% in today's vintage.
4. **The AI disclosure is honest but not prominent, and labels undercut it.** "Peer review" and "independent reviews" appear in the README, the method doc and the changelog. The page never says the analysis itself was produced with an AI. Author and reviewers are the same model.

---

## 1. Status of round-1 findings

| Round-1 item | Response says | Status now | Evidence |
|---|---|---|---|
| C1 health allocation | Fixed | **Fixed, with a leftover inconsistency** | The page and the paper say "health close to lump-sum". `docs/03-method.md` §3.10 says Fisher-Post & Gethin allocate health "by a usage profile". See m1. |
| C2 Forbes calibration reach | Fixed | **Fixed** | 1988 is now stated everywhere. TN 2025/01 §3.3 p.4: "We harmonize historical billionaire sources published by Forbes between 1988 and 2024." Small overstatement in m2. |
| C3 30% pre-committed source | Fixed | **Fixed** | `references.md` [INSEE-c1358], [INSEE-T2103]. |
| C4 "transfer" vocabulary | Fixed | **Fixed** | No "moved / transfers" on the page. The decomposition note is under the chart. |
| C5 IPP overclaim | Fixed | **Partly.** The 2023 column is now labelled, but a new misattribution appears and the conclusion still overreaches | See M1. |
| M1 `diinc` attribution | Fixed | **Fixed** | Fisher-Post & Gethin are cited on the page and in `02-data` §2.2. |
| M2 "one methodology" | Fixed | **Fixed** | `02-data` §2.2 point 3. |
| M3 Appendix H citation | Fixed | **Not fixed in `docs/03-method.md`** | Line 176 still reads "Garbinti, Goupille-Lebret & Piketty (2021, appendix H)". The paper, `references.md` and `rich-lists.md` are correct. See M4. |
| M4 secondary sources for votes | not listed | **Partly** | `rich-lists.md` refs 17–18 still link lcp.fr, publicsenat.fr and datan.fr. The official scrutins are named but not linked. |
| M4 "0,2 % … 37 foyers" | not listed | **Open** | `top_wealth_estimates.csv` still says IPP Note 92 "contains no such figure". This review found it nowhere in the note's text layer either. The charts are vector, so "not found in the note's text" is the supportable wording. |
| M5 counter-evidence prominence | Fixed | **Fixed for the top 5% (DWA). Open for vintages at the bottom** | See M2. |
| M6 missing sources | Fixed | **Fixed** | All added references were verified (§4). |
| M7 discontinuity as a finding | Fixed | **Fixed** | Labelled "most likely"; both readings given. |
| M8 contradictions between docs | Fixed | **Fixed** | `rich-lists.md` §3 now matches `dwa.md`. |
| M11 undefined citation keys | Fixed | **Fixed** | [Vermeulen2018], [BTZ2019] and [IPP2023] are now in `references.md`. |
| M9 licensing | Open → done in 0.4 | **Mostly done, but the "removed" statement is inaccurate** | See C1 and M5. |
| M10 Challenges from one table | Open → rebuilt | **Done** | Every row now has its own article and quote (§5). |
| Minor: CASD wording (doc 04) | not listed | **Open** | Four points are still unchanged: "without saying whether that means this grid" (the grid *is* labelled "Tarif subventionné"); "needed producer agreement by 13 October" (that is the deadline to *request* it); no "à concurrence de 3 ans" cap on export credits; DWA "Quarters after 2023-Q3 will be revised" is not labelled as inference. |
| Minor: "Paris region" | Fixed | **Partly** | Docs say "urban unit". The chart titles and paper §5.5 still say "outside the Paris region". Acceptable as a plain-language label if the note defines it. |

---

## 2. Ranked issues

### Critical (fix before the repository is made public)

**C1. "Removed before publication" is not true of the published repository.**

*Where the claim is made:*
- `README.md` "Data provenance and licences": "Earlier, unpublished versions used tables whose terms do not allow redistribution (Forbes API data, an Observatoire des inégalités table, a Paris Notaires table); they were removed before publication."
- The same sentence in `DATA_LICENSES.md`.
- `CHANGELOG.md` 0.4.0.
- `docs/notes/rich-lists-sources.md` line 8: "IdO links and figures … were removed."

*Evidence that values remain:*

1. **Forbes API figures in the review archive.** These files are published, and `docs/reviews/README.md` says reports "are kept as written".
   - `docs/reviews/review-sources.md` line 634: a table of counts and dollar totals for six years, labelled "recomputed from Forbes API".
   - The same file, lines 139–156: a 2014 Forbes total, the size of the 2013 list, named individual fortunes with amounts, and the total of the 2014 newcomers, all from the API. Line 596: citizens abroad counted from the API `city` field.
   - `docs/reviews/review-numbers.md` lines 136, 169, 193–194 and 394–395: Forbes totals and counts for 2005, 2013–2014, 2019–2021 and 2024 taken from the old API-built CSV.
   - `docs/reviews/review-methodology.md` line 213: a 2024 Forbes total described as the "project's own sum of `finalWorth`".
2. **Observatoire des inégalités figures.**
   - `docs/reviews/review-sources.md` line 620 says IdO table 2646 matches the old CSV for all 30 years.
   - `review-numbers.md` line 143 reproduces old Challenges rows from that table.
   - Three IdO-only totals (for 2014, 2016 and 2018) are still quoted in the current files. They appear in the `note` cells of `data/manual/challenges_500.csv` (rows 2014, 2016, 2018), and therefore in `site/data/france.json` (three occurrences of "Observatoire"), in `docs/notes/rich-lists.md` line 17 ("Older compilations also give …"), and in `rich-lists-sources.md` lines 41–43.
3. **Paris Notaires figures.**
   - `docs/notes/prices-housing.md` line 79 has a row "Paris (Notaires-INSEE)" of eight annual €/m² levels taken from the removed table.
   - Line 8 still lists `data/manual/notaires_idf_apartment_prices_m2.csv` as an input, although the file no longer exists.
   - Line 67 documents `notaires_*` keys that the build no longer produces.
   - Line 247 links the Notaires PDF.
   - The cross-check "DVF 1.9–4.7% above Notaires" (`prices-housing.md` lines 85 and 192; `docs/03-method.md` §3.9 lines 267–269) can no longer be recomputed from the repository. That contradicts "every number below was recomputed from the downloaded files" (`prices-housing.md` line 9).
   - `pipeline/sources/housing.py` still loads the Notaires CSV if it is present. That is harmless, but it is dead code.
4. **README "Sources".** Line 99 says: "Challenges … (via the Observatoire des inégalités and press articles)." That is no longer true.

*Why Critical.* The legal exposure of a few dozen figures inside review reports is probably small. They are short factual citations inside critical commentary. But the README makes an unqualified public statement about provenance and licensing, and the repository contradicts it. That is the kind of error a hostile reader will use against the whole project.

*Fix (either one):*
- (a) Redact the API- and IdO-derived values from the archived reports, replacing them with "[value from an earlier, withdrawn data version]". Delete the Notaires row and keys from `prices-housing.md`. Drop the three IdO totals from the notes, or say "an earlier compilation gave a different figure".
- (b) Keep the archives intact and change the statement to say so: "Earlier versions used … These data are no longer in `data/` or in the build; the archived review reports in `docs/reviews/` quote some figures from them as they were reviewed."

In both cases, fix README line 99. Mark the Notaires cross-check as "computed in version 0.3 from a table no longer in the repository", or remove it.

### Major

**M1. The project's own WID/IPP ratios are attributed to IPP, and the top-1% conclusion leaves out IPP's own reading.**

*Where:*
- `paper/paper.md` §5.4: "IPP finds 2.7 times WID's amount for the top 0.001% … WID therefore likely understates the income of the very top, not of the top 1% as a whole."
- The page, `renderIPP()`: "This suggests WID understates the income of the very top, while the top 1% as a whole is not understated."
- `docs/03-method.md` §3.8, lines 248–252: "IPP's 2025 paper finds 2.7× WID's amount…".
- `docs/01-concepts.md` line 129: "IPP find that following actual ownership chains gives the very top 1.7–2.7× more income [BBGM2025]".
- `docs/03-method.md` §3.10 table.

*Evidence:*
1. **IPP never compares its figures with WID's.** The ratios 2.7, 1.7, 1.13 and 0.87 are the project's own: IPP comprehensive income in euros divided by WID pre-tax income in euros. That is a legitimate calculation, but it must be presented as ours.
2. **IPP's own ratios are different numbers.** Comprehensive versus DINA-style dividend-imputed income is 3.03 for the top 0.001% and 1.82 for the top 0.01%. They are computed on the same data, so the denominators do not differ. Source: Bach, Bozio, Guillouzouic & Malgouyres, RFBerlin DP 70/25, Table A2, column "Ratio inc. sh." (<https://www.rfberlin.com/wp-content/uploads/2025/09/25070.pdf>).
3. **IPP's own reading of the top 1% points the other way.**
   - p.3: "Garbinti et al. (2018) obtain a top 1% share of 10.8% for 2014 (vs 13.8% for our estimates) and 3.7% (vs 6.2% in our data) for the top 0.01%".
   - p.13: "Our estimates imply a higher share of the top 1% … whereas our estimate is 13.8%, corresponding to a 27% increase … the corresponding top 1% share with the DINA dividend-based imputation … is 13.0%."
   - So in shares, IPP find the DINA-type top 1% *too low*. Their comparison is not like for like: their 13.8% is for 2016, against GGP 2018's 10.8% for 2014, an older series and a different year. This is counter-evidence the paper leaves out, not a proof that WID is wrong.
   - WID's top 1% is larger in euros (0.87×) because its income concept is broader: national income of about €1.9 tn, against IPP's household comprehensive income of about €1.25 tn. In shares of each source's own total, IPP's top 1% is larger. Stating "the top 1% as a whole is not understated" as a finding picks one of the two views.

*Fix:*
- Write "Comparing IPP's euros with WID's, **we** find…".
- Add: "In shares of their own totals, IPP put the top 1% at 13.8% against 10.8% in Garbinti et al. (2018), and say measuring retained earnings directly is a key reason (IPP 2025, pp. 3, 13). Whether WID understates the top 1% therefore depends on the denominator."
- In `01-concepts` §1.6, use IPP's own 1.8×–3.0× (comprehensive vs dividend-imputed, Table A2), or attribute 1.7–2.7× to the project.

**M2. "The bottom and middle are robust across sources" leaves out the same-team revision at the bottom.**

*Where:*
- `paper/paper.md` abstract ("The bottom and middle of the distribution are robust across sources") and §5.3.
- The page tile "How sure are we?" ("Sources agree on the poorest half, not on the very top").
- The "Same year, two estimates by the same team" table, built from `D.vintages`.

*Evidence:*
- GGP WID WP 2016/5, Table 1 (2014), read on the title-page PDF from wid.world: bottom 50% **6.3%**, middle 40% **38.4%**.
- The vintage used here (`site/data/france.json`, 2014): bottom 50% **4.99%**, middle 40% **36.31%**.
- So the poorest half's 2014 share was revised down by about a fifth (−1.3 points), about a third of its whole 1990–2024 decline in this vintage (8.9% → 4.8%, −4.1 points).
- Only a small part of this can be the Forbes top-up. TN 2025/01 §3.3 takes the added amount proportionally from the rest of the distribution, so a top-up of about 2–2.5% of total wealth lowers a 6.3% share by at most about 0.15 points. Most of the revision comes from other changes (the JEEA 2021 final series, national-accounts revisions, the refit), which the project does not document.
- The project's `vintages` table and `top_wealth_estimates.csv` keep only the top 1%, 0.1%, 0.01% and 0.001% rows of that Table 1. The bottom rows are not shown.
- The DWA agreement on the bottom 50% (−0.6 to +0.4 points) is real. It is one source agreeing with the current vintage, not proof of robustness.

*Fix:*
- Add the bottom 50% and middle 40% rows to the vintage table and to `top_wealth_estimates.csv` (same page, same table).
- Change the abstract to "The bottom and middle agree across today's sources (ECB / Banque de France); earlier vintages of WID itself put the poorest half higher (6.3% vs 5.0% in 2014)."

**M3. The AI disclosure is clear where it appears, but not prominent, and is undercut by "peer" and "independent" labels.**

*Where it is good:*
- `paper/paper.md` §8 ("These are not peer reviews by outside experts").
- `docs/reviews/README.md`.
- Page section 11 ("They are not peer review by outside experts").
- The README intro ("so far by AI reviewer agents").

*Problems:*
- **Labels that contradict the disclosure:**
  - `README.md` line 125: "Peer review: four reviews, second round, responses".
  - `README.md` line 56: "Four independent reviews".
  - `docs/03-method.md` line 5: "Version 0.3 follows four independent reviews". It is also stale; this is version 0.4.
  - `CHANGELOG.md`: "Second round of independent reviews".
- **The page never says that data collection, code and text were produced with an AI** (Claude). It discloses only that the *reviews* were AI. The README and the paper say so only in their last sections.
- **Author and reviewers are the same model family.** README: "That is why the reviews were made independent and adversarial". The reviewers can share the author's blind spots; for example, both may trust the same misread source. That should be said in one line. "Independent" is not accurate in the usual sense.
- **`CITATION.cff`:**
  - No human is named; the maintainer handle appears only in the paper's front matter.
  - There is no AI statement and no `abstract`.
  - It uses `type: software` and `license: MIT` for what is cited as a working paper whose text is CC BY 4.0.
  - Accountability for a public document that names living people (rich-list rows) and discusses a live tax debate would be clearer with a named, contactable maintainer.

*Fix:*
- Replace "Peer review" with "Reviews (AI agents)" and "independent" with "separate".
- Add one line under the page title or in the footer: "Built with Claude (Anthropic) under the maintainer's direction; reviewed by separate Claude agents, not by outside experts."
- Move the paper's AI paragraph into the front matter or the first page.
- In `CITATION.cff`, add a `preferred-citation` of `type: report`, list the licences (`MIT` and `CC-BY-4.0`), and name the maintainer (or the GitHub handle as `alias`).

**M4. One round-1 citation fix reported as done is not done.**
- `docs/03-method.md` line 176: "Garbinti, Goupille-Lebret & Piketty (2021, appendix H) split each Challenges family into 1, 10 or 15 members…".
- Appendix H is in the 2016 data appendix, WID WP 2016/6. Its title page reads "Accounting for Wealth Inequality Dynamics … APPENDIX … December 2016 … Last Revised: January 27, 2017", and §H.2 is on p.52. It is not in the JEEA 2021 paper.
- `response.md` lists round-1 M3 as **Fixed**.
- Fix: "(2016, rev. 2017; WID WP 2016/6, appendix H)".

**M5. The project's own data compilation has no stated licence, and the licence scope overlaps.**
- **Own compilation unlicensed.** `LICENSE` says `site/data/france.json` "is data … see DATA_LICENSES.md". `DATA_LICENSES.md` lists only third-party terms. Nothing says on what terms others may reuse the project's own work: the derived series, the scenario outputs, and the `data/manual/*.csv` compilations (URLs, notes, page references). A reuser cannot tell whether the CSVs may be redistributed.
- **`index.html` under two licences.** `LICENSE` puts `site/*.html` under MIT. `LICENSE-DOCS.md` puts "the explanatory text of the page" under CC BY 4.0. Only LICENSE-DOCS mentions the carve-out.
- **Quote columns.** The `quote` columns reproduce short press passages (≤ 25 words, attributed). That is defensible as short quotation for information (French CPI art. L122-5 3° a) requires naming the author and source), but no file states the basis.
- *Fix:*
  - State a licence for the project's own data contributions (for example CC BY 4.0 for `data/manual/*.csv`, excluding quoted passages and third-party figures, and the same for derived series in `france.json`, "subject to producers' terms").
  - Add to `LICENSE`: "except the explanatory text of `site/index.html`, see LICENSE-DOCS.md".
  - Add one line in DATA_LICENSES on the quotes.

### Minor

- **m1. Health allocation is described two ways.**
  - The page cross-check note says "health is close to the same amount per person in both"; the paper §5.2 says "health close to lump-sum … in WID".
  - `docs/03-method.md` §3.10 says "WID (Fisher-Post & Gethin 2023) attributes health by a usage profile".
  - Round 1 (Fisher-Post & Gethin 2023, pp.12–13) found health allocated by observed incidence (Gethin 2023) in the series actually used. "Close to lump-sum" is the DINA-Guidelines benchmark (p.70).
  - Use one wording: "by observed use, which is close to equal per person".
- **m2. The calibration wording slightly overstates TN 2025/01.**
  - Paper §4: "WID raises its top g-percentile to the Forbes billionaire total from 1988".
  - The note says "In cases where WID billionaire wealth is lower than Forbes … We leave WID benchmark series unchanged otherwise". It adds a "second correction" within the 127th g-percentile, and the comparison is with billionaire wealth (gpinter), not the top-0.001% total.
  - The page glossary ("at least what Forbes counts") is accurate; align the paper and `03-method` §3.7 with it.
- **m3. `references.md` [GGP2016-T1] has the wrong title.**
  - The WID WP 2016/5 title page reads "Accounting for Wealth Inequality Dynamics: Methods, Estimates and Simulations for France (1800-2014)", December 2016, first version 12 July 2016, last revised 27 January 2017.
  - "Wealth Concentration in France 1800–2014" is only the wid.world URL slug. (The CSVs name the source correctly as "WID WP 2016/5".)
- **m4. Landais "English version … PSE WP 2009" is unverified.** The French June 2007 PSE paper is verified at the INSEE URL. No English PSE 2009 edition was found (a later reference list cites "Landais (2009)"). Write "an English version circulated later" or drop it.
- **m5. Page reference list.**
  - "Bach, Bozio, Guillouzouic, Malgouyres (2025). Do Billionaires Pay Taxes?" has no venue (RFBerlin Discussion Paper 70/25).
  - Fisher-Post & Gethin (2023), which the method text cites, is not in the list.
  - The tile "first and latest estimates by the same research team" is loose. The current vintage is WIL's (Bajard et al. 2025) on top of GGP 2021. Say "an earlier estimate by the same research programme".
- **m6. `rich-lists-sources.md` and `rich-lists.md` small inconsistencies.**
  - Line 63 says `france.json` "keeps old values until rebuilt". It has been rebuilt: the JSON matches the CSVs, and the scenario years are 14 and 8 as stated.
  - Line 20 says "Nothing exists for 2001–2016"; `rich-lists.md` line 26 says "2010–2016".
  - The robots wording "Disallowing hosts include challenges.fr" is conservative. challenges.fr disallows ClaudeBot, anthropic-ai and Claude-SearchBot but not Claude-User. That is fine as a rule, but say "disallow Claude crawlers".
  - The README's "no data were scraped" should say "no database or API was scraped; figures were read from individual articles". An agent fetched the pages automatically.
- **m7. Two weak rich-list sources.**
  - 2025 Challenges threshold 245 comes from a Substack newsletter (dimanche7, 13 July 2025): "Le ticket d'entrée grimpe à 245 millions". 2024 is also 245 (AFP), so "grimpe" suggests the figure may be stale. Flag it as weak in the note.
  - 2012 rests on a blog that reposts Challenges' article verbatim (habarizacomores.com), possibly an unauthorised copy. It is already flagged "WEAK SOURCE". Prefer a web.archive.org copy of the challenges.fr 2012 article if one exists.
- **m8. `top_wealth_estimates.csv`.** "which contains no such figure" should read "not found in the note's text (figures not checked)". See the round-1 status table.
- **m9. Doc 04 wording, carried over from round 1.** The CASD items listed in the status table. The "8%" is now attributed to IPP and is accurate (DP 70/25 p.13: "only 8% of their real comprehensive income"); consider adding that at group level the dividend-imputed mean is 24% of comprehensive income for the top 75 (Table A2: 51.8 m vs 217.3 m).
- **m10. Stale data inventory in `docs/02-data-france.md`.**
  - §2.3 lists `insee_hpi.xml` (idbank 010567059) as fetched by `fetch.py` and the WID download as "~10 MB". `response.md` (code m10) says HPI was removed from `fetch.py`; the raw file is now `housing/insee_hpi_regions.xml`.
  - §2.1 lists "IPC by household category … incl. by income quintile … Plan", while `prices-housing.md` says INSEE publishes no CPI by quintile and the page already uses CPI by decile.
- **m11. "WID reports are CC BY-NC-SA 4.0"** (`DATA_LICENSES.md`) could not be verified on wid.world. Cite the page or drop the clause.
- **m12. Hero caption.** "…as much as the poorest 51.9% of adults put together, many of whom own very little or owe more than they own" is accurate, but its rhetorical register is stronger than the rest of the page. Optional: keep the comparison and drop the clause.
- **m13. Version and date drift.** `docs/03-method.md` line 5 says "Version 0.3". `CITATION.cff` `date-released: 2026-10-16` predates the actual public release.
- **m14. The post-2014 calibration inference is sound, but one phrase overreaches.**
  - `docs/03-method.md` §3.7 lines 149–151: "Over 2014–2024 the layers just below the top 0.001% are flat while the top 0.001% rises from 3.39% to 5.58%, which points to the calibration rather than a broad rise in top fortunes." Paper §5.3 item 3 says the same more cautiously.
  - After 2014, WID fixes "the asset composition by percentile to 2014" (TN 2021/16, version of 13 Jan 2022, p.3). Each g-percentile then moves only with the national totals of the assets it holds. The finest composition published in `WID_data_FR.csv` (`ahwbusj992`, `ahwfinj992`, `ahwhouj992`) is p99.9p100, so the mix inside the top 0.1% cannot be checked from public data. But the layers just below the top 0.001% are, like it, dominated by business and financial assets (round-1 `review-methodology.md`, C3), so without a correction they would move broadly together. A divergence of this size then points to the Forbes top-up. The inference is reasonable.
  - What overreaches is "rather than a broad rise in top fortunes": after 2014, WID's method cannot detect such a rise either way. Write "points to the calibration; WID's post-2014 method cannot show whether fortunes just below the top rose", and cite TN 2021/16 for why the neighbouring layers are flat.
- **m15. The self-hosted fonts never load.** `site/fonts/fonts.css` uses `url(fonts/X.woff2)`, which the browser resolves relative to the stylesheet, i.e. `site/fonts/fonts/X.woff2`. Served locally, that path returns HTTP 404 and `site/fonts/X.woff2` returns 200. The page silently falls back to system fonts. Use `url(X.woff2)`. The licences are fine (§3).

---

## 3. Provenance and licensing checks (task 1)

| Check | Result |
|---|---|
| Rich-list CSVs contain no API or IdO value | **V** for values. Every numeric cell is in its row's quote. All `source_url` hosts are press, Sénat, Forbes France via web.archive.org, or Challenges via web.archive.org. No `forbesapi` or `inegalites.fr` URL remains. The `note` cells still name three IdO totals (C1). |
| `france.json` `rich_lists` equals the CSVs | **V.** Script comparison: every key and value of each JSON row equals the CSV cell. Only years with a euro total (Challenges) are carried. No `forbesapi`, `inegalites` or `notaires` string anywhere in the JSON. |
| Every row has `source_url` + `quote` | **V.** Challenges 30 rows (1996, 1998–2026), Forbes 9 rows (2017–2025); 48 URL–quote pairs. |
| Quotes match the pages | **V** for 48/48 (47 verbatim after whitespace and quote-mark normalisation, 1 after punctuation stripping: the 2004 table row on permanent.nouvelobs.com). |
| Value hosts allow Claude agents (robots.txt) | **V.** All 21 value hosts (20 sites plus web.archive.org) allow ClaudeBot, Claude-User, Claude-SearchBot and anthropic-ai on the cited paths. fr.fashionnetwork.com explicitly allows them for "recherche / citation" and blocks training bots. challenges.fr disallows ClaudeBot, anthropic-ai and Claude-SearchBot and is used only through web.archive.org (2008 row). forbes.fr is used only through web.archive.org. |
| README / DATA_LICENSES statements | **C** for "removed before publication" (C1) and README line 99. **V** for "Raw downloads are not redistributed": `.gitignore` has `data/raw/`. **V** for the IPP row count (21). |
| IPP CSV limited to quoted figures | **V.** 21 rows, each with a page or table reference. All values checked against the PDFs: Note 92 revised (Tableau 1: 580 000; 3 385 000; 23 530 000; 171 822 000), RFBerlin DP 70/25 Table 1 (8 values), Table A2 (4 values), abstract and §4.2 ("almost 45%", "roughly 25%"), p.14 ("close to 85%"). Every row is used somewhere: page, paper, `03-method` §3.8, `rich-lists.md` §4 or doc 04. |
| Fonts | **V licence / C loading.** Both OFL-1.1 texts are present with the upstream copyright lines (Bricolage Grotesque Project Authors 2022; Newsreader Project Authors 2020); no Reserved Font Name is declared, so subsetting is allowed. **But** `site/fonts/fonts.css` uses `url(fonts/X.woff2)`, which resolves relative to the stylesheet, i.e. `site/fonts/fonts/X.woff2`. Served locally that is HTTP 404, and `site/fonts/X.woff2` is 200. The self-hosted fonts never load and the page falls back to system fonts. Use `url(X.woff2)`. DATA_LICENSES' privacy statement (no request to third-party font servers) remains true. |
| MIT / CC BY scoping | **P** (M5): overlap on `index.html`, no licence for the project's own data, `CITATION.cff` gives MIT only. |

## 4. Citations added since round 1 (task 2)

| Reference | Where | Checked against | Verdict |
|---|---|---|---|
| Bozio, Garbinti, Goupille-Lebret, Guillot, Piketty (2024), *AEJ: Applied* 16(2):31–65, doi:10.1257/app.20220023 | references.md, page, paper | Crossref: same title, authors, volume, issue, pages; issued 2024-04 | **V** |
| Blanchet, Chancel, Gethin (2022), *AEJ: Applied* 14(4):480–518, doi:10.1257/app.20200703 | references.md, paper | Crossref | **V** |
| Auten, Splinter (2024), *JPE* 132(7):2179–2227, doi:10.1086/728741 | references.md, page, paper | Crossref | **V** |
| Saez, Zucman (2020), "Trends in US Income and Wealth Inequality: Revising After the Revisionists", NBER WP 27921 | references.md, page | nber.org/papers/w27921: October 2020; the abstract discusses Auten & Splinter (2019) | **V** (it replies to the 2019 version of Auten & Splinter; say so) |
| Landais (2007), "Les hauts revenus en France (1998–2006) : une explosion des inégalités ?", PSE, June 2007 | references.md | INSEE-hosted PDF: title page "Camille Landais, Paris School of Economics, Juin 2007" | **V** (the English 2009 edition is **NF**, m4) |
| Fisher-Post, Gethin (2023), WID WP 2023/17 | references.md, page, paper | WIL PDF `WorldInequalityLab_WP2023_17_Government-Redistribution-and-Development` | **V** |
| Bajard et al. (2025), WIL TN 2025/01, "updated 18 Dec 2025" | references.md, page, paper | Title page: seven authors as listed, "This version: December 18, 2025"; §3.3 p.4 Forbes 1988–2024, 127th g-percentile | **V** |
| Blanchet, Martínez-Toledano (2021), WIL TN 2021/16, "Distributional Wealth Accounts in Europe: Methodology" | references.md, rich-lists.md | Title page: "Technical Note N° 2021/16 … First version: December 7, 2021; This version: January 13, 2022"; the quote at p.3 matches | **V** (cite the 2022 version) |
| GGP WID WP 2016/5, Table 1 (0.9% in 2014) | references.md, paper, page | Title page; Table 1 "Top 0.001% … 517 … 87 227 640 € … 180 329 356 € … 0,9%" | **V** value; **C** title (m3) |
| GGP WID WP 2016/6, Appendix H (1/10/15 members, 80% married, 20% non-resident) | references.md, rich-lists.md, paper | Title page "APPENDIX … Last Revised: January 27, 2017"; §H.2 pp.51–53 | **V** (but `03-method` line 176 still says 2021, M4) |
| DINA Guidelines, Oct 2025, coordinators Chancel, Flores, Moshrif, Nievas, Piketty | references.md | wid.world document page and search record: "VERSION: OCTOBER 2025"; coordinators as listed | **V** |
| Vermeulen (2018), *RIW* 64(2):357–387 | references.md | Crossref doi:10.1111/roiw.12279 (published online 2017) | **V** (add the DOI) |
| Bach, Thiemann, Zucco (2019), *ITAX* 26(6):1234–1258 | references.md | Crossref | **V** |
| GGP 2021 *JEEA* 19(1):620–663; BFP 2022 *RIW* 68(1):263–288 | references.md | Crossref | **V** |

## 5. Rich-list spot-check (task 1)

Script check: every quote fragment (split on " … " and " | ") was searched in the fetched page text. Result: 48/48 found (§3).

Hand check (16 rows): does the number in the cell equal the number in the quote, and does it describe that edition?

| CSV, year | Cell(s) | Source (host robots) | Passage read | Verdict |
|---|---|---|---|---|
| Challenges 2004 | total 153; No.1 14.246 | web.archive.org copies of lemagchallenges / permanent.nouvelobs (archive) | "153 milliards d'euros que représente le total des patrimoines de nos « 500 fortunes professionnelles »"; table row "1 1 14246 Bettencourt Liliane" | **V** |
| Challenges 2007 | 280; threshold 60; No.1 23 | webmanagercenter.com (allows) | "de 200 à 280 milliards d'euros … Pascal Lota … 60 millions … 23 milliards", AFP 11 Jul 2007 | **V** |
| Challenges 2012 | 267; 60 | habarizacomores.com (allows), dated 2012-07-12 | "il est resté collé à 60 millions … 267 milliards d'euros" (repost of Challenges' text) | **V**, weak source (m7) |
| Challenges 2013 | 329; No.1 24.3 | politis.fr (allows), 2013-07-12 | "Le rapport 2013 annonce une cagnotte de 329 milliards d'euros" | **V** (AFP's 330 is noted in the CSV) |
| Challenges 2014 | 390; No.1 27 | africanmanager.com (allows), 2014-07-10 | "atteignant une richesse globale de 390 milliards d'euros, selon le classement 2014 du magazine Challenges paru jeudi 10 juillet" | **V** |
| Challenges 2016 | 456; threshold 100 | 24matins.fr, lafinancepourtous.com (allow) | quotes found; "100 M€ pour le 500ème de la cuvée 2016" | **V** |
| Challenges 2018 | 650; 140; 73.2 | francesoir.fr (4 Jul 2018), gestiondefortune.com (6 Jul 2018) (allow) | "atteignant un record de 650 milliards d'euros, selon le classement 2018"; "Aujourd'hui, il en faut 140 M€" | **V** |
| Challenges 2022 | 1002 (retrospective) | luxus-plus.com (allows) | "reléguant loin derrière le record de l'année dernière à 1.002 milliards" in the 2023 article | **V** (retrospective, flagged) |
| Challenges 2024 | 1228; 245; 190 | fashionunited.fr (allows), 2024-07-18 | "les 500 plus grandes fortunes totalisent 1.228 milliards d'euros, 5% de plus qu'en 2023" | **V** |
| Challenges 2025 | 1128; 245; 163 | fashionunited.in (allows); dimanche7.substack.com (allows), 2025-07-13 | "reached 1,128 billion euros in 2025"; "Le ticket d'entrée grimpe à 245 millions d'euros" | **V** total; threshold **P** (m7) |
| Challenges 2026 | 1076; 250; 121.2 | fashionunited.fr; lyoncapitale.fr (allows), 2026-07-09 | "fortune minimale d'inclusion de 250 millions d'euros … 1 076 milliards d'euros, contre 1 279 milliards l'année dernière" | **V** (Lyon Capitale's 1 279 for 2025 is flagged as an outlier in the CSV) |
| Forbes 2017 | n 39; $245 bn; €228 bn | journaldeleconomie.fr (allows), 2017-03-20; web.archive.org copy of europe1.fr | "Les grosses fortunes françaises pèsent 245 milliards de dollars"; "(environ 228 milliards d'euros)" | **V** |
| Forbes 2020 | n 39; €277 bn | web.archive.org copy of forbes.fr | "pour un montant total de près de 277 milliards d'euros" | **V** ("près de" kept in the quote) |
| Forbes 2021 | n 42; $510 bn; €450 bn | fashionunited.fr; lequotidiendupharmacien.fr (allow; second page undated) | "un peu plus de 510 milliards de dollars"; "42 milliardaires … plus de 450 milliards d'euros" | **V**, but the second article carries no date; it is attributed to 2021 from its content (Bancel's entry) |
| Forbes 2022 | n 43; $550 bn | web.archive.org copy of forbes.fr, 7 Apr 2022 | "Nombre de milliardaires : 43 (contre 42 en 2021) Fortune nette totale : 550 milliards de dollars" | **V** |
| Forbes 2024 | n 53; €624 bn | web.archive.org copy of forbes.fr (article 2024-07-30); boursorama.com (allows) | "dix nouveaux noms … le club restreint des milliardaires qui cumule désormais 624 milliards d'euros"; "53 fortunes françaises" | **V** |

Rows not hand-checked beyond the script match (all found): Challenges 1996, 1998–2003, 2005, 2006, 2008–2011, 2015, 2017, 2019–2021, 2023; Forbes 2018, 2019, 2023, 2025.

## 6. Claim check: paper and page (task 3)

Values computed from data (shares, the decomposition, scenario results) were rebuilt, not re-derived. `build_data.py` on the current raw files reproduces `france.json` and `paper/numbers.json` exactly. The table below covers claims that rest on an external source.

| # | Claim | Where | Verdict | Source and passage |
|---|---|---|---|---|
| 1 | WID harmonises Forbes 1988–2024 and adds the gap to the 127th g-percentile | paper §4, §5.3; page; 03-method §3.7 | **V** (wording **P**, m2) | TN 2025/01 §3.3 p.4: "We harmonize historical billionaire sources published by Forbes between 1988 and 2024 … In cases where WID billionaire wealth is lower than Forbes, we add to the 127th g-percentile …" |
| 2 | Raw uncorrected French estimates underestimate billionaire wealth | rich-lists.md §2 | **V** | TN 2025/01 p.8: "our raw uncorrected estimates for countries like France or Britain significantly underestimate billionaire wealth" |
| 3 | Earlier estimate: top 0.001% 0.9% in 2014 | paper abstract, §5.3; page tile | **V** | WID WP 2016/5, Table 1 |
| 4 | After 2014, asset mix by percentile fixed at 2014 | paper §7; 02-data; 03-method §3.11 | **V** | TN 2021/16 p.3 (quoted in m14) |
| 5 | Flat layers below show the calibration drives the rise | 03-method §3.7; paper §5.3(3) | **P** | The inference is reasonable (with a fixed post-2014 asset mix, business-heavy neighbouring layers would move with the top unless the top-up is added); "rather than a broad rise in top fortunes" overreaches (m14) |
| 6 | Bottom and middle robust across sources | paper abstract; page tile | **P** | DWA agrees; the GGP 2016 vintage differs (M2) |
| 7 | GGP appendix H: 1/10/15 members, 80% married, ~20% non-resident | paper §4; 03-method; rich-lists | **V** | WID WP 2016/6 §H.2 p.52: "each family include 1, 10 or 15 members … 80% of these individuals are married … around 20% of the total wealth" |
| 8 | Post-tax: health close to lump-sum, education and collective spending proportional | paper §5.2; page | **P** (m1) | DINA-G Oct 2025 p.70 (benchmark, **V** in round 1); Bozio et al. 2024 p.16 (**V** in round 1); the vintage used allocates health by incidence (FPG 2023 pp.12–13) |
| 9 | Post-tax 2019+ repeats 2019 ratios | paper §7; page | **V** | WID metadata for `adiinc`/`sdiinc` (round 1) |
| 10 | IPP finds 2.7×, 1.7×, 1.13×, 0.87× WID | paper §5.4; page; 03-method §3.8 | **C** (attribution) | The ratios are the project's; IPP compares with dividend imputation (Table A2: 3.03, 1.82, 1.27, 1.07) |
| 11 | WID not understating the top 1% as a whole | paper §5.4; page | **P** (true in euros; IPP's own reading in shares is the opposite, M1) | IPP DP 70/25 pp.3, 13: top 1% 13.8% (2016) vs GGP 10.8% (2014), "a 27% increase" |
| 12 | WID ≈ IPP dividend-imputed (€9.2 bn vs €8.1 bn top 0.001%) | paper §5.4; page | **V** (inputs) | Table A2: 21,474,000 × 378 = €8.12 bn |
| 13 | "IPP find … 1.7–2.7× more income" | 01-concepts §1.6 | **C** | As #10 |
| 14 | IPP: 75 richest tax households, 2016 | page §06; 01-concepts | **V** | DP 70/25 Table 1, P99.9998 row, 75 households |
| 15 | IPP: top 75 have about an 85% chance of being in the Challenges list | rich-lists §4 | **V** | DP 70/25 p.14: "being included in the top 500 list close to 85%" |
| 16 | IPP: tax rate about 45% at P99.9, about 25% for billionaires | `ipp_top_income.csv` | **V** | DP 70/25 abstract: "from about 45% at the 0.1% threshold to roughly 25% among billionaires" |
| 17 | Doc 04: the DINA rule captures about 8% of top-75 income | 04 §4.1 | **V** | DP 70/25 p.13: "only 8% of their real comprehensive income" |
| 18 | ECB / BdF top 5% 5.8–7.6 points below WID; bottom 50% −0.6 to +0.4 | paper §5.3; page | **V** (data) | Rebuilt from `DWA_FR_NWA.csv` |
| 19 | INSEE CND: bottom 50% 38% vs WID 32% (2019) | paper §5.2; page | **V** (round 1; data reproduces) | `insee.md`, IA88 / ip2022 xlsx |
| 20 | Pre-committed spending 13.4% (1959) → 30.3% (2025) | paper §5.5; page | **V** | INSEE table 2.103, base 2020 (8988851); round 1 read 30.3% (2025); 1959 from the same file |
| 21 | Paris urban area prices about 7% higher | page Limits; 01-concepts | **V** | INSEE Première 1959 (round 1) |
| 22 | DREES 2011: 61% vs 23% of disposable income | page prices note | **V** | DREES ER 1055 Table 1 (round 1; the link resets today, use a Wayback copy) |
| 23 | Challenges 500 ≈ 40% of GDP vs 6% in 1996 | `top_wealth_estimates.csv` | **V** | legrandcontinent.eu, 2 Jul 2025: "avoisine aujourd'hui l'équivalent de 40 % du PIB, contre 6 % en 1996" |
| 24 | Challenges 2024 total €1,228 bn (used by AN report 930) | page, 03-method | **V** | fashionunited.fr AFP 18 Jul 2024; AN 930 (round 1) |
| 25 | Forbes 2024: 53 billionaires, €624 bn | page; 03-method | **V** | forbes.fr via web.archive.org (§5) |
| 26 | Auten & Splinter is the main critique; Saez–Zucman reply | page; paper | **V** (characterisation is fair) | NBER w27921 abstract |
| 27 | "Same research team" for the 2016 and current estimates | page tile | **P** | The current vintage is WIL (Bajard et al. 2025) on GGP 2021 (m5) |
| 28 | Population 20+ doubled since 1900 | paper §7; page | **V** (data) | 26.8 m → 53.0 m (`npopuli992`) |
| 29 | Rich-list figures differ by a few percent between sources | paper §7; page | **V** | Conflicts listed in `rich-lists-sources.md`: 700/711 (2019), 1128/1129 (2025), thresholds 59/60, 39/40, 80/82; Lyon Capitale's 1 279 is an outlier |
| 30 | Votes on the "taxe Zucman": 116–39, 129–188, 172–228 | rich-lists §4 | **V** (round 1, official scrutins) | Still linked to secondary sites (status table) |

## 7. Framing and neutrality (task 4)

**Balance.** The paper and the page are much more balanced than version 0.2:
- Ranges for the top are shown.
- The ECB gap sits next to the headline.
- The decomposition is careful not to imply transfers.
- The "What this page does not say" box is a good model.

Remaining imbalances:
- **Wealth at the top: one-way scepticism.** The text gives several reasons the top may be overstated (Forbes coverage, the top-bin inconsistency) and several reasons it may be understated (rich lists as lower bounds, IPP). This is balanced. One phrase in the calibration argument says more than the method can show (m14).
- **Income at the top.** IPP's own reading (the top 1% is understated in shares) is missing (M1).
- **Bottom of the distribution.** The vintage revision is missing (M2).
- **Counter-critique for France.** Auten & Splinter is US-specific. No French critique of DINA-type allocation is cited apart from INSEE's own CND, which the page uses well. The France Stratégie capital-tax committee is now in `references.md`. That is acceptable for a working paper. Consider one sentence noting that the main critiques are US-based.

**AI disclosure.** See M3. The text of the disclosure is accurate and appropriately modest ("not peer reviews by outside experts"). Its placement and the contradictory labels weaken it. The page should disclose AI authorship, not only AI review.

**Authorship.** "Show Me Your Pie contributors (maintainer: github.com/Zboule)" is acceptable for code. For a working paper that makes claims about a live policy debate and names living individuals (No.1 fortunes in the rich-list CSVs), name an accountable maintainer and a contact (M3). The rich-list rows contain only figures already published by Challenges and Forbes about public figures. They are low-risk, but an accountable contact is still expected.

## 8. Reproducibility for a newcomer (task 5)

| Check | Result |
|---|---|
| Rebuild from raw | **V.** `python3 -I pipeline/build_data.py data/raw <out>` reproduces `site/data/france.json` exactly (apart from `meta.built`). `paper_numbers.py` reproduces `paper/numbers.json` byte for byte. |
| Tests | **V.** `python3 -m unittest discover -s pipeline/tests`: 23 tests OK. `node pipeline/tests/test_core.mjs` passes, but the README does not mention it or the need for Node. |
| `fetch.py` | **NC** (not run). |
| Relative links in Markdown | **V.** All relative links and anchors in README, paper, CONTRIBUTING, DATA_LICENSES, docs and notes resolve. One exception: `docs/reviews/README.md` links `round2-response.md`, which does not exist yet. |
| External links | **V** for 124 of 139 URLs checked (web.archive.org copies were checked separately in §5) (HTTP 200/206 to a browser UA). The rest: |
| | - 4 fr.fashionnetwork.com URLs were false negatives from comma truncation; their full URLs return 200 (§5). |
| | - ECB `data-api` and DWA note return 503 transiently, then 200. |
| | - The DREES ER 1055 PDF resets the connection (known; add a Wayback URL). |
| | - ccomptes.fr times out to scripts. |
| | - **github.com/Zboule/show-me-your-pie (3 links on the page, `CITATION.cff`) and zboule.github.io/show-me-your-pie (README) return 404.** The repository is not public yet. Check these after publishing. |
| "Three commands" | The paper §8 and page §11 say three; README "Run it" lists five (three pipeline steps, tests, server). Harmless, but align them. |
| Data inventory | `docs/02-data-france.md` §2.3 is stale (m10). |
| Fonts | The relative URL in `site/fonts/fonts.css` does not resolve (§3). |

## 9. Most important actions, in order

1. **C1.** Make the "removed before publication" statement true or accurate. Fix README line 99, the Notaires row and keys in `prices-housing.md`, and the IdO totals in the notes. Decide how the review archives are handled.
2. **M1.** Attribute the WID/IPP ratios to the project, and add IPP's own top-1% reading (pp. 3, 13).
3. **M2.** Add the bottom-50% and middle-40% rows of GGP 2016 Table 1 to the vintage comparison, and soften "robust across sources".
4. **M3.** Remove "Peer review" and "independent"; add an AI-authorship line to the page and the paper's front matter; complete `CITATION.cff`.
5. **M4, M5.** Correct the "(2021, appendix H)" citation; state a licence for the project's own data.
6. **m15.** Fix the font URL.
