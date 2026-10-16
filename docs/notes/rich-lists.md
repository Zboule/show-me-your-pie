# Rich lists and the top tail of French wealth

Purpose: check that the WID.world backbone, which stops at the top 0.001% (about 530 adults), does not understate billionaire wealth. Data: `data/manual/challenges_500.csv` and `data/manual/forbes_france_billionaires.csv`. In both files, `source_url` can hold several URLs separated by ` | `, and `quote` holds the exact phrase from each one, in the same order. Every figure is quoted from a published article; see [rich-lists-sources.md](rich-lists-sources.md). Last checked 2026-10-16.

## 1. What each list measures

**Challenges, "Les 500 plus grandes fortunes de France"** (annual, early July, 1996 to 2026)
- **Scope.** Professional wealth only: stakes in listed and unlisted firms. Personal assets such as property and art are excluded [1][2].
- **Unit.** Families, not individuals. Entries like "famille X dont Y" mix single people and whole dynasties. The 2026 edition counts "153 familles milliardaires" [3].
- **Method** (from GGP's 2016/2017 data appendix H, WID WP 2016/6, citing Challenges' own methodology note) [4]:
  - Listed shares are valued at market price.
  - Unlisted firms are valued from accounts and comparable transactions; only about a third of families hold listed shares.
  - Figures are gross wealth, not net.
  - People in the list are sent their estimate and can comment on it.
  - Around 2013, GGP estimated that about 100 families, holding roughly 20% of the total, live outside France. They call this a lower bound.
- **Valuation date.** Not stated in any source we found; only the publication date in early July is known.
- **Currency and revisions.** Totals were published in francs until 2001. Our CSV keeps those franc amounts in the notes and gives no euro total for those years, because we do not convert. Euro totals are the figures quoted in press coverage of each edition, mostly AFP relays, and are often rounded. Where no edition-year figure exists, we use an exact figure stated in a later article, flagged as retrospective in the note. Challenges later revises some figures: its current web pages show 711 for 2019 against 700 in the AFP coverage at publication, and 2025 is restated as 1 129 against 1 128. Older compilations also give 394 for 2014 against 390 at publication, and 670 for 2018 against 650. Treat the series as ±3%. Totals are missing for 1997, 1998, 2002, 2003, 2005, 2008, 2011, 2015 and 2021 (1997 has no row).
- **Bias.** Leaving out non-business assets pushes the totals down. Grouping by family, including non-residents, and valuing at market price push them up; Challenges documents no liquidity or tax discount.
- **Comparing with WID.** WID uses individual adults with wealth split equally within couples, so "500 families ≈ top 0.001%" is only a loose match.

**Forbes World's Billionaires** (annual, early April)
- **Valuation date.** A snapshot of stock prices and exchange rates in early March (11 March for the 2022 list) [5].
- **Unit.** Individuals, including "wealth belonging to a billionaire's spouse and children if that person is the founder".
- **Assets.** Covers "private companies, real estate, art and more", and discounts fortunes that lack documentation [5].
- **Country.** Assigned by citizenship, not residence, so some French billionaires on the list live abroad.
- **How our CSV is built.** It covers the 2017–2025 editions. Each count and total is quoted from a published article, mostly Forbes France's annual piece on French billionaires or AFP relays of it; none is computed by us. Totals are kept in the currency the article states. USD totals: 2017, 2021, 2022. EUR totals: 2017 (AFP's approximate conversion), 2020, 2021, 2024. 2018, 2019, 2023 and 2025 have a count only. No article we could reach gives a count or total for 2010–2016 or 2026.

## 2. How WID France estimates the top

The benchmark is Garbinti, Goupille-Lebret & Piketty (GGP), "Accounting for Wealth-Inequality Dynamics: Methods, Estimates, and Simulations for France", *JEEA* 19(1):620–663, 2021 [6] (working paper: WID WP 2016/5 [7]).

- **1970–2014: mixed income capitalization-survey method.**
  - Capital income from the income-tax micro-files is capitalized. These files oversample the top and are exhaustive at the very top.
  - Assets that produce no taxable income (owner-occupied housing, deposits, life insurance) are imputed from wealth surveys.
  - The result is scaled to national accounts, with wealth split equally between adult partners.
- **1800–1970: estate-multiplier method on inheritance records.** For 1984–2010 it also serves as a cross-check.
- **Wealth-tax (ISF) data and rich lists are not inputs.** In the authors' words: "We also offer detailed comparisons and reconciliations with other data sources (wealth tax data and billionaire lists) for the recent period, although we do not formally use them for our benchmark series." And: "there is so much uncertainty about billionaire lists that they should be used with a lot of caution" [7].

