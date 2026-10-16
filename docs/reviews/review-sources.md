# Source and fact-check review

Review date: 2026-10-16. Scope: `README.md`, `docs/*.md`, `docs/notes/*.md`, the
static and generated text of `site/index.html` (including its "Main references"),
and `data/manual/*.csv`. Nothing outside `docs/reviews/` was modified.

**Method.**
- Every verdict below rests on a passage read in the source itself: a publisher or
  Crossref record, an official PDF or web page, or the ECB/INSEE/Forbes API. Where a
  source could not be opened, the verdict says so.
- Bibliographic fields were checked against Crossref (`api.crossref.org/works/<doi>`).
- Local claims about WID were checked in `data/raw/WID_data_FR.csv`,
  `WID_metadata_FR.csv` and `site/data/france.json` (vintage ETag
  `34ddb835-65de34aea53dd`, fetched 2026-10-16).
- Downloaded PDFs are not committed. Re-check anything marked Partially or
  Not found before relying on it.

**Important: this review covers a moving target.**
- The issues below were found on the files as they stood at about 21:36 on
  2026-10-16.
- While the verification ran, several reviewed files were edited by someone else
  (timestamps 22:06–22:25): `01-concepts.md`, `02-data-france.md`, `03-method.md`,
  `references.md`, `insee.md`, `prices-housing.md`, `rich-lists.md`, `site/index.html`
  and `ipp_top_income.csv` (226 → 21 rows). `notaires_idf_apartment_prices_m2.csv`
  is no longer in `data/manual/`.
- A quick re-check at 22:26 gives the status of each issue below. It is a grep and
  spot-read, not a full re-review of the new text. Read the rest of the report as the
  evidence base, and the table below as what is still open.

| Issue | Status at 22:26 | What remains |
|---|---|---|
| C1 public-spending allocation | **Largely fixed.** Page "How this is computed" and the cross-check note now say health is close to lump-sum (Bozio et al. 2024; DINA guidelines 2025). | Re-read insee.md §4–5 for any leftover "neutral" or ranked-reasons wording. Cite Fisher-Post & Gethin p.12–13 (health by incidence) as the source for *this* vintage. |
| C2 Forbes calibration and headline tile | **Largely fixed.** The default start is now 1990, after calibration begins in 1988 (sourced to WID metadata in 03-method). A "two estimates" tile compares the 2016 paper with today's WID. The page warns for pre-1988 starts. | Add the bounded statement (Forbes ≈4.3 of 5.6 points in 2024). Describe the 2013→2014 Forbes jump as a coverage change. |
| C3 30% pre-committed source | **Fixed** ([INSEE-c1358], [INSEE-T2103]). | — |
| C4 "transfers / moved" vocabulary | **Largely fixed** on the page (lede and section "How each slice changed"). README no longer uses "moved". 03-method §3.2 documents the v0.1 wording. | Check the remaining code identifiers and labels (`transfer-chart`, table headers). |
| C5 IPP overclaim | **Mostly fixed.** The summary now says "indicative" and reports ratios by group. | Drop "IPP's earlier note found larger gaps": the earlier row was internally impossible (C5 evidence 2). Doc 04 §4.1 "only 8%" is still unqualified (per household, vs 24% at group level). |
| M1 `diinc` attribution | Fixed (Fisher-Post & Gethin cited). | — |
| M2 "one methodology" | Fixed (phrase gone). | — |
| M3 Appendix H | **Partly.** The formula now uses 1.8 adults per member. | 03-method §3.7 "Scenarios" still says "(2021, appendix H)"; rich-lists.md is correct. |
| M4 secondary political sources | **Open.** rich-lists still cites datan.fr. | Use AN scrutins n°881 and n°3300 and Sénat scrutin n°322. Requalify the "66%" and "0,2 % / 37 foyers" notes. |
| M5 counter-evidence prominence | Fixed (tiles note gives the ECB/BdF top-5% gap). | — |
| M6 missing sources | **Mostly fixed** (Auten, Landais, Comité fiscalité du capital, SILC now in references.md). | Blanchet, Chancel & Gethin (2022), the source of WID's European post-tax series. |
| M7 top-bin "discontinuity" | Appears removed from 03-method. | — |
| M8 doc contradictions | Fixed for the BdF note. | Check 01-concepts "below 0.001% only rich lists" (now cites IPP: OK) and the WP 2687 wording in rich-lists §3. |
| M9 licensing | **Open, but now listed.** The README has a pre-publication checklist. | No LICENSE file. Forbes ToS (API scraping) is not mentioned anywhere. Permissions from IdO, IPP and Notaires are still pending. |
| M10 IdO single source | Fixed (rich-lists §1 now says the table gives no method or revision note). | Show a ±3% band on the page if desired. |
| M11 undefined keys | Fixed. | — |
| Minor bibliography | Mostly fixed (BFP DOI, Verbist No. 130, Accardo A.). | Re-run §1 Minor against references.md. |
| Paris "region" wording | Fixed in docs and the limits list ("urban unit/area"). | Chart titles still say "outside the Paris region". |

**Verdict in one paragraph.** The data work is careful. Almost every number traced
to a source matches: about 60 numeric values checked across seven CSVs, the ECB API,
INSEE xlsx files and the Forbes API, with no undisclosed mismatch. The problems are
in **interpretation and framing**, where the page says more than the sources do:

- One explanatory claim shown on the page is contradicted by WID's own current
  methodology: health is not allocated in proportion to income.
- The headline wealth tile for the top 0.001% compares a start year that is probably
  uncalibrated with a Forbes-floored end year (Forbes ≈4.3 of 5.6 points in 2024).
  The calibration also reaches more years than the docs say.
- The "transfers" vocabulary implies euros changing hands, which the method itself
  denies.
- The IPP comparison presents a superseded figure the project derived itself as an
  equal estimate, and claims a certainty IPP's own 2025 paper does not support.
- One citation points to the wrong document: the 30% pre-committed figure is cited
  to a Martinique dossier.
- The repository is not yet publishable as-is on licensing grounds: Forbes ToS,
  Observatoire des inégalités, IPP and Notaires terms, and no LICENSE file.

---

## 1. Ranked issues

### Critical (fix before publishing)

**C1. The page's explanation of the INSEE-vs-WID post-tax gap is contradicted by
WID's current method.**
- *Where:* `site/index.html` `renderCrosscheck()` note ("WID shares public spending
  out in proportion to income, which understates what public services bring to the
  bottom half"); `docs/notes/insee.md` §3 table, §4 ("neutral for inequality"), §5
  reason 1; `docs/03-method.md` §3.8d ("because WID allocates health/education/
  collective spending in proportion to income (main WID scenario)").
- *Evidence:*
  - The docs rely on Bozio et al., WID WP 2018/10, p.14: "In our main scenario … impute
    in-kind transfers and collective expenditure proportionally to post-tax
    disposable income". That paper is superseded.
  - Its published version, Bozio, Garbinti, Goupille-Lebret, Guillot & Piketty,
    *AEJ: Applied* 16(2):31–65 (2024), doi:10.1257/app.20220023, p.16, reads: "Our
    baseline scenario (V1) assumes i) a lump-sum imputation of health care
    expenditure to individuals, and ii) a proportional imputation … for education
    spending and collective expenditures".
  - The DINA Guidelines, October 2025 version, p.70, read: "WID benchmark series
    assume a close to lump-sum imputation of healthcare expenditure and a
    proportional imputation of all other items."
  - The paper this vintage's `diinc` metadata actually cites (M1) points the same
    way. Fisher-Post & Gethin (2023), WID WP 2023/17, p.12–13: "In the main results,
    we thus present series with education spending allocated proportionally to
    posttax disposable income". And: "Data on the distributional incidence of
    healthcare come from Gethin (2023) … In line with other DINA studies, all other
    government expenditure is distributed proportionally". Health is therefore
    allocated by observed incidence, not in proportion to income, in the series
    actually used.
- *Consequences:*
  - The page states as fact, and with a normative verdict ("understates"), a
    mechanism the docs themselves flag as "not checked" (insee.md §7).
  - The ranking of reasons for the 38% (INSEE) vs 32% (WID) bottom-50% gap is
    unsupported.
  - The claim that in-kind transfers are "neutral" in the ERFS comparison
    (insee.md §4) is wrong for health.
- *Fix:*
  - Delete the sentence on the page.
  - Rewrite insee.md §3–5 and 03-method §3.8d on the basis of DINA Guidelines 2025
    p.70: health close to lump-sum; education and collective spending proportional.
  - The remaining differences are education and collective-spending allocation,
    no re-ranking in the INSEE CND, and unit. Present them as hypotheses, unranked.
  - Note that the local `diinc` metadata says "Education is distributed
    proportionally to posttax disposable income" and says nothing on health.
  - Add Bozio et al. (2024) to `references.md`.

