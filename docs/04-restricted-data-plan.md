# 4. Restricted data plan: measuring the very top from administrative microdata

This page plans how the project could compute its seven layers, and the
billionaire layer, directly from French administrative microdata instead of
relying only on WID.world and rich lists.

- The data sit in the CASD (Centre d'accès sécurisé aux données). It is a
  secure remote-access service, and every project must pass the Comité du
  secret statistique (CSS).
- Facts are dated 2026-10-16. Each one cites the official page where it was
  read. Anything not read on a source page is marked **[not verified]**.
- Published figures already extracted from people who did this work are in
  `data/manual/ipp_top_income.csv` and `data/manual/top_wealth_estimates.csv`.

**Bottom line**

1. **A personal or open-source project cannot apply alone.** CASD bills and
   hosts only a legal entity (*personne morale*), and access is intended for
   non-profit research. We need a host research institution, in practice one
   of the teams in §4.7.
2. **The earliest realistic CSS session is 16 March 2027.** The 1 December
   2026 session needed producer agreement by 13 October 2026, which has
   passed. First data access is therefore plausible around mid-2027. That
   date is our estimate, not a published delay.
3. **Cost is modest.** Expect about €7–9k a year at the 2023 INFRASEC-A list
   price for one user on the large machine POTE needs. Research
   establishments get subsidised rates.
4. **The hard limit is wealth, not access.**
   - Total personal wealth (financial and real estate) was declared only
     under the wealth tax, the ISF, which ended in 2017.
   - Since 2018 the IFI covers real estate only.
   - Even the ISF excluded business assets (*biens professionnels*), which
     make up "au moins 66 %" of the wealth of the 380 richest tax units
     [AN-930, p.8].
   - So microdata give exact top *income* fractiles for 2003 onwards. Exact
     top *wealth* fractiles have to be rebuilt by capitalising income and
     valuing firms through ownership links, as IPP did for one year, 2016.

## 4.1 What microdata can do that public data cannot

| Question | Public data today | With CASD microdata |
|---|---|---|
| Exact thresholds, averages and shares of the top 0.1%, 0.01%, 0.001% and 0.0002% of income | WID fractiles, partly modelled; DGFiP open tables stop at deciles and tax brackets [DGFiP-IR] | Direct computation on the exhaustive income-tax file POTE: about 40 million tax units, 2003–2024 on CASD [CASD-POTE] |
| Income including profits kept inside controlled companies | Allocated in proportion to dividends received (DINA rule). IPP estimate that, for the top 75 tax units in 2016, this captures about 8% of their income as measured through ownership links (their benchmark, not a directly observed quantity) [WP25, §3.2.1] | Retained earnings attributed through observed ownership links: BIC-IS corporate returns, LIFI group links, the BADS2A link table [N92; WP25] |
| Mobility at the top (who stays in the top 0.001%) | Not possible | POTE is a panel of tax units. IPP find a 3-year stay rate in the top 0.001% of 15% for taxable income and 64% for comprehensive income [WP25, Table A1] |
| Wealth of the top 0.1–0.001% | WID capitalisation plus the Forbes top-up; rich lists | Capitalisation on POTE plus firm valuation from BIC-IS/FARE balance sheets. ISF totals for 2006–2017; IFI real estate for 2018–2022 [CASD-ISF] |
| Housing at market value by income or wealth rank | WID asset composition; survey values | Owners from FIDELI and the land registry, linked to transaction prices (DVF, public) |
| Inheritance received at the top | Estate-multiplier series | DMTG estate samples, but only 1994, 2006 and 2010 [CASD-DMTG] |
| Cross-checks | ERFS and Patrimoine (HVP) published tables | ERFS 2005–2023 and HVP 2017/2020/2023 microdata, thin at the top |

## 4.2 Datasets

Years are those listed in the CASD catalogue on 2026-10-16, unless noted.

| Dataset | Producer | Unit | Years on CASD | Coverage | What it gives us | Source |
|---|---|---|---|---|---|---|
| **POTE** (2042 income-tax returns and annexes) | DGFiP | tax unit (*foyer fiscal*) | 2003–2024 | Exhaustive: "l'ensemble des contribuables", about 40m tax units and 4,000 variables. Only the *département* code is given. | Exact top income fractiles; panel; capital income for capitalisation. IPP describe it as a 2003–2023 panel [WP25 §2.1.1]. | [CASD-POTE]; [DGFiP-POTE-deck] |
| **ISF-IFI** (wealth-tax returns, form 2725) | DGFiP | tax unit | 2006–2022 | All wealth-tax filers, about 350,000 in 2016 above €1.3m [WP25]. ISF (to 2017): real estate and financial wealth, business assets excluded [AN-930 p.8]. IFI (2018–): real estate only. | Total taxable wealth at the top to 2017; real estate after. Same identifier as POTE. | [CASD-ISF] |
| **ISF-IFI_long** | DGFiP | tax unit | 1994–2019 | Long panel, not linked to POTE | Long top-wealth panel | [CASD-ISF-long] |
| **BIC-IS** (corporate tax returns) | DGFiP | firm | 2016–2025 | All firms subject to corporate tax. Form 2033/59 lists shareholders owning at least 10% [N92, encadré 1]. | Profits, retained earnings, corporate tax paid, direct personal shareholders | [CASD-BICIS] |
| **LIFI** (financial links between firms) | INSEE / DGFiP | firm-to-firm links | 2012–2024 | Group structures | Pyramids: profits of subsidiaries traced up to the controlling household | [CASD-LIFI] |
| **FARE** (Esane) | INSEE / DGFiP | firm | 2008–2023 | All market firms | Balance sheets for valuing unlisted firms | [CASD-FARE] |
| **BADS2A** (shareholders and executives linked twice) | IPP / DGFiP / CASD | person-to-firm link | 2016 only | All observed shareholding links of tax units, from 2033/59 forms, Orbis and the RNCS company register, matched by CASD as trusted third party | The link that makes "economic income" possible | [N92, encadré 1]. Whether outside teams can use it: **[not verified]**, ask IPP/DGFiP. |
| **FIDELI** | INSEE / DGFiP | individual, household, dwelling | 2015–2024 | Exhaustive demographic file built from tax sources | Individualising tax units; linking people to dwellings | [CASD-FIDELI] |
| **Fichiers fonciers** (built-property file) | DGFiP | premises | only 2023 listed | Exhaustive land register | Owned dwellings by owner | [CASD-FONCIER] |
| **DVF** (property sale prices) | DGFiP / Etalab | transaction | public, about the last 5 years | All sales, except Alsace, Moselle and Mayotte | Market value of dwellings (open, no CASD needed) | [DVF] **[not verified on page]** |
| **ERFS** | INSEE / DGFiP | household | 2005–2023 | About 50k households, sample | Cross-check of disposable income; useless above roughly the top 1% | [CASD-ERFS] |
| **Histoire de vie et Patrimoine** (HVP) | INSEE | household | 2017, 2020, 2023 (earlier Patrimoine waves 1998–2014) | Survey with oversampling of the wealthy; feeds the euro-area HFCS | Assets not seen in tax data: deposits, life insurance, owner-occupied housing | [CASD-HVP]; [CASD-PAT] |
| **EDP** (permanent demographic sample) | INSEE / DGFiP | individual | 1968–2022 | Sample | Long individual trajectories; sampling rate **[not verified]** | [CASD-EDP] |
| **DMTG** (inheritance and gift duties) | DGFiP | estate | 1994, 2006, 2010 | Sample of estates; representativeness of 2010 "n'est pas établie" per CAE | Inheritance at the top, with large gaps | [CASD-DMTG]; [CAE69] |
| **Filosofi** | INSEE | household | on CASD after CSS review; years **[not verified]** | Exhaustive local income | Geography only | [INSEE-Filosofi] |

## 4.3 What we would compute

Each output is aggregated to a layer of this project. Unit conversions follow
[03-method.md](03-method.md).

1. **Exact income layers, 2003–2024 (POTE).**
   - Thresholds, averages and shares of fiscal income for the layers P90–99,
     P99–99.9, P99.9–99.99, P99.99–99.999 and top 0.001%, plus the top
     0.0002% (about 75 tax units). Compare with WID pre-tax income for the
     same years.
   - Tax units must be converted to adults. Wages and pensions are declared
     per person in the 2042 return, so they can be individualised (to check
     against the POTE documentation). Capital income is split equally
     within couples, as WID does.
   - IPP and the DGFiP publish results by tax unit. The DGFiP top 0.1%
     (40,700 tax units in 2022, entry €463,000) is an open anchor
     [DGFiP-A8; INSEE-FPS2025].
2. **"Economic income" including retained earnings, 2016 and beyond.**
   - Replicate IPP: add the profits kept in companies a household controls
     (at least 10% owned, or controlled), traced through LIFI pyramids, and
     the corporate tax those companies paid.
   - BADS2A exists only for 2016. Other years need new person-to-firm
     matching by a trusted third party (CASD/DGFiP), as IPP did.
   - IPP's 2016 benchmark is in `data/manual/ipp_top_income.csv`. The top
     0.1% share is 6.2% of comprehensive income against 3.4% of taxable
     income [WP25, Table 1].
3. **Wealth layers.**
   - (a) 2006–2017: total ISF-declared wealth for filers. Business assets
     are missing because they were exempt.
   - (b) All years: capitalise POTE capital income (the GGP method), using
     yields from national accounts.
   - (c) Business wealth of controlling owners: value controlled firms from
     BIC-IS/FARE balance sheets and listed prices, attributed via ownership
     links.
   - (d) Fill non-taxable assets (life insurance, deposits, main residence)
     from HVP.
   - Output: an independent top 0.01% / 0.001% wealth estimate, to set
     against the Forbes-adjusted WID and against Challenges (see
     [notes/rich-lists.md](notes/rich-lists.md)).
4. **Mobility.**
   - Transition matrices between layers over 1, 3 and 10 years from the
     POTE panel. Breaks in tax-unit identity at marriage, divorce or death
     need FIDELI or the EDP to follow individuals.
5. **Housing at market value.**
   - Link owners (Fichiers fonciers, FIDELI) to DVF local prices per m² and
     report owned housing at market value by income layer. This is the
     microdata version of planned extension §3.9-6.
6. **Inheritance at the top.**
   - DMTG samples for 1994, 2006 and 2010 only. CAE note 69 recommends
     depositing an anonymised inheritance register at CASD [CAE69], which
     does not exist yet.

## 4.4 Access procedure

**Who can apply**
- Only a legal entity can fund a subscription or host the access terminal:
  "seule une personne morale peut financer un abonnement"; "une SD-Box ne
  peut être hébergée qu'à l'adresse d'une personne morale" [CASD-FAQ].
- One project has a single funder [CASD-CONTRAT].
- CASD's main mission serves "utilisateurs poursuivant des fins non lucratives
  de recherche, d'étude, d'évaluation ou d'innovation"; private-sector use is
  a secondary mission [CASD-ENROL-2025].
- The CSS weighs "la qualité de la personne ou de l'organisme présentant la
  demande et les garanties qu'il présente" [CSS-PROC].
- No page we read says whether an NGO or an open-source collective is
  eligible **[not verified]**. Plan on a university or public research
  partner as applicant.
- Individual-level data also needs a GDPR processing record held by the host
  institution's data protection officer [DGFiP-POTE-deck].

**Steps** [CASD-HABIL; CSS-PROC]
1. Create an account on the CASD portal (cdap.casd.eu) and sign a
   confidentiality commitment.
2. Write the dossier: team, sources, project description. "L'usage de chaque
   source doit ainsi être justifié" [CSS-PROC].
3. Get the data producers' prior agreement at least two weeks before the
   deadline (DGFiP for POTE, ISF-IFI and BIC-IS; INSEE for FIDELI, ERFS, HVP,
   EDP, FARE and LIFI).
4. CSS opinion, given in session or by electronic consultation.
5. For tax data, the DGFiP then sends an "Autorisation de communication de
   données fiscales", signed for the budget minister [CSS-FAQ].
   - The legal basis is LPF art. L135 D (research access after CSS opinion).
     We could not open the Légifrance text **[not verified]**.
   - The CSS authorisation runs for 6 years [CSS-FAQ].
6. Signatures by producers and the Archives, a contract with CASD, then
   enrolment:
   - an online session of about 2 hours;
   - fingerprints of two fingers taken in person to issue the smart card;
   - an SD-Box terminal delivered to the host [CASD-ENROL].
   - Enrolment validity: the habilitation page says 4 years, the enrolment
     page and the 2025 deck say 6 years.

**CSS calendar** (new projects) [CSS-CAL]. The CSS holds four sessions a year
plus about eight electronic consultations [CSS-FONCT].

| CSS session | Producer agreement by | Dossier by |
|---|---|---|
| 1 Dec 2026 | 13 Oct 2026 (passed) | 2 Nov 2026 |
| **16 Mar 2027** | 26 Jan 2027 | 15 Feb 2027 |
| 1 Jun 2027 | 13 Apr 2027 | 3 May 2027 |
| 5 Oct 2027 | 17 Aug 2027 | 6 Sep 2027 |
| 30 Nov 2027 | 12 Oct 2027 | 2 Nov 2027 |

The 2027 producer deadlines are labelled "si ajout de sources" on the page.

**Delays**
- Formalities after the opinion "peuvent néanmoins prendre plusieurs
  semaines" [CSS-PROC].
- A CNRS guide counts "en moyenne trois semaines" for signatures and advises
  planning for "plusieurs mois" [CNRS-guide].
- INSEE: "Ce processus peut prendre des mois" [INSEE-CS].
- Our estimate is 6–8 months from now to first login (16 March 2027 CSS,
  then authorisation, contract and enrolment). This is derived from the
  calendar, not a published figure.

**Fees** (INFRASEC-A, "tarifs applicables à compter du 01/01/2023") [CASD-TARIFS]
- **Standard package: €253 per month.** It includes 1 user, 20 exports and
  MS Office.
- **SD-Box: €37 per month** per access point.
- **Extra users:** +€39, +€37, +€32 and +€27 per month for users 2 to 5,
  then +€22 for each user from the 6th.
- **Larger machines:** configurations 2–5 add €74, €147, €327 or €466 per
  month.
- **Extra exports:** €318 for a pack of 10.
- **Terms:**
  - The minimum project length is one year.
  - The page says research establishments get "les tarifs subventionnés",
    without saying whether that means this grid or a further cut.
  - Students, PhD candidates and post-docs get reductions.
  - The page does not say whether these prices are before or after VAT (HT
    or TTC).
- **INFRASEC-DMA grid** ("organismes publics et entreprises"): €601–3,234
  HT a month, plus €63 HT per user a month, plus €2,120 HT setup. This would
  apply if the host is not a research establishment.
- **Our budget estimate: about €7.4–9.1k a year** on INFRASEC-A.
  - POTE needs a "configuration élevée (4 ou 5)" [DGFiP-POTE-deck].
  - One user with configuration 4 or 5 costs about €617–756 a month
    (derived).

**Output checking (what can leave the secure environment)** [CASD-FAQ; CASD-ENROL-2025]
- Every export is checked by CASD. A project gets 20 export credits of 30
  minutes each, and each output needs a text file describing it.
- Household data: cells of "pas moins de 11 individus".
- Tax data: "seuil de 11 unités, une unité ne peut représenter plus de 85% du
  total d'une case".
- Consequences for us:
  - Our smallest layers are 378 tax units (top 0.001%) and 75 tax units (top
    0.0002%), which passes the count rule.
  - The 85% dominance rule could block a cell where one fortune dominates.
    IPP published averages for the top 75, so layer-level statistics are
    feasible.
  - Single-year thresholds near one person are not.
- Code written inside CASD would have to leave through the same export check
  **[not verified]**, as would the import rules for code written outside.
  Either way the scripts can be published; the microdata never leave.

## 4.5 Proposed project design

1. **Host.** Join an existing CASD project, or co-apply with a team that
   already holds POTE, BIC-IS and LIFI (§4.7). Joining an existing project
   might avoid a new full CSS dossier and a new trusted-third-party
   matching; how the CSS handles new users and new purposes on an existing
   project is **[not verified]**.
2. **Scope of the first dossier.**
   - POTE 2003–2024 and ISF-IFI 2006–2022: income and wealth layers,
     mobility.
   - BIC-IS 2016–2025, LIFI and FARE: retained earnings and firm values.
   - FIDELI and Fichiers fonciers: individualisation and housing.
   - HVP: imputation of non-taxable assets.
   - Each source justified against an output in §4.3.
3. **Outputs.** Only aggregated tables by layer and year, the same shape as
   `site/data/france.json`, plus the code. Each table is labelled
   "computed on CASD, project ref. …" and sits next to the WID series, never
   silently replacing it.
4. **Timeline** (estimate):
   - Nov 2026 – Jan 2027: agree a partner, draft the dossier, ask the
     producers.
   - 26 Jan 2027: producer agreements.
   - 15 Feb 2027: dossier.
   - 16 Mar 2027: CSS.
   - Spring 2027: DGFiP authorisation, CASD contract, enrolment.
   - Mid-2027: first exports.
5. **Meanwhile, open anchors**, already in `data/manual/`:
   - DGFiP Analyses n°8: top 0.1% income and wealth, 2003–2022, with Excel
     [DGFiP-A8].
   - INSEE *France, portrait social* 2025 (POTE-based) [INSEE-FPS2025].
   - DGFiP income-tax and IFI open tables [DGFiP-IR; DGFiP-IFI].
   - IPP's 2016 tables [N92; WP25].

## 4.6 Known limits

- **No total wealth in tax data after 2017.** IFI covers real estate only,
  and ISF never included exempt business assets. The DGFiP itself calls this
  "une rupture de série" [DGFiP-A8, p.2]. Top wealth from microdata will
  still be partly modelled.
- **Tax units are not adults.** Splitting requires assumptions, and
  individual identifiers need FIDELI or the EDP.
- **Non-residents are out of scope.** French-citizen billionaires living
  abroad are outside POTE. Challenges and Forbes include some of them; see
  [notes/rich-lists.md](notes/rich-lists.md).
- **Ownership links exist only from 10%.** The 2033/59 form lists
  shareholders of at least 10%. Smaller stakes in listed firms are seen only
  through dividends.
- **BADS2A is a single cross-section (2016).** Its reuse by outside teams is
  unconfirmed.

## 4.7 Candidate research partners

| Team | What they did with these data | Link |
|---|---|---|
| **IPP** (Institut des politiques publiques, PSE/GENES): L. Bach (ESSEC), A. Bozio (PSE/EHESS), A. Guillouzouic (AMSE/CNRS), C. Malgouyres (CREST/CNRS) | Built BADS2A with the DGFiP and CASD (POTE, ISF-IFI, BIC-IS, Orbis, RNCS) for 2016; top 0.0002% income and tax rates; persistence; link to Challenges | [N92]; [WP25] |
| **CAE** (Conseil d'analyse économique), same IPP authors with N. Grimprel and C. Landais | Focus 118 (July 2025): emigration of the top 1% by capital income, from POTE, ISF-IFI and BADS2A | [CAE-F118] |
| **CAE note 69** (Dherbécourt, Fack, Landais, Stantcheva, 2021) | Inheritance, using DGFiP extractions; recommends depositing an inheritance register at CASD | [CAE69] |
| **PSE / World Inequality Lab**: B. Garbinti (Banque de France / CREST), J. Goupille-Lebret, T. Piketty | WID France series. Exhaustive income-tax micro-files "since 2010 … about 37 million tax units"; estate-tax samples. The benchmark this project already uses. | [GGP-DINA-app]; [GGP-wealth] |
| **DGFiP statistics office** (O. Arnal, R. Loiseau, V. Vicaire) | DGFiP Analyses n°8: top 0.1% income (POTE) and wealth (ISF 2003–2016, IFI 2017–2022); INSEE *France, portrait social* 2025 chapter | [DGFiP-A8]; [INSEE-FPS2025] |
| **INSEE** (J.-M. Germain and others) | Distributional national accounts by household ("revenu élargi"), from ERFS; finest group the top 5% | [INSEE-A88] |
| **Banque de France** (A. Mesnard) | Experimental distributional wealth accounts from HVP; does not reach the top 1% yet | [BDF-DWA] |
| **CREST** | Home of Malgouyres and Garbinti (above); no separate team page checked **[not verified]** | — |
| **Cour des comptes / Conseil des prélèvements obligatoires** | December 2025 report on distortions in wealth taxation; site not reachable for checking **[not verified]** | [CDC-2025] |

## 4.8 References

- [AN-930] Assemblée nationale, commission des finances, rapport n°930 on the PPL for a 2% minimum tax on ultra-high wealth, Feb 2025. https://www.assemblee-nationale.fr/dyn/17/rapports/cion_fin/l17b0930_rapport-fond.pdf
- [N92] Bach, Bozio, Guillouzouic, Malgouyres, *Quels impôts les milliardaires paient-ils ?*, Note IPP 92, June 2023 (revised PDF 2025). https://www.ipp.eu/wp-content/uploads/2025/05/92_Note_IPP_Billionaires-version-actualisee.pdf
- [WP25] Same authors, *Do Billionaires Pay Taxes?*, RFBerlin DP 70/25, Sept 2025. https://www.rfberlin.com/wp-content/uploads/2025/09/25070.pdf
- [CAE-F118] CAE Focus 118, July 2025. https://cae-eco.fr/static/pdf/Focus_118_emigration_fiscale_250725_v2.pdf
- [CAE69] CAE note 69, *Repenser l'héritage*, Dec 2021. https://cae-eco.fr/static/pdf/cae-note069.pdf
- [DGFiP-A8] DGFiP Analyses n°8, *Revenus et patrimoine des foyers les plus aisés en France*, Jan 2025. https://www.impots.gouv.fr/dgfip-analyses-revenus-et-patrimoine-des-foyers-les-plus-aises-en-france
- [INSEE-FPS2025] INSEE, *France, portrait social* 2025. https://www.insee.fr/fr/statistiques/8612588
- [INSEE-A88] INSEE Analyses 88 (2023). https://www.insee.fr/fr/statistiques/7669723
- [GGP-DINA-app] Garbinti, Goupille-Lebret, Piketty, DINA appendix (WID WP 2017/5). https://wid.world/www-site/uploads/2017/04/GGP2017DINAAppendix_WIDWP201705-1.pdf
- [GGP-wealth] Same authors, WID WP 2016/5. https://wid.world/document/b-garbinti-j-goupille-and-t-piketty-wealth-concentration-in-france-1800-2014-methods-estimates-and-simulations-2016/
- [BDF-DWA] Banque de France, distributional wealth accounts, Feb 2024. https://www.banque-france.fr/fr/publications-et-statistiques/publications/de-nouvelles-statistiques-sur-la-distribution-du-patrimoine-des-menages-dans-la-comptabilite
- [CDC-2025] https://www.ccomptes.fr/fr/publications/corriger-les-principales-distorsions-de-limposition-du-patrimoine
- [CASD-POTE] https://www.casd.eu/en/source/income-tax-declarations-for-tax-households-form-2042-and-appendices/
- [DGFiP-POTE-deck] DGFiP presentation of POTE on CASD, March 2025. https://casd.eu/wp/wp-content/uploads/presentation_donnees-POTE_CASD_mars2025.pdf
- [CASD-ISF] https://www.casd.eu/en/source/panel-file-of-taxpayers-subject-to-wealth-tax-and-real-estate-wealth-tax/
- [CASD-ISF-long] https://www.casd.eu/en/source/long-panel-file-of-taxpayers-subject-to-the-wealth-tax-and-the-real-estate-wealth-tax/
- [CASD-BICIS] https://casd.eu/en/source/industrial-and-commercial-profits-all-schemes
- [CASD-LIFI] https://www.casd.eu/en/source/financial-links-between-enterprises/
- [CASD-FARE] https://www.casd.eu/en/source/annual-structural-statistics-of-companies-from-the-esane-scheme/
- [CASD-FIDELI] https://www.casd.eu/en/source/housing-and-individual-demographic-file/
- [CASD-FONCIER] https://www.casd.eu/en/source/built-property-land-register-file/
- [CASD-ERFS] https://www.casd.eu/en/source/tax-and-social-incomes-survey/
- [CASD-HVP] https://casd.eu/en/source/life-history-and-wealth-survey
- [CASD-PAT] https://casd.eu/en/source/household-wealth-survey
- [CASD-EDP] https://www.casd.eu/en/source/permanent-demographic-sample
- [CASD-DMTG] https://casd.eu/en/source/duties-on-the-free-transfer-of-assets/?tab=1
- [INSEE-Filosofi] https://insee.fr/en/metadonnees/source/operation/s2146/acces-micro-donnees
- [DVF] https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/
- [DGFiP-IR] https://www.impots.gouv.fr/node/28082
- [DGFiP-IFI] https://www.impots.gouv.fr/impot-sur-la-fortune-immobiliere-ifi
- [CASD-FAQ] https://www.casd.eu/gerer-son-projet/faq/
- [CASD-CONTRAT] https://www.casd.eu/gerer-son-projet/contractualisation-2/
- [CASD-HABIL] https://www.casd.eu/gerer-son-projet/procedures-dhabilitation/
- [CASD-ENROL] https://www.casd.eu/gerer-son-projet/seance-denrolement-2/
- [CASD-ENROL-2025] CASD enrolment presentation, April 2025. https://www.casd.eu/wp/wp-content/uploads/CASD_Presentation_Enrolement_20250402.pdf
- [CASD-TARIFS] https://www.casd.eu/tarifs-2/
- [CSS-PROC] https://www.comite-du-secret.fr/procedure/
- [CSS-FAQ] https://www.comite-du-secret.fr/foire-aux-questions-faq/
- [CSS-FONCT] https://www.comite-du-secret.fr/presentation-du-comite/fonctionnement/
- [CSS-CAL] https://www.comite-du-secret.fr/calendrier/nouveaux-projets-et-demandes-de-prolongation-au-dela-de-8-ans/
- [CNRS-guide] CNRS PPR Autonomie, *Accéder aux données diffusées par le CASD* (27/01/2023). https://www.enssib.fr/bibliotheque-numerique/documents/71037-acceder-aux-donnees-diffusees-par-le-casd.pdf
- [INSEE-CS] INSEE, *Courrier des statistiques* n°3. https://www.insee.fr/fr/statistiques/fichier/4254227/courstat-3-7.pdf