**After 2014**
- **To 2020.** Technical Note 2021/16 [8]: "We extrapolate the wealth distribution series of [GGP] (2021) forward up to 2020 by fixing the asset composition by percentile to 2014." The shares then move only with the asset totals in the national accounts.
- **Forbes correction.** Technical Note 2025/01 (December 2025) [9] now applies one: "In cases where WID billionaire wealth is lower than Forbes, we add to the 127th g-percentile of each country the difference between the theoretical and Forbes total wealth of billionaires." The added amount is taken proportionally from the rest of the distribution. The note adds that "our raw uncorrected estimates for countries like France or Britain significantly underestimate billionaire wealth."
- **Consequence for us (checked).** The vintage we download is Forbes-adjusted: the `WID_metadata_FR.csv` source field for `shwealj992` / `ahwealj992` cites Bajard, Bauluz, Brassac, Chancel, Martínez-Toledano, Piketty, Sodano (2025), "Global wealth inequality on WID.world: Estimates and imputations", which is Technical Note 2025/01. So WID's top 0.001% is at least the Forbes total in recent years. What remains open is the layer just below: see [03-method.md §3.7](../03-method.md#37-the-very-top-calibration-rich-lists-scenarios), where Challenges' 500 families now exceed WID's whole top 0.01%.

## 3. Methods that combine rich lists with survey or tax data

- **Vermeulen (2018)**, "How Fat is the Top Tail of the Wealth Distribution?", *Review of Income and Wealth* 64(2):357–387. Adds Forbes observations to wealth surveys, then fits a Pareto tail. A few extreme observations remove most of the downward bias.
- **Bach, Thiemann & Zucco (2019)**, "Looking for the missing rich: tracing the top tail of the wealth distribution", *International Tax and Public Finance* 26(6):1234–1258. HFCS survey data plus Forbes and national rich lists, for France, Germany and Spain. The 2015 working-paper version used the 2010 Challenges list [10].
- **Blanchet & Martínez-Toledano (2023)**, "Wealth inequality dynamics in Europe and the United States: Understanding the determinants", *Journal of Monetary Economics* 133:25–43. Combines tax-based series, the HFCS and national accounts, with no rich-list correction of its own.
- **ECB Distributional Wealth Accounts (DWA)** [11]:
  - A Pareto tail above about €1m, fitted on the HFCS plus rich lists, following Vermeulen.
  - France compiles its own DWA. ECB Working Paper 2687 (Engel, Gayà Riera, Grilli & Sola, 2022) is an ECB-staff overview of the rich lists available at HFCS wave 3 and lists "FR – Challenges (504)" [12]; it does not say which list France's DWA uses in every wave.
  - The Banque de France methodology note [13] (readable with a browser User-Agent; see [notes/dwa.md](dwa.md)) speaks of "classements … fournis par la presse nationale", adjusted for family size, country of residence and valuation differences from ESA 2010 (not "illiquidity", as an earlier version of this note said).
- **Others** (verified via Crossref):
  - Waltl & Chakraborty (2022), *Journal of Economic Inequality* 20(1):169–203.
  - Waltl (2022), *Review of Income and Wealth* 68(1):74–108.
  - Cantarella, Neri & Ranalli (2024), *Review of Income and Wealth* 70(3):551–580.
  - Saez & Zucman (2016), *Quarterly Journal of Economics* 131(2):519–578, which uses the Forbes 400 only as a check.

## 4. French studies of billionaires' income and taxation

- **IPP Note n°92 (June 2023)**, Bach, Bozio, Guillouzouic & Malgouyres, "Quels impôts les milliardaires paient-ils ?" [14].
  - Data: 2016 tax and firm data, linked through holding companies.
  - "Billionaires" here means the top 0.0002% by economic income, which is 75 households.
  - Total tax rate: falls "de 46 % pour les 0,1 % les plus riches, à 26 % pour les 0,0002 %". Personal taxes are about 2% of economic income for the top 378 households.
  - The note does not use Challenges. The follow-up working paper, "Do Billionaires Pay Taxes?" (2025), matches the Challenges list to the tax data as a check: the top 75 have about an 85% chance of appearing in the list [15].
- **Zucman's report for the G20 (25 June 2024)**, "A blueprint for a coordinated minimum effective taxation standard for ultra-high-net-worth individuals" [16]. A 2% minimum tax on about 3,000 billionaires would raise "$200-$250 billion per year". Their current effective tax rate is "equivalent to 0.3% of their wealth".
- **The "taxe Zucman" in France**: a 2% floor on wealth above €100m.
  - The Assemblée nationale passed it on 20 February 2025 by 116 votes to 39. The Sénat rejected it on 12 June 2025 by 188 to 129 [17]. It was rejected again in the 2026 budget on 31 October 2025, 172 for and 228 against [18].
  - Assemblée report n°930 cites Zucman's estimate, extrapolated from Challenges, of "1 800 … foyers fiscaux possédant un patrimoine supérieur à 100 millions" [19].
  - The same report puts their wealth at about 1,500 Md€ in its optimistic scenario. That is 1,200 Md€ for the Challenges 500 (whose 2024 total was 1,228 Md€) plus 300 Md€ for taxpayers between €100m and €245m. Its estimated yield is 15.3 to 25.5 Md€.
  - The report calls €245m both Challenges' entry threshold and the average fortune; only the threshold reading is consistent with the figures.
  - The DGFiP gave no count of households, and the bill's explanatory memorandum says about 4,000.