**C2. The headline top-0.001% wealth tile mixes calibrated and uncalibrated years,
and the docs understate how far the Forbes calibration reaches.**
- *Where:*
  - page lede note ("Wealth after 2014 is extrapolated by WID and its top group is
    lifted to Forbes totals … part of the recent gain");
  - the tiles "Top 0.001% · net wealth 0.8% → 5.6%" and "Moved to the top 0.001%";
  - Limits list on the page;
  - 03-method §3.5;
  - 02-data §2.2.
- *Evidence:*
  1. **Reach of the correction.** WIL Technical Note 2025/01 (Bajard et al., updated
     version 18 Dec 2025), §3.3 p.4–5, adds the Forbes gap to the 127th
     g-percentile. Its Figure 2, "Wealth of billionaires in selected countries,
     1980–2024", plots "Base DINA" vs "Corrected DINA" for France over the whole
     period. Nothing in the note restricts the correction to extrapolated years.
     The docs and page tie it to the post-2014 extrapolation.
  2. **Same year, two vintages.** For 2014, an *observed* year (`data_quality` = 4),
     the GGP benchmark (WID WP 2016/5 rev. Jan 2017, Table 1, read) gives the top
     0.001% **0.9%**. The vintage used here gives **3.39%**.
     - The Forbes total alone is €216bn of €12,324bn (1.75%), using 03-method §3.7
       and dwa.md §5. So the top-up cannot explain the whole 2.5-point gap.
     - At least about 0.7 points come from other revisions: the JEEA 2021 final
       series, national-accounts updates, or the gpinter refit. None of these is
       documented in the project.
     - In **2024** the Forbes total is about €630bn of €14,657bn, i.e. **≈4.3 of
       the 5.58 points** of the top 0.001% share. Because WID's top bin is floored at
       Forbes, the recent level is set mostly by Forbes.
     - TN 2025/01 publishes the uncorrected French series only as a chart (Fig. 2).
       Whether the 1980 value (0.80%) carries any correction is not stated.
     - The tile therefore compares a start year that is probably uncalibrated with
       an end year that is calibrated. The size of the method effect is uncertain,
       but it is large in recent years.
  3. **The 2014 jump is a Forbes coverage change.** It comes from the Forbes API
     (fork G, recomputed). The 2013 list is complete (1,426 entries) but lacks
     fortunes long established by 2013 that appear in 2014:
     - Perrodo $10bn, A. Wertheimer $9bn, Castel $8bn, Servier $7.6bn, Drahi $6.3bn;
     - the 23 new French entries in 2014 total $69bn.
     - 03-method §3.5 describes this as "jumps in the Forbes series".
- *Fix:*
  - Say the Forbes top-up applies to every year for which WID has Forbes data, not
    only after 2014. Ask WIL or check `WID_metadata_FR.csv` for the first corrected
    year.
  - Show the GGP 2014 benchmark (0.9%) next to the current 3.4% on the page.
  - Either drop the top-0.001% tile from 1980 or caption it: "recent years are
    floored at the Forbes total (≈4.3 of 5.6 points in 2024)".
  - Replace "part of the recent gain" with that bounded statement.
  - Describe the 2013→2014 Forbes jump as a coverage change.

**C3. The "≈30% of disposable income" pre-committed figure cites the wrong
document.**
- *Where:* `docs/01-concepts.md` §1.2 step 6 → `[INSEE definitions]` in
  `references.md`.
- *Evidence:* The linked `ma_ind_09_def.pdf` is the definitions page of *Insee
  Dossier Martinique* n°9 (March 2018), on household budgets in the Antilles. It
  contains no 30% figure. The figure is in INSEE national accounts table 2.103,
  base 2020: 30.1% (2024) and 30.3% (2025), verified on
  <https://www.insee.fr/fr/statistiques/8988851>, `t_2103_fr.xlsx`.
- *Fix:*
  - Cite definition c1358 for the concept and table 2.103 for the number.
  - Add the two items 01-concepts omits from the list: TV services, and financial
    services incl. FISIM.

**C4. "Transfers", "moved" and "changed layer" describe flows that the method says
did not happen.**
- *Where:*
  - README line 5 and "What moved between layers";
  - page lede "how much has moved between those layers";
  - section title "What moved between layers";
  - the summary sentence "€X … changed layer";
  - tile "Moved to the top 0.001%";
  - table header "Euros moved";
  - 01-concepts §1.7 "Transfers between layers";
  - 03-method §3.5 `transfer_L`.
- *Evidence:* 03-method §3.5 says "This is a counterfactual on *shares*, not a claim
  that euros were taken from one group and handed to another". The page vocabulary
  says the opposite, and only the method doc carries the disclaimer.
- *Fix:*
  - Rename throughout to "gain/loss relative to the start-year split", or "euros
    above/below the start-year share".
  - Put the counterfactual sentence on the page, directly under the chart title.
  - Rename `transfer_L` in the docs.

**C5. The page overclaims what IPP shows about WID's top income, and gives a
superseded, self-derived figure the same standing as the published one.**
- *Where:* the page `renderIPP()` summary ("the size is uncertain, but the direction
  is not: WID's income measures likely understate the very top"); the column "IPP
  comprehensive income (2023 note, revised)"; 03-method §3.8d ("top 0.001% 2.0%
  (2025 paper) or 5.1% (revised 2023 note)"); 03-method §3.8d reading paragraph.
- *Evidence:*
  1. **The 5.1% is not published by IPP.** It is derived by the project:
     171.822m × 378 / 1,278bn. Note 92 publishes no shares.
  2. **The 2023 note had an impossible row.** In the original PDF the 75 richest had
     1,076.7m × 75 = €80.8bn of economic income. That is more than the whole top
     0.001% (171.8m × 378 = €64.9bn), of which they are a part. The 2025 PDF
     corrects only that row (`diff` of the two PDF texts). Neither the PDF nor the
     landing page says it was revised. So "IPP's own estimates moved between
     versions" misdescribes a correction.
  3. **The revised note and WP 2025 differ at every top fractile**, with no stated
     reason. Means above the threshold:
     - top 1%: 580k vs 455k;
     - top 0.1%: 3.385m vs 2.035m;
     - top 0.01%: 23.5m vs 10.9m;
     - top 0.001%: 171.8m vs 64.8m.

     The concepts differ: "economic income" is 80% of primary factor income,
     "comprehensive income" 68% of net primary factor income. WP 2025 (RFBerlin DP
     70/25) supersedes the note.
  4. **WP 2025 itself narrows the gap with WID-type estimates.** At p.13 it compares
     its top 1% (13.8%) with Garbinti et al. 2018 (10.8%). A DINA-style dividend
     imputation on its own data gives 13.0%, "which is 6.5% lower". So at the
     top 1% the DINA gap is small and partly definitional. Large ratios (×4 to ×6.5)
     appear only at the top 0.001% and above, for one year (2016), in tax households.
  5. **Units and denominators differ.** IPP's top 0.001% is 378 tax units against
     about 530 adults in WID. Totals differ too: €1,250bn comprehensive income vs
     WID national income.
- *Fix:*
  - Drop the 2023-note column from the page, or label it "superseded; derived by
    us".
  - Replace the summary with: "In 2016, IPP's comprehensive income puts the top
    0.001% of tax households at 2.0% of income, about 4× WID's pre-tax share for
    the top 0.001% of adults. Units and totals differ; for the top 1% the gap
    nearly disappears under a DINA-style imputation (IPP WP 2025, p.13)".
  - In doc 04 §4.1, "captures only 8%" is a per-household figure (WP25 p.13). At
    group level the dividend-imputed mean is 24% of comprehensive income (Table A2).
    Say which is meant.

### Major

**M1. The source of post-tax national income (`diinc`) is misattributed.**
- WID's own metadata for `adiinc`/`sdiinc` cites Fisher-Post & Gethin (2023), WID
  WP 2023/17. For Europe that paper takes its series from Blanchet, Chancel &
  Gethin (2022). The metadata adds: "2019-2022 series are estimated by applying the
  2019 ratio of pretax to posttax income by generalized percentile."
- The page ("How this is computed") and 02-data §2.2 credit GGP 2018/2021. GGP 2018
  is about pre-tax income.
- *Fix:* cite Fisher-Post & Gethin 2023 and Bozio et al. 2024 for `diinc`. State
  that 2019–2024 post-tax shares are a fixed-ratio extrapolation.

**M2. "One methodology from 1900 to 2024" overclaims** (02-data §2.2 point 3).
- WID's metadata describes several regimes:
  - `sptinc`: "Before 1980, series is constructed based on the trend observed in
    the fiscal income data";
  - wealth: GGP to 2014, then fixed 2014 asset mix, plus the Forbes top-up;
  - the 2026 update round: TN 2025/10 and TN 2026/04, cited in the metadata but
    never in the docs.
- *Fix:* replace with "a consistent framework stitched from several methods; see
  the breaks listed in §1.7".

**M3. GGP Appendix H is cited three ways, and the scenario only approximates it.**
- 03-method §3.7 says "Garbinti, Goupille-Lebret & Piketty (2021, appendix H)".
  rich-lists.md §5 says "GGP 2017, appendix H". The link [4] is WID WP 2016/6, the
  Data Appendix of December 2016, revised 27 Jan 2017. Appendix H is not in the JEEA
  2021 appendix (WID WP 2020/05 has Appendices A–B).
- GGP split each family into k members and treat 80% of them as married, giving
  about 1.8k adults per family. They compare with the top 0.001% only (p.52–53).
  `top_tail.py` uses n = 500 × k, and its "Spread" scenario compares with the top
  ~5,000 adults.
- *Fix:* cite "GGP (2016, rev. 2017), WID WP 2016/6, Appendix H". Say the scenario
  is "inspired by", not "the values GGP use in their own comparison".

**M4. Secondary sources are cited for political and parliamentary facts.**
- *Votes:* use the official scrutin pages, which confirm all three counts, in place
  of datan.fr, lcp.fr and publicsenat.fr:
  - AN scrutin n°881, 20 Feb 2025, 116–39:
    <https://www.assemblee-nationale.fr/dyn/17/scrutins/881>
  - Sénat scrutin n°322, 12 June 2025, 129 for, 188 against:
    <https://www.senat.fr/cra/s20250612/s20250612_5.html>
  - AN scrutin n°3300, 31 Oct 2025, amendment n°2359, 172–228:
    <https://www.assemblee-nationale.fr/dyn/17/scrutins/3300>
- *"66% business assets of the 380 richest"* (doc 04 bottom line; AN-930 p.8): this
  is second-hand. AN 930 attributes it to the *Comité … de la fiscalité du capital*
  on p.8 and to "les économistes de l'IPP" on p.31. The primary source has not been
  opened. Cite it as "reported by AN 930" or find the original.
- *"0,2 % pour les 37 foyers"* (`top_wealth_estimates.csv` note): AN 930 calls it a
  global tax rate on p.15 and an income-tax rate on p.18, both sourced to IPP. The
  figure is not in Note 92's text but may come from a chart. Say "not found in the
  note's text" rather than "contains no such figure".
- *Zucman's figures:* Zucman (G20 report, p.11) gives French billionaires' total
  rate as 27%, while IPP gives 26%. Note it where both are cited.

**M5. Counter-evidence is less prominent than the headline.**
- The lede and tiles use WID only. Three findings that point the other way appear
  only in the lower "Do other sources agree?" section and in notes:
  - DWA top 5% 5.8–7.6 points *below* WID in every year 2009–2024;
  - INSEE HVP top 1% about 11 points below WID;
  - ERFS showing the opposite income trend 1996–2018.
- WID's TN 2025/01 also carries its own caveats (p.8), and none is quoted:
  - Forbes counts "broader family units";
  - it neglects "diversified portfolios";
  - WID may "significantly underestimate" top 1% shares in some countries.
- *Fix:* add one tile or lede sentence: "Independent central-bank estimates put the
  top 5% share 6–7 points lower".

**M6. Credible sources that could qualify the conclusions are missing.**
- None of the following is cited (searched across all docs):
  - Bozio et al. 2024 (*AEJ: Applied*): the method behind WID's French post-tax series.
  - France Stratégie, *Comité d'évaluation des réformes de la fiscalité du capital*
    (reports 2019–2023), POTE-based evidence on top dividends after 2018:
    <https://www.vie-publique.fr/sites/default/files/rapport/pdf/276598.pdf>.
  - INSEE *Insee Références – Revenus et patrimoine des ménages* (annual).
  - Landais (2007) on French top incomes 1998–2006.
  - OECD Income Distribution Database; Eurostat EU-SILC.
  - Blanchet, Chancel & Gethin (2022) on Europe vs US.
  - Auten & Splinter (2024), *JPE* 132(7):2179–2227, doi:10.1086/728741: the main
    critique of DINA allocation choices (US). Cite with the Saez–Zucman reply.
  - DGFiP Analyses n°8 is used only in doc 04, not on the page.
- None of these is likely to reverse the bottom/middle findings. They matter for the
  top-tail and post-tax claims.

**M7. "Discontinuity in WID's top bin" is presented as a finding** (03-method §3.7).
- The data are right: 2024 thresholds of the last bins are 56.0, 63.4, 74.3, 94.5,
  then 798.7 €M, all of equal 0.001% width.
- But the jump is 7.1× in 2024 and 2.5× in 2010, and "fortunes between €100M and
  €800M are thin in WID" is the project's own inference.
- *Fix:* label it as our analysis, give both ratios, and link it to the Forbes
  top-up (C2), which creates exactly this pattern.

**M8. Contradictions between the docs.**
- rich-lists.md §3 and ref [13] say the Banque de France DWA note "could not be
  downloaded" and "reportedly" mentions "illiquidity". dwa.md [3] quotes it
  accurately.
  - Both URLs serve the same file (identical MD5).
  - The note speaks of ESA 2010 valuation differences, not illiquidity.
  - It needs a browser User-Agent; plain curl gets an Akamai 403.
- rich-lists.md §3 presents ECB WP 2687's "FR – Challenges (504)" as France's DWA
  list. It is an ECB-staff overview of rich lists at HFCS wave 3. The BdF note only
  says "classements … fournis par la presse nationale".
- 01-concepts §1.6: "Below 0.001% no statistical source exists; only rich lists".
  IPP measure the top 0.0002% (75 tax units) from tax data (Note 92, WP 2025).

**M9. Licensing blocks publication as-is** (details in §4).
- There is no LICENSE file.
- Forbes ToS prohibit "data mining, robot, spider … scraping" and storing content
  in a database. The CSV `source_url` documents an API scrape, which appears to
  conflict with these clauses. Get a legal opinion or switch to press-reported
  totals.
- The Observatoire des inégalités table is "© Tous droits réservés" and reuse needs
  written permission. 29 of 31 Challenges totals come only from it.
- IPP and Paris Notaires material is all rights reserved. `ipp_top_income.csv`
  (226 rows) and `notaires_idf_apartment_prices_m2.csv` (142 rows) may be substantial
  reproductions.
- WID publishes no database licence.
- The README "Sources" section omits ECB, INSEE ERFS/HVP/CND, DVF, Notaires, IPP,
  DREES, France Stratégie and DGFiP.

**M10. One undocumented secondary table carries the Challenges series.**
- IdO table 2646 matches the CSV for all 30 years (1996–2025). It gives no method,
  no franc-conversion note and no revision note.
- Primary press figures differ by 1–3%: 2014 390 vs 394; 2018 650 vs 670; 2019 700
  vs 711; 1996 81.7 vs 80 (536 MdF ÷ 6.55957).
- *Fix:* say so in rich-lists.md §1, and show the uncertainty band (±3%) on the page.

**M11. Undefined citation keys** in 01-concepts:
- `[Vermeulen2018; BTZ2019]` (§1.6);
- `[IPP2023]` (§1.6);
- "Blanchet et al. 2021" (§1.2 step 5), probably the 2021 DINA Guidelines.

None of these is in references.md.

### Minor

- **Bibliographic fields** (all checked against Crossref or the publisher):
  - BFP2022 is *RIW* 68(1):263–288, doi:10.1111/roiw.12510. The page prints
    "Review of Income and Wealth ." with an empty volume.
  - Fleurbaey & Gaulier 2009: pages 597–624, doi:10.1111/j.1467-9442.2009.01578.x.
  - Verbist et al. 2012 is OECD SEM WP **No. 130**.
  - RC2003: doi:10.1016/S0165-1765(02)00205-7.
  - JK2016: doi:10.1257/aer.20110236. The link goes to the 2010 NBER WP.
  - WH1968: AER pages missing; the link is the 1967 IRP draft, marked "Not to be
    quoted".
  - SSF2009: no publisher or URL.
  - [INSEE-EN2021]: the first author is **Aliocha** Accardo (doc says "J."). It is an
    *Insee Références* chapter, 22/07/2021.
  - [INSEE-DT2023]: title missing ("Approche élargie des inégalités et de la
    redistribution en France…", DT 2023-07, 08/03/2023).
  - IA88 title is truncated on the page.
  - [DINA-G]: authors and version history missing. The PDF is "VERSION: OCTOBER 2025".
  - JEEA 19(1) has a published Correction (p.707); mention it.
  - rich-lists ref [8]: the slug says "2021-12", but the PDF is TN **2021/16**,
    Blanchet & Martínez-Toledano, "Distributional Wealth Accounts in Europe:
    Methodology". Add title and authors.
  - IPP Note 92: the 2025 PDF still says "Juin 2023". Cite both versions with
    upload dates.
- **Fragile links:**
  - oecd-ilibrary returns 403; use DOIs.
  - PSE pages for GGP2018 and BFP2022 return 403/418 to bots; use DOIs.
  - The DREES ER 1055 URL resets the connection; add a Wayback URL.
  - banque-france.fr needs a User-Agent.
- **"Paris region +7%"** (01-concepts §1.2, references.md, page): INSEE compares the
  Paris *urban unit* (89% of Île-de-France's population) with the rest of the
  mainland *excluding Corsica*.
- **HVP quote uncited:** "sans calage sur les masses…" (insee.md §2) is genuine but
  comes from Insee Résultats <https://www.insee.fr/fr/statistiques/8736846>, which is
  not cited.
- **Unlabelled inferences:**
  - "Mortgage repayments are not included" (prices-housing §1.2) is not stated in
    c1358. It follows from national-accounts concepts; label it so.
  - insee.md §2 says CND collective spending is "allocated equally per UC". INSEE
    distributes national collective spending "forfaitairement" and local spending
    by civil-servant payroll, so it is near-flat, not exactly equal.
- **DWA:**
  - "Quarters after 2023-Q3 will be revised" extends a press-release sentence
    written about "data from 2021 onwards"; label it as inference.
  - "Pension entitlements (compulsory schemes …)": the ECB note excludes non-social-
    security pension claims. Pay-as-you-go pensions are outside the accounts anyway.
- **CASD/CSS wording (doc 04):**
  - SD-Box rule omits "sauf dérogation du producteur".
  - The 20 export credits are capped "à concurrence de 3 ans".
  - The INFRASEC-A grid *is* labelled "Tarif subventionné", so the "without saying"
    sentence is wrong.
  - 13 Oct 2026 is the deadline to *request* producer agreement, not to obtain it.
  - The 11-unit and 85% rules come from the 2025 enrolment deck, not the FAQ.
  - ISF-IFI ships as overlapping panels (2018–22, 2007–18, 2006–20, 2006–19).
  - The INFRASEC-DMA SD-Box is €53 HT.
  - The DVF "[not verified on page]" tag can be removed (verified).
- **Statistiques DVF** keeps only single-property sales ("ne garder que les mutations
  qui concernent un seul bien"); add to prices-housing caveats.
- **Rich-list CSV notes:**
  - 1999 threshold: Challenges 2000 says 140 MF, the note says 141.
  - The "UNVERIFIED" tags on 2022 threshold and 2025 threshold/top-1 can be removed
    (confirmed).
  - The 2026 €250m threshold has a single regional source.
  - Forbes lists heirs separately (Dassault, Saadé), so "individuals" partly means
    heirs of one fortune.
  - "Assigned by citizenship" rests on the API field name, not on Forbes's
    methodology text.
- **IPP Note 92 citation:** the landing page and the 2025 PDF give no revision
  notice. Cite both PDFs with upload dates (2023-09, 2025-05) and describe the
  change as a corrected row.
- **DGFiP A8:** the PDF has no usable text layer, so re-checks must read page
  images. Note this in the CSV.
- **Exchange rates:** WID converts Forbes at the latest exchange rate, the project at
  each year's rate. Say so where the two are compared.
- **Page wording:**
  - "Rich lists count the largest fortunes directly from company valuations":
    unlisted firms are *estimated* (Challenges, via GGP app. H; Forbes "discount[s]
    fortunes" lacking documentation). Drop "directly".
  - "Most income of the largest fortunes … never appears on a tax return": supported
    by IPP for the top 75 tax units in 2016 only. Say so.

---

## 2. Claim verification

Verdicts: **V** = Verified, **P** = Partially, **NF** = Not found or not openable,
**C** = Contradicted. Quotes are from the source as read.

### WID / DINA

| Claim | Where | Verdict | Source opened | Passage (page) |
|---|---|---|---|---|
| WID adds the Forbes difference to the top g-percentile | 03-method §3.7; rich-lists §2; page | V | WIL TN 2025/01 (wid.world, PDF, "This version: December 18, 2025") | "In cases where WID billionaire wealth is lower than Forbes, we add to the 127th g-percentile of each country the difference…" (p.4) |
| …taken proportionally from the rest | 03-method §3.5, §3.7 | V | same | "the same amount is subtracted proportionately to each group of the bottom 99.999% to keep aggregate wealth constant" (p.5) |
| Correction concerns years after 2014 (implied) | page lede/limits; 03-method §3.5 | C (not supported) | same | Fig. 2 "Wealth of billionaires in selected countries, 1980–2024", Base vs Corrected DINA incl. France (p.6) |
| Raw estimates "significantly underestimate billionaire wealth" for France | rich-lists §2, §5 | V | same | "our raw uncorrected estimates for countries like France or Britain significantly underestimate billionaire wealth" (p.8) |
| TN 2025/01 Table 1 world/Europe values | ggp_richlist_comparison.csv | V | same | World 3,514 / 13,270 vs Forbes 2,781 / 14,211; Europe 246 / 1,008 vs 562 / 2,955 (p.7) |
| WID metadata cites Bajard et al. 2025 | rich-lists §2 | V (+ also cites TN 2025/10, TN 2026/04, not mentioned in docs) | `data/raw/WID_metadata_FR.csv` | "Technote for the update: … Bajard, F., Bauluz, L., … Sodano, A. (2025)" |
| Wealth data_quality 4 to 2014, 0 from 2015; income extrapolated from 2019 | dwa §3; insee §4 | V | `WID_data_FR.csv` | shweal p90p100 2014 = 4, 2015 = 0; sptinc/sdiinc 2018 = 5, 2019 = 4 |
| TN 2021/16 "fixing the asset composition by percentile to 2014" | rich-lists §2 [8] | V (slug mislabelled) | wid.world …technical-note-2021-12 → PDF "Technical Note N° 2021/16" | "We extrapolate the wealth distribution series of Garbinti, Goupille-Lebret, and Piketty (2021) forward up to 2020 by fixing the asset composition by percentile to 2014" (p.2–3) |
| GGP: lists not formally used for benchmark | rich-lists §2 | V | GGP WID WP 2016/5 (rev. 27 Jan 2017) | "…although we do not formally use them for our benchmark series" (abstract) |
| GGP: "so much uncertainty about billionaire lists…" | rich-lists §2 | V | same | "…should be used with a lot of caution (in addition to other sources rather than on their own)" (p.25) |
| GGP 2014: top 1% 23.4, 0.1% 8.2, 0.01% 2.8, 0.001% 0.9 | top_wealth_estimates.csv; 03-method §3.8d | V | same, Table 1 | all values, average €180,329,356, threshold €87,227,640 |
| GGP app. H: families of 1/10/15 members, 80% married, ~20% non-resident, 100 families | 03-method §3.7; rich-lists §5 | V (but source is WP 2016/6, not "2021" or "2017") | GGP Data Appendix WID WP 2016/6 | "the median family size is 11 and the mean 14. We alternatively consider that each family include 1, 10 or 15 members"; "100 families … are not French residents … around 20% … rough estimate … lower bound" (p.52) |
| Corrected Challenges "consistent" with benchmark | rich-lists §5 | V | same | "our benchmark estimates give consistent levels of wealth share when compared to our preferred corrected Challenges series" (p.53) |
| WID allocates in-kind and collective spending in proportion to income (main scenario) | insee §3, §5; 03-method §3.8d; page | **C** | DINA Guidelines Oct 2025; Bozio et al. AEJ 2024; Fisher-Post & Gethin WID WP 2023/17 p.12–13 ("Data on the distributional incidence of healthcare come from Gethin (2023)") | "WID benchmark series assume a close to lump-sum imputation of healthcare expenditure and a proportional imputation of all other items" (p.70); "lump-sum imputation of health care expenditure" (AEJ WP version p.16) |
| WP 2018/10 main scenario proportional | insee §3 | V (superseded) | WID WP 2018/10 | "impute in-kind transfers and collective expenditure proportionally to post-tax disposable income" (p.14) |
| `diinc` rests on GGP2018 / DINA-G | 02-data §2.2; page | P (misattributed) | `WID_metadata_FR.csv`; Fisher-Post & Gethin WID WP 2023/17 | metadata source = Fisher-Post & Gethin (2023); "2019-2022 series are estimated by applying the 2019 ratio of pretax to posttax income by generalized percentile" |
| One methodology 1900–2024 | 02-data §2.2 | P (overclaim) | `WID_metadata_FR.csv` | "Before 1980, series is constructed based on the trend observed in the fiscal income data" |
| diinc 1980–2024; cainc stops in 1979 | 02-data; 03-method §3.2 | V | `WID_data_FR.csv` | adiinc 45 years 1980–2024; acainc only 1970, 1975, 1979 (metadata itself says "1980-2021", an internal WID inconsistency) |
| Adults 2024 ≈ 52.96m; layer sizes | 03-method §3.4 | V | `WID_data_FR.csv` | npopuli992 2024 = 52,956,956 |
| Top 0.001% share 2.4→3.4 (2013–14), 3.4→4.8 (2020–21), 5.6 (2024) | 03-method §3.5 | V | `france.json` | 2.39, 3.39, 3.44, 4.78, 5.58 |
| Top-bin threshold 7× above the bin below | 03-method §3.7 | P (2024: 8.5× vs the threshold just below, 7.1× vs the average; 2010: 2.5×; interpretation is ours) | `WID_data_FR.csv` | thresholds 56.0, 63.4, 74.3, 94.5, 798.7 €M (2024) |
| P99 pre-tax threshold €233k; top 1% share 11.8% (2024) | 01-concepts §1.5 | V | `france.json` | threshold 233,015; share 0.1182 |

### ECB / Banque de France DWA

| Claim | Where | Verdict | Source opened | Passage (page) |
|---|---|---|---|---|
| First published 8 Jan 2024 as experimental statistics | dwa §1 | V | ECB press release ecb.pr240108 | "The European Central Bank (ECB) has today published experimental statistics on Distributional Wealth Accounts (DWA)" |
| "comply with many, but not all, of the quality requirements…" | dwa §1 | V | same | exact |
| Published five months after quarter end | dwa §1 | V | same | "published five months after the end of each period" |
| Quarters after 2023-Q3 will be revised | dwa §2, §6 | P (inference) | same | "data from 2021 onwards will be revised when the next HFCS wave becomes available" |
| AT, DE, FR, IT, NL compile their own series | dwa §1 | V | ECB DWA methodological note | "Other countries (Austria, Germany, France, Italy and the Netherlands) compile the data themselves" (p.2) |
| 93% of assets, 88% of liabilities covered | dwa §1 | V | same | Table 1 "Sub-total 93% … 88%" (p.9, euro area mid-2023) |
| Missing-rich step second-largest after calibration; w0 = €1m; Vermeulen | dwa §2.3; rich-lists §3 | V | same | "the second most significant of the reconciliation steps … after the final proportional allocation" (p.16); "w0 is set at €1 million for most countries" (fn 22) |
| WP 2687 authors, title, July 2022 | dwa [4] | V | ECB WP 2687 PDF | cover |
| WP 2687 Table 1 "FR – Challenges (504)" at wave 3 | dwa §2.3; rich-lists §3 | V (quote) / P (as BdF's official list) | same | "The number in parentheses is the number of observations provided by the rich list at the time of the third HFCS wave" (p.16) |
| BdF note: ~90% coverage; "ne permettent pas … top 10 % ou le top 5 %" | dwa §1 | V | BdF `F26z_note_methodologique_DWA.pdf` (browser UA needed) | p.2; fn 12 p.6 |
| 4 households per family; FIBEN/LIFI/INPI; residence; ESA 2010 valuation | dwa §2.3 | V | same | fn 3 p.4 |
| BdF note "could not be downloaded", mentions "illiquidity" | rich-lists §3 [13] | **C** | 2024-02 URL (same MD5 as 2026-09 file) | adjustment is for "différentiels de méthode de valorisation … (SEC 2010)"; no "illiquidity" |
| Wave anchors and coverage 75.9 / 65.4 / 76.3 / 67.6 / 73.4% | dwa §2 | V | same | Chart G1 (p.5) |
| Published shares: top 10% 2009 = 51.0, 2024 = 54.4; bottom 50% 2014 = 5.6; top 5% 2024 = 40.7; total 2024 = €13,841bn; 2009-Q4 to 2026-Q1 | dwa §4–5 | V | ECB SDMX API (URL in dwa.md) | 51.03; 54.45; 5.6; 40.66; 13,841,054 (UNIT_MULT 6) |

### INSEE, DREES, France Stratégie, prices and housing

| Claim | Where | Verdict | Source opened | Passage (page) |
|---|---|---|---|---|
| INSEE: 57% of people receive more than they pay (2019) | references.md; insee | V | Insee Analyses 88, <https://insee.fr/fr/statistiques/7669723> | "en 2019, 57 % des personnes reçoivent plus qu'ils ne versent" |
| CND total €2,026bn; €610bn non-monetary; collective ≈ €4,200 per UC | insee §2, §5 | V | same, Fig. 1 | "Transferts non monétaires 610,3"; "Dépenses collectives 195,2 / 4 200" |
| Collective spending "allocated equally per UC" | insee §2 | P | same, méthode | "distribuées forfaitairement"; localisable part "à partir de la masse salariale des fonctionnaires" |
| Paris region prices 7% above rest of mainland France, 2022 | 01-concepts; references; page | P (geography) | Insee Première 1959, <https://www.insee.fr/fr/statistiques/7649921> | "La région parisienne est l'unité urbaine de Paris"; "province … hors unité urbaine de Paris et hors Corse" |
| IP1959 Fisher 7.2 / excl. rents 5.0 / rents 39.6 / baskets 8.2 & 6.2 | prices-housing §1.3 | V | same + xlsx | Fig. 1 and data file |
| Pre-committed ≈30% of disposable income [INSEE definitions] | 01-concepts §1.2 | **C** (wrong source) / V (number, other source) | `ma_ind_09_def.pdf` (Insee Dossier Martinique n°9); table 2.103 | no "30 %" in the PDF; t_2103 row "_DEP_REVENU" 2024 = 30.1, 2025 = 30.3 |
| Definition c1358 items | prices-housing §1.2 | V | <https://www.insee.fr/fr/metadonnees/definition/c1358> | "…télécommunications ; frais de cantine ; services de télévision… assurances (hors assurance-vie) ; services financiers (y compris… SIFIM)" |
| Mortgage repayments not included (NA definition) | prices-housing §1.2 | P (inference) | c1358 | not stated |
| Table 2.103 series 1960–2025 | prices-housing §1.2 | V | t_2103_fr.xlsx (page 8988851, 29/05/2026) | all 12 points match |
| DREES ER 1055 totals 61 / 39 / 31 / 23 / 30; includes mortgage repayments | prices-housing §1.2 | V (via Wayback; DREES site resets) | er1055-2.pdf | "pauvres (61 %)… l'ensemble des ménages (30 %)"; column "Remboursements de prêts immobiliers" |
| France Stratégie NA 102: 27%→32%; poor 60% of disposable income | prices-housing §1.2 | V | NA 102 PDF | "passant de 27 % à 32 %" (p.1); "41 % de leurs dépenses mais 60 % de leur revenu disponible" (p.6) |
| IP1815 Fig. 7 quintiles 31.5 … 19.0 | prices-housing §1.2 | V | <https://www.insee.fr/fr/statistiques/4764600> | Fig. 7 "(hors loyers imputés)" |
| HVP "sans calage sur les masses des comptes de patrimoine" | insee §2 | V (uncited page) | <https://www.insee.fr/fr/statistiques/8736846> | exact |
| HVP top 10% 48%, Gini 0.652 (2024) | insee §6 | V | IF371 page + xlsx | "Les 10 % les mieux dotés détiennent à eux seuls 48 %"; "0,652 en 2024" |
| ERFS Gini 2024 = 0.302; top 10% = 24.9 | insee §4 | V | page 2491918 xlsx | Gini 0.302; S90 75.1 |
| DVF excludes Alsace, Moselle, Mayotte; 5-year window | 04 §4.2; prices-housing §2 | V | data.gouv DVF dataset | "au cours des cinq dernières années … à l'exception de l'Alsace, de la Moselle et de Mayotte" |
| Notaires level moves exactly with INSEE 010567012 | prices-housing §1.3 | V (our computation) | PDF + BDM | ratio 79.32–79.79 over 138 quarters |

### IPP, Zucman, Parliament, DGFiP

| Claim | Where | Verdict | Source opened | Passage (page) |
|---|---|---|---|---|
| IPP Note 92: authors, June 2023 | rich-lists §4; 04 [N92] | V | ipp.eu revised PDF | cover "Juin 2023 … Laurent Bach, Antoine Bozio, Arthur Guillouzouic, Clément Malgouyres" |
| IPP: 75 billionaire households; 46% vs 26% total tax rate | rich-lists §4 | V | same | "passant de 46 % pour les 0,1 % les plus riches, à 26 % pour les 0,0002 % les plus riches (les « milliardaires »)" (p.1); 75 foyers at P99,9998 (Tableau 1) |
| Personal taxes ≈2% of economic income for top 378 | rich-lists §4 | V | same | "ne représenter plus que 2 % du revenu économique parmi les 378 ménages les plus aisés" (p.4) |
| Note 92 does not use Challenges | rich-lists §4 | V | both versions | no occurrence of "Challenges" |
| Note 92 revised vs original: only the top-0.0002% row changed | ipp csv note | V | both PDFs (`diff`) | the 634,504,000 vs 1,076,710,000 row; original row was internally impossible (see C5) |
| WP 2025: RFBerlin DP 70/25, Sept 2025 | 04 [WP25] | V | rfberlin PDF | "DISCUSSION PAPER SERIES 70/25 … SEPTEMBER 2025" |
| WP 2025: rates 45% → 25%; personal taxes 2% | ipp csv | V | same | "total tax rates fall from 45% at the 0.1% threshold to 25% for billionaires" (abstract) |
| Top 75 ~85% probability of being in the Challenges list | rich-lists §4 | V | same | "probability of being included in the top 500 list close to 85%" (p.14) |
| DINA rule captures only 8% of top-75 income | 04 §4.1 | P (per household; 24% at group level) | same | "which is only 8% of their real comprehensive income" (p.13); Table A2 51.8m vs 217.3m |
| 3-year stay rate top 0.001%: 15% vs 64% | 04 §4.1 | V | same, Table A1 | "below 15%, while it is as high as 63.5%" (p.14) |
| POTE panel 2003–2023; ~350,000 ISF filers above €1.3m | 04 §4.2 | V | same §2.1.1 | p.7 |
| Top 0.001% 2.0% (2025) or 5.1% (2023 note) of income | 03-method §3.8d; page | P (5.1% is derived by the project and superseded) | both PDFs | WP25 Table 1 "1.97"; Note 92 publishes no shares |
| WID-type top 1% close to IPP under DINA imputation | not in docs | (counter-evidence) | WP25 | "with the DINA dividend-based imputation of retained earnings is 13.0%, which is 6.5% lower" (p.13) |
| CAE Focus 118 authors, July 2025; 0.2% / 0.6% emigration; 43%; €30,000 | 04 §4.7; ipp csv | V | cae-eco.fr PDF | "0,6 % … top 1 % des revenus totaux s'est expatrié fiscalement en 2017, contre 0,2 % pour le top 1 % des revenus du capital" |
| Zucman G20, 25 June 2024: $200–250bn, ~3,000 taxpayers, 0.3% of wealth | rich-lists §4 | V | taxobservatory PDF | "would raise $200-$250 billion per year globally from about 3,000 taxpayers … equivalent to 0.3% of their wealth" (p.1) |
| French billionaires 27% total; 1.7% income tax; ~25% corporate | ipp csv | V | same | p.11, p.15 |
| AN adopted taxe Zucman 20 Feb 2025, 116–39 | rich-lists §4 | V | AN scrutin n°881 | "Pour l'adoption : 116 Contre : 39 … L'Assemblée nationale a adopté" |
| Sénat rejected 12 June 2025, 188–129 | rich-lists §4 | V | senat.fr compte rendu, scrutin n°322 | "Pour l'adoption 129 Contre 188" |
| Rejected in PLF 2026, 31 Oct 2025, 172–228 | rich-lists §4 | V | AN scrutin n°3300 | "amendement n° 2359 de M. Vallaud … Pour l'adoption : 172 Contre : 228" |
| AN 930 p.8: "au moins 66 % du patrimoine des 380 foyers" | 04 bottom line | V (second-hand in source) | AN 930 PDF | p.8, citing the Comité; p.31 attributes it to IPP |
| AN 930 p.14: Zucman's 1,800 households > €100m | rich-lists §4 | V | same | "estime à 1 800 le nombre de foyers fiscaux possédant un patrimoine supérieur à 100 millions" |
| AN 930 calls €245m both threshold and average | rich-lists §4 | V | same | p.14 "seuil d'entrée … 245 millions"; p.36 "en moyenne un patrimoine de 245 millions" |
| AN 930: €1,500bn = 1,200 + 300; yield 15.3–25.5 Md€; 1,228bn in 2024 | rich-lists §4 | V | same | p.37; p.7 |
| PPL 768: "quelques 4 000 contribuables" | top_wealth csv | V (on PDF p.4, not p.5) | pion0768.pdf | "seuls les quelques 4 000 contribuables dont le patrimoine est supérieur à 100 millions d'euros, soit 0,01 % des contribuables" |
| DGFiP A8: Jan 2025, authors; "rupture de série" | 04 §4.6 | V | impots.gouv PDF (no text layer, read as images) | "le patrimoine mobilier n'est plus déclaré, ce qui crée une rupture de série" (p.2) |
| Top 0.1% income 2022: 40,700 households, entry €463k | 04 §4.3 | V (in DGFiP A8; INSEE FPS co-citation not checked) | same | "environ 40 700 foyers en 2022. Le seuil d'entrée … est un revenu de 463 K€" (p.2) |
| Zucman (Le Grand Continent): Challenges 500 ≈ 40% of GDP vs 6% in 1996 | top_wealth csv | V | legrandcontinent.eu | "avoisine aujourd'hui l'équivalent de 40 % du PIB … contre 6 % en 1996" |

### CASD / CSS (doc 04)

| Claim | Verdict | Source opened | Passage |
|---|---|---|---|
| "seule une personne morale peut financer un abonnement" | V | casd.eu FAQ | exact |
| SD-Box only at a legal entity's address | P (omits "sauf dérogation du producteur") | same | "sauf dérogation du producteur de données, une SD-Box ne peut être hébergée qu'à l'adresse d'une personne morale" |
| 20 export credits, 30 min | P (cap "à concurrence de 3 ans" omitted) | same | "20 exports pour toute la durée de votre projet à concurrence de 3 ans" |
| 11-individual / 11-unit + 85% rules | V (but source is the 2025 enrolment deck, not the FAQ) | CASD_Presentation_Enrolement_20250402.pdf | "seuil de 11 unités, une unité ne peut représenter plus de 85% du total d'une case" |
| Main mission non-profit research | V | same, slide 2 | exact |
| INFRASEC-A prices (253, 37, users, configs, 318, from 01/01/2023, min 1 year) | V | casd.eu/tarifs-2 | "Tarifs applicables à compter du 01/01/2023"; "253,00 € / mois" |
| Page doesn't say whether subsidised = this grid | C (minor) | same | grid header "Tarif subventionné" |
| Budget €7.4–9.1k/yr | V (arithmetic) | same + POTE deck | (253+37+327)×12 = 7,404; (253+37+466)×12 = 9,072 |
| CSS calendar dates | V | comite-du-secret.fr calendrier | "Séance du 16 mars 2027 … 26 janvier 2027 … 15 février 2027" |
| "producer agreement by 13 Oct 2026" | P (deadline to *request*) | same | "Date limite de demande d'accord préalable des producteurs : 13 octobre 2026" |
| Four sessions + ~8 e-consultations; 6-year authorisation; DGFiP "Autorisation de communication…" | V | CSS fonctionnement, FAQ | "tient quatre séances par an"; "accordée pour une durée de 6 ans" |
| LPF L135 D legal basis | P (Légifrance 403; cited by CSS FAQ) | CSS FAQ | "L135D du livre de procédures fiscales" |
| Enrolment ~2h, two fingers, 6 vs 4 years | V (CASD contradicts itself) | enrolment and habilitation pages | "valide pendant six ans" vs "durée de validité de 4 ans" |
| POTE 2003–2024, all taxpayers, 40m units, 4,000 variables | V | CASD POTE page + DGFiP deck | "40 millions de foyers fiscaux, 4 000 variables" |
| Other CASD vintages (ISF-IFI, BIC-IS, LIFI, FARE, FIDELI, Foncier, ERFS, DMTG) | V (ISF-IFI as overlapping panels) | CASD source pages | — |
| CNRS "en moyenne trois semaines"; INSEE "peut prendre des mois" | V | enssib PDF; Courrier des stat. n°3 | exact |

### Rich lists (methodology)

| Claim | Where | Verdict | Source opened | Passage |
|---|---|---|---|---|
| Forbes 2022 snapshot 11 March | rich-lists §1 | V | Wayback 20220627 forbes.com/billionaires | "stock prices and exchange rates from March 11, 2022" |
| Spouse and children included if founder | rich-lists §1 | V | same | exact |
| Private companies, real estate, art; discounts undocumented fortunes | rich-lists §1 | V | same | "When documentation isn't supplied or available, we discount fortunes" |
| Country by citizenship | rich-lists §1 | P (API field name only) | Forbes API | `countryOfCitizenship` |
| 7–10 French billionaires a year abroad (2014–2026) | rich-lists §1 | V (rough) | Forbes API `city` | 2014: 10, 2021: 9, 2026: 8 |
| Challenges professional wealth only | rich-lists §1 | V | fashionunited.fr 2026 | "ne prend pas en compte les biens personnels, comme l'immobilier" |
| 2026 "153 familles milliardaires" | rich-lists §1 | V | same | exact |
| 2019 list "6 % du patrimoine actuel des Français" | rich-lists §5 | V | fr.fashionnetwork.com …1116501 | exact |

---

## 3. CSV spot-check

Random sample drawn with `random.seed(20261016); random.sample(...)` in
`python3 -I`:
- Challenges: 2000, 2012, 2013, 2019.
- Forbes: 2010, 2014, 2018, 2022.

All other rows are **targeted**, not random: the "UNVERIFIED" and "CONFLICT" rows,
plus rows from `ipp_top_income.csv`, `top_wealth_estimates.csv`,
`precommitted_spending_surveys.csv`, `insee_spatial_price_gap.csv` and
`notaires_idf_apartment_prices_m2.csv`.

A second seeded draw (same seed, two rows per file) was made from the files as they
stood at 22:26, after the concurrent edits. Its results follow the main table.

| File | Row | Field | CSV | Source | Source opened | Match |
|---|---|---|---|---|---|---|
| challenges_500 | 1996–2025 (all 30) | total_eur_bn | — | IdO table 2646 | inegalites.fr table 2646 | Yes, all 30 |
| challenges_500 | 2000 | total / threshold / No.1 | 191 / – / Arnault | 1,259 MdF (= 191.9 €bn), 218 MF, Arnault 134 MdF | Challenges archive (Wayback 2001) | Yes |
| challenges_500 | 1999 (note) | threshold | 141 MF | 140 MF | same | No (note typo) |
| challenges_500 | 1996 (note) | total | 80 (IdO) | 536 MdF = 81.7 €bn | Challenges archive | ~2% gap (IdO rounding/conversion) |
| challenges_500 | 1998 | No.1 | Bettencourt | rank 1 "Famille Bettencourt dont Liliane" | Wayback 1999 Fort1.html | Yes |
| challenges_500 | 2005 | No.1 | Arnault | AFP 2006 "conserve … la première place" | webmanagercenter 2006 | Implied only (as noted) |
| challenges_500 | 2012 | No.1 amount | 21 | "21 milliards d'euros"; "-3%" | franceinfo | Yes |
| challenges_500 | 2013 | total / No.1 / threshold | 329 / 24.3 / 65 | 329 / 24.3 / "de 65 à 235 millions" | politis.fr; journaldeleconomie | Yes |
| challenges_500 | 2014 | total / threshold | 394 / 80 | AFP 390; "80 en 2014" | africanmanager; fashionunited 2024 | Conflict disclosed |
| challenges_500 | 2018 | total / threshold | 670 / 140 | AFP 650; 140 M€ | lalibre.be; gestiondefortune | Conflict disclosed |
| challenges_500 | 2019 | total / No.1 | 711 / 90 | "700 milliards", 90 | fashionnetwork | Yes (press rounded) |
| challenges_500 | 2022 | threshold / No.1 | 200 / 149 | 200 M€ / 149 | luxus-plus.com | Yes (UNVERIFIED tag removable) |
| challenges_500 | 2025 | threshold / No.1 | 245 / 163.4 | 245 / 163.4 | dimanche7; fashionunited.in | Yes (tag removable) |
| challenges_500 | 2026 | total / families / threshold | 1076 / 153 / 250 | 1,076 / 153 / 250 (one regional source) | fashionunited.fr; lyoncapitale | Yes |
| forbes_france | 2010, 2014, 2018, 2022, 2024, 2026 | n / total_usd_bn | 12/89.7; 43/235.2; 40/320.4; 43/550.0; 53/673.5; 53/627.8 | recomputed from Forbes API | forbesapi JSON (browser UA) | Yes, all |
| forbes_france | 2017 | n / total | 38 / 245.1 | press 39 / $245bn | thelocal.fr | Count gap disclosed |
| forbes_france | 2021 | n / total | 42 / 512.2 | "42 milliardaires … un peu plus de 510 milliards de dollars" | fashionunited.fr | Yes |
| top_wealth_estimates | GGP 2014 four shares + avg + threshold | — | 23.4 / 8.2 / 2.8 / 0.9; 180,329,356; 87,227,640 | GGP WP 2016/5 Table 1 | Yes |
| ggp_richlist_comparison | TN 2025/01 Table 1 world and Europe | — | as CSV | TN 2025/01 p.7 | Yes |
| precommitted_spending_surveys | DREES 2011 totals (5 groups) | — | 61/39/31/23/30 | ER 1055 Table 1 | Yes |
| precommitted_spending_surveys | DREES poor rents 37; affluent mortgage 8; all mortgage 7; middle health ins. 3 | — | as CSV | same | Yes |
| precommitted_spending_surveys | DREES affluent school_canteen | blank | "<1" | same | Acceptable; note it |
| precommitted_spending_surveys | FS NA102 chart (poor, affluent, all, 4 years) | — | as CSV | NA 102 p.1 | Yes |
| precommitted_spending_surveys | FS NA102 Tableau 3 D1/D5/D9; Tableau 2 medians | — | as CSV | NA 102 p.12 | Yes |
| insee_spatial_price_gap | 2015 Total (8.8 / 9.2), hors loyers 6.2, rents 48.9, Santé 6.5 | — | as CSV | IP1590 Fig. 1 | Yes |
| notaires_idf_apartment_prices_m2 | 1996 Q1, 2020 Q4, 1991 Q1 (Paris, IdF, PC, 92, 95) | — | as CSV | Paris Notaires PDF | Yes |

**Second seeded draw** (`random.seed(20261016)`, two rows per file, files as of
22:26):

| File | Row index | Row | CSV | Source | Passage read | Match |
|---|---|---|---|---|---|---|
| ipp_top_income (21 rows) | 4 | WP25 top 1% taxable_income_mean_above | 265,000 | WP25 Table 1 row "P99 378,333 135,000 265,000" | as quoted | Yes |
| ipp_top_income | 17 | WP25 top 0.0002% total effective tax rate (comprehensive) | 25 | WP25 abstract | "45% at the 0.1% threshold to 25% for billionaires" | Yes |
| top_wealth_estimates | 13 | AN 930, foyers > €100m, total wealth | 1,500 €bn | AN 930 yield table | "1 500 milliards d'euros … 25 milliards d'euros 0,9 %" | Yes |
| top_wealth_estimates | 16 | AN 930, 380 richest foyers, business-asset share | 66% | AN 930 p.8 | "au moins 66 % du patrimoine des 380 foyers les plus riches" | Yes (second-hand, see M4) |
| precommitted_spending_surveys | 37 | DREES 2011, affluent, other insurance & financial services | 2 | ER 1055 Tableau 1, row "Aisés" | "8 2 1 <1 2 2 8 23" | Yes |
| precommitted_spending_surveys | 70 | FS NA102 Tableau 3, D5 arbitrable income threshold | 1,131 | NA 102 p.12 | "Revenu arbitrable par UC 377 605 794 960 1 131 …" | Yes |

**IPP and DGFiP rows** (sources: IPP Note 92 revised and original PDFs; RFBerlin
DP 70/25; DGFiP Analyses n°8; AN 930):

| File | Row | CSV | Source | Match |
|---|---|---|---|---|
| ipp_top_income | N92 revised, top 0.001% economic mean above | 171,822,000 | 171 822 000 (Tableau 1 p.3) | Yes |
| ipp_top_income | N92 revised / original, top 0.0002% economic mean above | 634,504,000 / 1,076,710,000 | same values | Yes (original row internally impossible, see C5) |
| ipp_top_income | N92 top 1% fiscal threshold; top 0.1% economic mean; aggregate | 135,000; 3,385,000; 1,278bn | same | Yes |
| ipp_top_income | WP25 Table 1, top 0.001% comprehensive mean / share / ratio | 64,768,000 / 1.97 / 4.2 | same | Yes |
| ipp_top_income | WP25 Table 1, top 0.0002% comprehensive mean / share; taxable threshold | 217,289,000 / 1.31; 14,953,000 | same (N92 gives 14,998,000) | Yes |
| ipp_top_income | WP25 top 10% taxable share; Table A2 top 1% dividend-imputed share | 34.96; 12.98 | same | Yes |
| ipp_top_income | CAE F118 rows (0.2%, 0.6%, 43%, €30,000, 0.02–0.23%) | as CSV | CAE PDF | Yes |
| top_wealth_estimates | DGFiP 2016 THP: 38,000 foyers, 387bn, 3.5%, avg 10.2m | as CSV | A8 p.1–3 (p.3 says 9.9m: source inconsistency, disclosed) | Yes |
| top_wealth_estimates | DGFiP 2022 IFI THP: 187bn, 1.8%, avg 4.6m, threshold 2,667k | as CSV | A8 p.3, Tableau 1 | Yes |
| top_wealth_estimates | AN 930: 1,500bn; 1,800 foyers; 0.3% | as CSV | p.14, p.36–37 | Yes |
| top_wealth_estimates | PPL 768 "4 000" | note says p.5 | on PDF p.4 | Page reference off by one |

**Overall:** about 60 values were checked across seven CSVs. There was no
undisclosed value mismatch. The discrepancies found are in notes (1999 threshold,
PPL page), in source labelling (Appendix H, Note 92 revision) and in single-source
dependence (IdO).

---

## 4. Licensing and attribution

| Producer / dataset | Licence found | Terms URL | Attribution required | Restrictions for this repo | Confidence |
|---|---|---|---|---|---|
| WID.world bulk data | **None published** for the database. /terms-of-use/ is 404; the bulk-zip README has no licence. WID *reports* are CC BY-NC-SA 4.0. | <https://wid.world/data/> | None stated; cite WID + vintage + GGP | Do not redistribute raw CSVs (already gitignored). Publishing derived `france.json` with citation is customary; ask WIL to be safe. | Medium–low |
| INSEE (BDM, xlsx, publications) | Licence Ouverte / Open Licence 2.0 "sauf mention contraire" | <https://www.insee.fr/fr/information/2008466> | « Source : Insee » + date of last update | Do not alter meaning | High |
| ECB Data Portal (DWA) | ESCB reuse policy, free reuse | <https://www.ecb.europa.eu/stats/ecb_statistics/governance_and_quality_framework/html/usage_policy.en.html> | "Source: ECB statistics." | Statistics "not modified": label derived series (D6–D9 sums, p90–95, household counts) as own calculations | High |
| Banque de France Webstat | Per-dataset; BdF property | <https://webstat.banque-france.fr/terms/terms-and-conditions/?flg=fr-fr> | cite the dataset | Project uses the ECB copy, so ECB terms apply | Medium |
| DVF / Statistiques DVF | Licence Ouverte 2.0 + DVF conditions | <https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/> | "DGFiP, DVF" / "Etalab, Statistiques DVF" + date | No re-identification; no search-engine indexing of personal data. Département aggregates only (current practice is fine). | High |
| Paris Notaires Services | None found; assume all rights reserved | PDF linked in prices-housing.md | cite Paris Notaires Services / Notaires-INSEE | 142-row transcription may constitute a substantial extraction: ask permission or keep annual values only | Low |
| Forbes World's Billionaires | Forbes Terms of Service | <https://www.forbes.com/terms-and-conditions/> | — | "solely for personal, non-commercial" use; no "data mining, robot, spider … scraping"; no storing in a database. **The API method appears to conflict with these ToS clauses** (a legal check is advisable). Yearly count and total are facts (lower risk); do not commit per-person data; consider press-reported totals. | High |
| Challenges via Observatoire des inégalités | "© Tous droits réservés" | <https://www.inegalites.fr/Mentions-legales> | « article repris du site de l'Observatoire des inégalités » + link | Reuse of "textes et données" needs written permission: ask, or cite each figure to Challenges/press | Medium–high |
| IPP (Note 92) | All rights reserved | <https://www.ipp.eu/mentions-legales/> | — | Reproduction "sans l'autorisation écrite préalable de l'IPP, est interdite": 226-row CSV needs permission; quoting figures is fine. RFBerlin WP licence not checked. | High |
| France Stratégie | Etalab 2.0 (except third-party IP) | <https://www.strategie-plan.gouv.fr/mentions-legales> | source + URL | Page is internally inconsistent; figures are fine | Medium–high |
| DGFiP (Analyses n°8, open tables) | Licence Ouverte 2.0 | <https://www.impots.gouv.fr/mentions-legales> | source + date | graphics excluded | High |
| DREES | Not verified (site unreachable) | — | — | likely Etalab | Low |
| Assemblée nationale reports | Not verified; AN open data uses Licence Ouverte | — | cite report | quoting figures is fine | Low |
| Future CASD outputs | CASD FAQ | casd.eu FAQ | "…Centre d'accès sécurisé aux données – CASD (Réf. 10.34724/CASD)" | mandatory on subsidised rate | High |

**Before publishing:**
1. Add a `LICENSE`. Suggested: MIT for `pipeline/` and `site/`, CC BY 4.0 for
   `docs/` and own derived tables.
2. Add `DATA_LICENSES.md` stating that third-party data keep their terms.
3. Resolve IdO, IPP, Notaires and Forbes. Either obtain permission or reduce the
   CSVs to cited facts.
4. Replace the README "Sources" section with a full attribution block. One line per
   producer is needed: WID (vintage date), « Source : Insee », "Source: ECB
   statistics", DGFiP/Etalab DVF, Paris Notaires Services, DGFiP Analyses n°8,
   France Stratégie NA 102, DREES ER 1055, IPP Note 92 and WP 2025, Challenges via
   IdO, and Forbes (totals only). Add the line "derived figures are our own
   calculations, not endorsed by any producer".

---

## 5. Documentation gaps (reproducibility for a new contributor)

1. **The WID vintage cannot be re-downloaded.** WID replaces the bulk zip in place.
   The build records ETag and SHA-256 (`france.json` → `meta.inputs_sha256`), but
   the raw file is gitignored and WID does not archive vintages.
   - Results cannot be reproduced once WID updates.
   - The licence question (§4) decides whether raw inputs can be deposited, e.g. on
     Zenodo. At minimum, say this in README.
2. **The Forbes series depends on an undocumented API.** It needs a browser
   User-Agent and breaches the ToS.
   - Banque de France files also need a User-Agent.
   - DREES URLs reset the connection.
   - Document these in the README or `pipeline/` comments and give archive URLs.
3. **Doc tables have no generating script.** dwa.md §4–5, insee.md §4–6,
   prices-housing §3 and 03-method §3.7/§3.8d say "recomputed", but no script
   regenerates them. A contributor cannot tell whether they are stale after a new
   vintage. Add `pipeline/report_tables.py` or a notebook, or mark each table with
   its build date.
4. **The `data/manual/*.csv` schemas are undocumented.** Columns, units, the
   ` | ` URL separator (explained only in rich-lists.md), and the conventions for
   "UNVERIFIED", "CONFLICT", "SUPERSEDED" and "LOWER BOUND" are not written down.
   - `ipp_top_income.csv` mixes superseded and current rows, with the status only in
     free text.
   - Add a `data/manual/README.md` and a `status` column.
5. **02-data §2.3 lists only three inputs.** It omits the DWA, INSEE (ERFS, HVP,
   CND), prices (CPI deciles, table 2.103) and housing (DVF, Notaires, HPI regions)
   files that `fetch.py` downloads via `pipeline/sources/`.
6. **The scenario parameters are not traced.** k, c and the Pareto-in-top-bin
   assumption are not linked to GGP's 1.8k-adults-per-family rule (M3). A reader
   cannot check that "the values GGP use" is accurate.
7. **No changelog or versioning of data revisions.** For example, the IPP Note 92
   revision, Challenges 2018 650→670, and the WID 2026 update round.
8. **The AI-assisted compilation is not disclosed.** Several CSV notes say
   "UNVERIFIED by the compiler … sub-search". Say in the README how rows were
   compiled and verified.