## 5. Known comparisons

- **GGP (2016, rev. January 2017), WID WP 2016/6, appendix H [4]** is the only published reconciliation of WID-type estimates with Challenges that we found.
  - It covers the top 0.001% share for 1998–2013.
  - Families are split into 1, 10 or 15 members (based on US Forbes family sizes), with 80% of members assumed married.
  - About 20% of the wealth is removed as held by non-residents.
  - Result: the corrected Challenges series is "consistent" with their benchmark, while uncorrected lists come out higher. The numbers are in a separate Excel file we have not retrieved.
- **WIL Technical Note 2025/01 [9]**: uncorrected WID France estimates fall short of Forbes billionaire wealth.
- **Rough scale**: press coverage of the 2019 Challenges list described its 700 Md€ as "6 % du patrimoine actuel des Français" [20].

## References

1. https://fashionunited.fr/actualite/people/la-fortune-des-500-plus-riches-francais-depasse-1-200-milliards-deuros-pour-la-premiere-fois-selon-challenges/2024071835536 (AFP, 2024: "l'ensemble des actifs professionnels, cotés ou non cotés … ne prend pas en compte les biens personnels")
2. https://bourseinside.fr/economie/la-fortune-des-500-francais-les-plus-riches-bat-tous-les-records
3. https://fashionunited.fr/actualite/people/bernard-arnault-redevient-la-1ere-fortune-professionnelle-de-france-selon-challenges/2026070842308
4. https://wid.world/document/b-garbinti-j-goupille-t-piketty-appendix-wealth-concentration-france-1800-2014-methods-estimates-simulations-2016/
5. https://web.archive.org/web/20220627132403/https://www.forbes.com/billionaires/ (methodology text only; per-year figures and their articles are in the CSV)
6. https://doi.org/10.1093/jeea/jvaa025
7. https://wid.world/document/b-garbinti-j-goupille-and-t-piketty-wealth-concentration-in-france-1800-2014-methods-estimates-and-simulations-2016/
8. Blanchet, T., Martínez-Toledano, C. (2021), "Distributional Wealth Accounts in Europe: Methodology", World Inequality Lab Technical Note 2021/16 (the URL slug says 2021-12): https://wid.world/document/distributional-financial-accounts-in-europe-world-inequality-lab-technical-note-2021-12/
9. https://wid.world/document/global-wealth-inequality-on-wid-world-estimates-and-imputations-world-inequality-lab-technical-note-2025-01/
10. https://doi.org/10.1007/s10797-019-09578-1 ; https://www.diw.de/documents/publikationen/73/diw_01.c.513261.de/dp1502.pdf
11. https://data.ecb.europa.eu/sites/default/files/2024-01/DWA%20Methodological%20note_0.pdf
12. https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp2687~a91d434d45.en.pdf
13. https://www.banque-france.fr/system/files/2024-02/Donnees_et_methodologie_comptes%20distributionnels%20de%20patrimoine%20des%20m%C3%A9nages_2024_02_07.pdf
14. https://www.ipp.eu/publication/note-ipp-n92-quels-impots-les-milliardaires-paient-ils/
15. https://www.rfberlin.com/wp-content/uploads/2025/09/25070.pdf
16. https://taxobservatory.world//www-site/uploads/2024/06/report-g20.pdf
17. https://lcp.fr/actualites/fiscalite-en-premiere-lecture-l-assemblee-adopte-un-impot-plancher-de-2-sur-le ; https://www.publicsenat.fr/actualites/economie/taxe-zucman-le-senat-rejette-la-creation-dun-nouvel-impot-sur-les-ultra-riches
18. https://datan.fr/votes/legislature-17/vote_3300 (secondary aggregator; the official records are Assemblée nationale scrutins n° 881 and n° 3300 and Sénat scrutin n° 322, which the source review confirmed)
19. https://www.assemblee-nationale.fr/dyn/17/rapports/cion_fin/l17b0930_rapport-fond.pdf ; https://www.assemblee-nationale.fr/17/pdf/propositions/pion0768.pdf
20. https://fr.fashionnetwork.com/news/Le-luxe-domine-le-classement-challenges-des-fortunes-francaises,1116501.html
21. Other DOIs: 10.1111/roiw.12279 ; 10.1016/j.jmoneco.2022.11.010 ; 10.1007/s10888-021-09519-1 ; 10.1111/roiw.12519 ; 10.1111/roiw.12657 ; 10.1093/qje/qjw004
