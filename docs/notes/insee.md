# INSEE distribution statistics as a cross-check on WID

Purpose: compare WID.world, our backbone, with INSEE's official distribution statistics for income and wealth. INSEE is an independent source. It ranks people differently and measures different concepts. Code: `pipeline/sources/insee.py`; run it with `python3 -I pipeline/sources/insee.py <raw_dir>`. Every INSEE number below was parsed from the downloaded xlsx files, and every WID number was computed from `site/data/france.json`. Values described as "derived" are our own arithmetic on published figures, with the formula given. Last checked 2026-10-16.

## 1. Tables used

| Key in `load()` | INSEE publication (page) | File | Years | Unit |
|---|---|---|---|---|
| `erfs_indicators` | Niveau de vie et indicateurs d'inégalités ([2491918](https://www.insee.fr/fr/statistiques/2491918)) | `reve-niv-vie-indic-inegalite.xlsx` | 1975, 1979, 1984, 1990, 1996–2024 | constant 2024 € per UC; S20…S90 shares; Gini |
| `erfs_deciles` | Distribution des niveaux de vie ([2416808](https://www.insee.fr/fr/statistiques/2416808)) | `reve-niv-vie-decile-individu.xlsx` | 1996–2024 | D1…D9, P95, constant 2024 € |
| `erfs_mean_by_decile` | ERFS séries longues 1996–2023, DNV01bis ([8731524](https://www.insee.fr/fr/statistiques/8731524)) | `irsocerfs2023_DNV01_bis.xlsx` | 1996–2023 | mean niveau de vie per tenth, constant 2023 € |
| `erfs_decile_shares` | same, DNV02 | `irsocerfs2023_DNV02.xlsx` | 1996–2023 | share of total niveau de vie per tenth |
| `erfs_vingtiles` | same, DNV01 | `irsocerfs2023_DNV01.xlsx` | 1996–2023 | P5…P95, constant 2023 € |
| `erfs_before_redistribution` | same, IG5 | `irsocerfs2023_IG5.xlsx` | 1996–2023 | deciles of niveau de vie *before* redistribution, constant 2023 € |
| `erfs_ig1` | same, IG1 | `irsocerfs2023_IG1.xlsx` | 1996–2023 | as `erfs_indicators`, unrounded Gini (used as a check) |
| `hvp_inequality`, `hvp_thresholds` | Insee Focus 371, complementary tables 1–2 ([8672665](https://www.insee.fr/fr/statistiques/8672665)) | `IF371.xlsx` | 2015, 2018, 2021, 2024 | top 50/25/10/5/1% shares of gross wealth; D1…P99 of gross and net wealth |
| `hvp_long_series` | Patrimoine … séries longues ([8263048](https://www.insee.fr/fr/statistiques/8263048)) | `hvp_series_longues_fr.xlsx` | 1998, 2004, 2010, 2015, 2018, 2021 | mean gross wealth *hors reste* by bracket, deciles, Gini, current € |
| `hvp_net_by_gross_2021` | Patrimoine … en 2021 ([8262352](https://www.insee.fr/fr/statistiques/8262352)) | `hvp_mtmoymed_patbrut_patnet_fr.xlsx` | 2021 | mean gross and net wealth by tenth of gross wealth |
| `hvp_lorenz_2021` | RPM 2024 vue d'ensemble, fig. 2 ([7941439](https://www.insee.fr/fr/statistiques/7941439)) | `RPM2024-VE2.xlsx` | 2021 | Lorenz curve of gross wealth hors reste (check) |
| `cnd_2019` | Insee Analyses 88, André, Germain & Sicsic 2023 ([7669723](https://www.insee.fr/fr/statistiques/7669723)) | `IA88.xlsx` | 2019 | distributed national accounts by twentieth, € per UC |
| `cnd_2022` | Insee Première 2022 ([8275760](https://www.insee.fr/fr/statistiques/8275760)) | `ip2022.xlsx` | 2022 | CND by tenth and twentieth, € bn |
| `cnd_2023` | Insee Analyses 118 ([8974371](https://www.insee.fr/fr/statistiques/8974371)) | `IA118.xlsx` | 2023 | CND by tenth, € bn; inequality indicators |

`load()` runs these consistency checks, and all of them currently pass:
- The 2023 values in the 1975–2024 table equal those in the 1996–2023 IG1 table.
- The tenths in DNV02 sum to 100%.
- The CND tenths and twentieths sum to the published total.
- The 2019 CND consumption-unit counts we derive add up to the published total.
- The 2021 top 10% share derived from the long wealth series matches the Lorenz curve: 48.5% vs 48.3%.

## 2. What each INSEE measure is

**ERFS *niveau de vie***
- **Concept.** Household disposable income divided by consumption units (UC). The OECD-modified scale gives 1 to the first adult, 0.5 to each other person aged 14 or over, and 0.3 to each child under 14. Every member of the household is given that niveau de vie.
- **Unit and ranking.** Statistics are over persons of all ages, ranked by niveau de vie.
- **Income included.** Wages, pensions, unemployment benefits, self-employment income and financial income (partly imputed), plus cash benefits, minus direct taxes (income tax, CSG/CRDS, housing tax).
- **Income excluded.** Imputed rents of owner-occupiers, in-kind transfers, collective spending, undistributed corporate profits, and indirect taxes.
- **Field.** Metropolitan France, ordinary housing only. Excluded: people in institutions, homeless people, households whose reference person is a student, and households with negative declared income.
- **Data.** The sample of the Labour Force Survey is matched to tax and benefit files. Top incomes therefore come from tax returns, but only for sampled households, so the top 1% is poorly measured (INSEE publishes nothing above P95 in these tables).
- **"Before redistribution"** (table IG5): the same unit and ranking, using income before taxes and social benefits. Pensions and unemployment benefits are treated as primary income.

**Wealth surveys** (Patrimoine 1998–2015, then *Histoire de vie et Patrimoine*, HVP)
- **Unit.** The household, ranked by household wealth (gross or net). No equivalence scale and no split between adults.
- **Concept.** Gross wealth = financial + housing + business + residual assets (cars, durables, jewellery, art). Net wealth = gross wealth minus debt. "Hors reste" excludes residual assets and is the only concept comparable since 1998.
- **Data.** The survey oversamples wealthy households using wealth-tax and tax data, but is not calibrated to national accounts. INSEE: "sans calage sur les masses des comptes de patrimoine".
- **Published shares.** INSEE publishes shares of *gross* wealth only. It publishes no top shares of net wealth (see §6).

**Distributed national accounts** (*comptes nationaux distribués*, CND, also called *revenu élargi*)
- **Total distributed.** All of net national income: €2,026 bn in 2019, €2,227 bn in 2022 and €2,083 bn in 2023 (each a published "Ensemble").
- **Ranking.** Persons are ranked by their *usual* ERFS niveau de vie and amounts are per UC. Because groups are never re-ranked by extended income, a "top 10%" share here is a concentration share, below the share the top 10% by extended income would hold. INSEE says so and calls its Gini a pseudo-Gini.
- **"Before transfers"** = extended primary income. Pensions and unemployment benefits are counted as transfers, not as primary income.
- **"After transfers"** (*niveau de vie élargi*) adds three things:
  - Cash benefits.
  - In-kind transfers allocated by use: health, education, housing.
  - Collective spending allocated equally per UC: about €4,200 per UC in every group in 2019 (IA88, figure 1).
- **Vintages.** The 2019 (IA88), 2022 (IP2022) and 2023 (IA118) vintages use different conventions. IA118 values general-government primary income at basic prices and shows the public deficit separately. Do not splice them.

## 3. How these measures differ from WID

| | WID (`ptinc`, `diinc`, `hweal`) | INSEE |
|---|---|---|
| Unit | adults 20+, income or wealth of couples split equally, children not counted | ERFS and CND: persons of all ages, household income pooled and divided by UC. HVP: households |
| Ranking | by the measure itself | ERFS: niveau de vie. CND: *usual* niveau de vie (no re-ranking). HVP: wealth |
| Total | national income / national household wealth (rescaled to national accounts) | ERFS: survey-and-tax disposable income. CND: national income. HVP: survey totals, not rescaled |
| Pensions | primary income in `ptinc` | primary income in ERFS IG5; a transfer in CND |
| In-kind and collective spending | included in `diinc`. WID's benchmark: health close to lump-sum, education and other spending in proportion to post-tax disposable income (DINA Guidelines Oct. 2025, p. 70; Bozio et al., *AEJ: Applied* 2024). The France metadata of this vintage cites Fisher-Post & Gethin (2023) and states that education is proportional; it says nothing on health | not in ERFS; in CND, allocated by use (in kind) and near-flat per UC (collective: national spending lump-sum, local spending by civil-servant payroll) |
| Imputed rents, undistributed profits | included | not in ERFS; included in CND |
| Top coverage | tax tabulations and micro-files, Pareto interpolation, down to the top 0.001% | ERFS: sample of tax returns. HVP: survey with oversampling. CND: built on ERFS microdata and scaled to national-accounts totals (Insee Méthodes 138); its top coverage is not assessed here |
| Prices | national income deflator, constant 2025 € | CPI, constant € of the last year |
| Field | France | ERFS: metropolitan France. HVP: France excluding Mayotte (metropolitan France before 2010). CND: France |
| Recent years | `ptinc` and `diinc` extrapolated from 2019 on; `hweal` from 2015 on | observed |

**Levels differ by construction, so we compare shares and ratios.**
- **Income in 2019.** WID's post-tax income per adult is €46,714 in 2025 €, or €40,116 in 2019 € once multiplied by WID's deflator (0.85876). Over 51.6 million adults that gives €2,070 bn, within 2% of the CND's net national income of €2,026 bn.
- **Same total, different unit.** The CND divides about the same total among 46.5 million UC (€43,560 per UC), and WID among 51.6 million adults.
- **ERFS levels are lower.** ERFS niveau de vie is much lower (2019 mean: €28,380 in 2023 €). It counts only disposable cash income: the CND's household disposable income is €1,423 bn, against €2,026 bn of national income.

### Series breaks

**ERFS.** Each break appears as two columns for the same year. `load()` keeps both and lists the runs between breaks in `segments`.
- **1975–1990, and the first "1996" column in the 1975–2024 file:** excludes financial income. This is not comparable with later years.
- **2010:** financial income is imputed from the Patrimoine 2010 survey.
- **2012:** the survey was renovated. Income tax is now the tax *paid* during the year. The pension bonus for parents of three or more children and employers' health-insurance contributions are now counted. Financial income is imputed from Patrimoine 2014–15.
- **2020:** a fragile year, and the start of a production chain rebuilt on the new Labour Force Survey.
- **Pre-2020 values differ from the Insee Première retropolation.** INSEE warns that its pre-2020 values differ from the retropolated series in the Insee Première "Niveau de vie et pauvreté en 2024". We did not download that series.

**Wealth surveys.**
- 2010 appears twice, under the old and the new method.
- Residual assets have been measured differently since 2014–15, hence the "hors reste" concept for long comparisons.
- Survey weights were recomputed in 2021 for the 2010–2018 waves, so values differ from older publications.
- The field became France excluding Mayotte in 2010.
- IF371 publishes 2015–2024 on the latest weights.

## 4. Income: ERFS vs WID post-tax income (`diinc`)

**WID column definitions.**
- Top 10% and bottom 50% shares are WID's own `share` series.
- P90/P10 = `threshold["90"]` / `threshold["10"]`.
- S80/S20 and Palma are derived from the 127 `gp` groups: S80/S20 = top 20% share / bottom 20% share; Palma = top 10% share / bottom 40% share.

**ERFS column definitions.**
- Top 10% = 1 − S90.
- Bottom 50% = S50.
- D9/D1, (100−S80)/S20, Palma and Gini are as published.

\* = WID extrapolation (WID's `extrapolated_from` is the first extrapolated year: 2019 for income, 2015 for wealth). 2018 is the last observed year for WID income.

| Year (ERFS column) | ERFS top 10% | WID top 10% | ERFS bottom 50% | WID bottom 50% | ERFS D9/D1 | WID P90/P10 | ERFS S80/S20 | WID S80/S20 | ERFS Palma | WID Palma | ERFS Gini |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1996¹ | 22.5 | 25.7 | 31.0 | 30.0 | 3.51 | 3.74 | 4.11 | 4.62 | 0.99 | 1.16 | 0.279 |
| 2000 | 23.5 | 25.6 | 30.8 | 30.7 | 3.50 | 3.46 | 4.18 | 4.33 | 1.04 | 1.12 | 0.286 |
| 2005 | 23.8 | 25.7 | 31.0 | 30.0 | 3.35 | 3.61 | 4.18 | 4.51 | 1.04 | 1.16 | 0.286 |
| 2008 | 24.3 | 26.0 | 30.9 | 30.1 | 3.38 | 3.52 | 4.27 | 4.47 | 1.07 | 1.16 | 0.289 |
| 2010 | 24.9 | 24.7 | 30.2 | 30.7 | 3.48 | 3.41 | 4.48 | 4.24 | 1.13 | 1.09 | 0.299 |
| 2010² | 25.3 | 24.7 | 30.1 | 30.7 | 3.45 | 3.41 | 4.52 | 4.24 | 1.15 | 1.09 | 0.303 |
| 2012 | 25.1 | 23.3 | 30.0 | 31.6 | 3.53 | 3.30 | 4.56 | 3.97 | 1.14 | 0.99 | 0.303 |
| 2012² | 25.0 | 23.3 | 30.1 | 31.6 | 3.54 | 3.30 | 4.60 | 3.97 | 1.14 | 0.99 | 0.302 |
| 2015 | 24.2 | 23.7 | 30.6 | 31.7 | 3.46 | 3.28 | 4.35 | 3.96 | 1.08 | 1.00 | 0.292 |
| 2018 | 24.8 | 23.8 | 30.3 | 31.9 | 3.49 | 3.17 | 4.45 | 3.91 | 1.12 | 1.00 | 0.298 |
| 2019 | 23.9 | 23.5* | 30.8 | 32.1* | 3.42 | 3.13* | 4.36 | 3.83* | 1.06 | 0.98* | 0.289 |
| 2020³ | 23.6 | 22.9* | 31.1 | 32.8* | 3.28 | 2.97* | 4.21 | 3.62* | 1.04 | 0.93* | 0.284 |
| 2020³⁴ | 23.1 | 22.9* | 31.5 | 32.8* | 3.30 | 2.97* | 4.07 | 3.62* | 1.00 | 0.93* | 0.277 |
| 2021 | 24.4 | 23.8* | 30.6 | 32.2* | 3.41 | 3.00* | 4.45 | 3.77* | 1.09 | 0.99* | 0.294 |
| 2022 | 24.4 | 23.6* | 30.6 | 32.0* | 3.38 | 3.11* | 4.40 | 3.85* | 1.09 | 1.00* | 0.294 |
| 2023 | 24.5 | 23.6* | 30.3 | 31.6* | 3.49 | 3.22* | 4.53 | 3.95* | 1.11 | 1.01* | 0.297 |
| 2024 | 24.9 | 23.8* | 30.1 | 31.5* | 3.48 | 3.20* | 4.62 | 3.94* | 1.14 | 1.02* | 0.302 |

**How to read it**
- **Levels are close.**
  - The top 10% holds 23–26% in both sources every year, and the bottom 50% holds 30–33%.
  - Since 2010, WID is slightly *less* unequal than ERFS: bottom 50% 1–2 points higher, S80/S20 about 3.9 against 4.4.
  - This is not a contradiction, but we have not decomposed it. The unit differs (equal-split adults vs persons weighted by UC), and WID's post-tax income contains items ERFS lacks (imputed rents, undistributed profits, indirect taxes deducted). In-kind transfers are not neutral here: health, attributed close to lump-sum in WID, raises the bottom's share, while education and collective spending, proportional to income in WID, are neutral.
- **The trends differ.**
  - From 1996 to 2019, ERFS's top 10% share rises from 22.5% to 23.9%, after peaking at 25.4% in 2011. WID's falls from 25.7% to 23.5% (23.8% in 2018, its last observed year).
  - The ERFS rise crosses the 2010 and 2012 breaks. Each break improved the imputation of financial income, which lifts the top, so part of the rise is method.
  - WID's post-tax fall after 2008 follows its own pre-tax top 10% share, which fell from 35.2% (2008) to 32.9% (2012). It plausibly also reflects the 2012–2013 tax changes, but we have not decomposed it.
  - Since 2012² the gap is small and both series are roughly flat: ERFS 25.0 → 24.8 (2018) → 23.9 (2019), WID 23.3 → 23.8 (2018) → 23.5 (2019, extrapolated).
- **WID's P90/P10 has fallen from 3.7 to 3.1–3.2; ERFS's D9/D1 stays at 3.3–3.5.** WID ranks adults, ERFS ranks persons by household niveau de vie, and the income concepts differ. We have not separated the unit effect from the concept effect.
- **2020 needs care on both sides.**
  - ERFS 2020 is flagged as fragile and starts a new chain.
  - WID's 2019–2024 are extrapolations; in 2020 mean income per adult falls 8.5%. ERFS shows niveau de vie *rising*, because cash support is in disposable income.
  - Do not compare 2020-based growth rates.

**Growth per year, ERFS vs WID post-tax income** (ERFS: constant euros, CPI; WID: constant 2025 €, national income deflator)
- **1996 → 2018** (WID's last observed year; crosses the 2010 and 2012 ERFS breaks). Ending in 2019 (WID extrapolated) gives almost the same numbers: ERFS +0.87 / +0.89 / +0.76 / +0.91%, WID +1.52 / +1.16 / +0.73 / +0.98%.

  | | ERFS | WID |
  |---|---|---|
  | Bottom (D1 / P10) | +0.78% | +1.50% |
  | Middle (median) | +0.81% | +1.15% |
  | Top (D9 / P90) | +0.75% | +0.72% |
  | Mean | +0.91% | +0.99% |

  - The average growth rates agree.
  - WID's P10 grows faster than its median and P90. ERFS shows almost uniform growth across the distribution.
- **2012² → 2018** (no ERFS break; WID observed). To 2019 instead: ERFS +0.64 / +0.66 / +0.17 / +0.31%, WID +1.18 / +0.67 / +0.40 / +0.68%.

  | | ERFS | WID |
  |---|---|---|
  | Bottom (D1 / P10) | +0.27% | +1.02% |
  | Middle (median) | +0.33% | +0.54% |
  | Top (D9 / P90) | +0.03% | +0.32% |
  | Mean | +0.18% | +0.65% |

  Same shape (the top grows least), but WID grows faster. In-kind transfers and collective spending are in WID and not in ERFS, and the deflators differ.
- **2020³⁴ → 2024:**
  - ERFS: D1 −0.30%, median +0.55%, D9 +1.03% a year.
  - WID: +1.1% to +3.0% a year, but from its 2020 dip and wholly extrapolated. Not informative.

**Before redistribution: ERFS IG5 vs WID pre-tax income (`ptinc`)**

| Ratio | ERFS IG5 | WID `ptinc` |
|---|---|---|
| D9/D1 (P90/P10 for WID) | 5.2–6.3 | 12.9–13.9 |
| D9/D5 (P90/P50 for WID) | 2.03–2.15 | 2.21–2.35 |

- Both treat pensions as primary income, and the upper half agrees well.
- The bottom does not:
  - WID's P10 is an adult with very little pre-tax income: students, inactive adults, adult children living with their parents.
  - ERFS pools income within the household and divides by UC, which lifts these people to their household's level.
- This is a *unit* difference, not an error on either side.

## 5. Revenu élargi (CND) vs WID

All CND shares below are **derived** by us; the pseudo-Gini, Palma and S80/S20 are published by INSEE.
- **2022 and 2023:** shares are group masses (€ bn) divided by the published total.
- **2019:** IA88 gives euros per UC by twentieth. The number of UC in each twentieth is recovered as net transfers (€ bn) / net transfers (€ per UC). These counts sum to 46.51 million UC, against 46.51 million implied by the published total (1,758.4 bn / 37,810 € per UC).

WID columns rank adults by the measure itself. Pensions are in WID's `ptinc` but outside CND's "before transfers". WID 2019 is already an extrapolation, so WID 2018 (last observed year) is shown too.

| 2019 | Top 10% | Top 5% | Bottom 50% | Palma | S80/S20 | (pseudo-)Gini |
|---|---|---|---|---|---|---|
| CND primary income, extended to national income (product taxes allocated by consumption) | 31.8 | 22.2 | 24.0 | 1.9 | 8.1 | 0.403 |
| CND before transfers, basic prices (no pensions) | 34.2 | 24.1 | 21.6 | 2.4 | 10.9 | 0.441 |
| WID `ptinc` 2019\* (pensions included) | 34.1 | – | 20.5 | 2.56 | 16.4 | – |
| WID `ptinc` 2018 (observed) | 34.3 | – | 20.3 | 2.59 | 16.5 | – |
| CND after transfers (niveau de vie élargi) | 21.0 | 13.8 | 38.3 | 0.7 | 2.4 | 0.188 |
| CND household disposable income (incl. undistributed profits) | 26.1 | 17.6 | 30.6 | 1.2 | 4.6 | 0.295 |
| WID `diinc` 2019\* | 23.5 | – | 32.1 | 0.98 | 3.83 | – |
| WID `diinc` 2018 (observed) | 23.8 | – | 31.9 | 1.00 | 3.91 | – |

| CND, later vintages (derived from € bn) | Top 10% before | Bottom 50% before | Top 10% after | Bottom 50% after |
|---|---|---|---|---|
| 2022 (IP2022, base 2020) | 34.0 | 20.6 | 21.7 | 37.0 |
| 2023 (IA118, new conventions) | 34.5 | 20.7 | 20.6 | 38.2 |
| WID 2022 / 2023 (`ptinc` / `diinc`, extrapolated) | 34.4 / 34.0 | 20.3 / 20.3 | 23.6 / 23.6 | 32.0 / 31.6 |

IA118 publishes for 2023 a pseudo-Gini of 0.451 before transfers and 0.188 after, Palma 2.4 → 0.7 and S80/S20 11.7 → 2.5.

**How to read it**
- **Before transfers, the two sources agree almost exactly on the top 10%** (34%) **and the bottom 50%** (21%), although they treat pensions in opposite ways and do not rank the same people.
  - Where the two differ is the extreme bottom: WID's S80/S20 is 16 against CND's 11. As with ERFS, this is the per-adult unit with no pooling.
- **After transfers, the CND is far more equal than WID's post-tax income:** top 10% 21% against 23.5%, bottom 50% 38% against 32%, Palma 0.7 against 1.0. Possible reasons, not separated here and not ranked:
  - **No re-ranking in the CND.** Persons are ranked by usual niveau de vie. Someone with a high extended income but an ordinary usual niveau de vie stays in a middle group, which mechanically lowers the top share and raises the bottom's.
  - **Allocation of education and collective spending.** INSEE attributes education by use and collective spending near-flat per UC; WID attributes both in proportion to disposable income. Health is close to lump-sum in both, though by different profiles. These items are about 30% of national income in the CND (€610 bn of €2,026 bn in 2019).
  - **Unit.** UC-weighted persons, against equal-split adults.
- **What this cross-check is consistent with:**
  - WID's *pre-tax* split (top 10% and bottom 50%). The match could partly be offsetting effects, since pensions are treated in opposite ways and the ranking differs.
  - WID's national-income totals.
- **What it does not test:**
  - The level of inequality in WID's post-tax income. That level depends on an allocation convention the two producers resolve differently.

## 6. Wealth: HVP vs WID net personal wealth (`hweal`)

WID: net wealth, adults, equal split. HVP: gross wealth, households. Years after 2014 in WID are extrapolations (\*).

| Year | HVP gross, top 10% | HVP gross, top 1% | HVP gross, bottom 50% (derived 1 − top 50%) | HVP Gini (gross) | WID net, top 10% | WID net, top 1% | WID net, bottom 50% |
|---|---|---|---|---|---|---|---|
| 2015 | 48 | 16 | 8 | 0.645 | 58.9* | 26.1* | 5.0* |
| 2018 | 46 | 15 | 8 | 0.638 | 59.2* | 26.4* | 4.9* |
| 2021 | 47 | 15 | 8 | 0.645 | 59.7* | 27.2* | 4.9* |
| 2024 | 48 | 15 | 7 | 0.652 | 59.9* | 27.7* | 4.8* |

The long series reaches back to WID's observed years. Shares of gross wealth hors reste are **derived** as 0.1 × the mean of a tenth (or 0.01 × the mean of the top 1%) divided by the overall mean:

| HVP wave (field, method) | Top 10% | Top 1% | Bottom 50% | Gini (hors reste) | WID net, top 10% | WID net, top 1% | WID net, bottom 50% |
|---|---|---|---|---|---|---|---|
| 1998 (metropolitan France, old method) | 46.2 | – | 7.7 | 0.639 | 59.5 | 28.1 | 5.9 |
| 2004 (metropolitan France, old method) | 45.8 | – | 7.2 | 0.640 | 56.7 | 25.1 | 6.0 |
| 2010 (metropolitan France, old method) | 46.9 | – | 6.7 | 0.651 | 58.3 | 24.6 | 4.7 |
| 2010 (France excl. Mayotte, new method) | 48.2 | 16.0 | 6.2 | 0.661 | 58.3 | 24.6 | 4.7 |
| 2015 (France excl. Mayotte) | 49.1 | 16.2 | 6.7 | 0.663 | 58.9* | 26.1* | 5.0* |
| 2018 (France excl. Mayotte) | 47.4 | 15.2 | 6.8 | 0.654 | 59.2* | 26.4* | 4.9* |
| 2021 (France excl. Mayotte) | 48.5 | 16.1 | 6.4 | 0.663 | 59.7* | 27.2* | 4.9* |

**Net wealth, 2021, bounds** (derived from `hvp_net_by_gross_2021`, households ranked by gross wealth):
- Their net-wealth shares are: top 10% 48.7%, top 1% 16.6%, bottom 50% 7.2%.
- Ranking by gross rather than net wealth can only lower a top group's share and raise a bottom group's share. So the true HVP top 10% share of net wealth is **at least 48.7%**, and the true bottom 50% share is **at most 7.2%**.
- INSEE publishes no exact net-wealth shares.
- The net-wealth thresholds INSEE does publish (IF371) give D9/median of 4.8–5.1 in 2015–2024. WID's net P90/P50 is 5.3.

**How to read it**
- **The top is much smaller in HVP.**
  - The top 10% holds about 48% in HVP against about 59% in WID.
  - The top 1% holds about 15–16% in HVP against 26–28% in WID, roughly 11 points less.
  - The gap is concentrated in the top 1%, as expected: a survey, even with oversampling, misses most very large fortunes. WID takes the top from income-tax capital income and, since the 2025 vintage, lifts the top to the Forbes total (see [rich-lists.md](rich-lists.md)).
  - Gross vs net works the other way: debt is a larger share of wealth in the middle, so net shares are more concentrated than gross shares (2021 bound above: 48.7% net vs 47% gross). So the concept gap does not explain HVP's lower top share.
  - HVP is also not rescaled to national-accounts totals. Business and financial assets, both concentrated at the top, are the components surveys typically under-report.
- **Unit.**
  - Households versus equal-split adults. A household is a couple or a single person, often with children, and households are ranked by total wealth. This lifts couples' households relative to singles.
  - Equal splitting assigns each adult half of a couple's wealth, and every adult, including young adults living alone with almost nothing, counts as a unit.
  - We have not quantified the unit effect. Most of the 11-point gap at the top 1% is more plausibly coverage of large fortunes than unit.
- **Trends are flat in both sources.**
  - Over 1998–2010, HVP hors reste goes 46.2 → 46.9 (old method) and WID 59.5 → 58.3.
  - Over 2010–2021, HVP goes 48.2 → 48.5 and WID 58.3 → 59.7.
  - HVP has no clear rise in the top 1% (16.0 → 16.1), while WID's top 1% rises from 24.6 to 27.2. WID's rise after 2014 is an extrapolation with a fixed asset mix plus the Forbes calibration, which HVP cannot see.
- **The bottom half agrees roughly.**
  - HVP's bottom 50% gross share is 6–8%; the true net share is at most 7.2% in 2021. WID's net share is 4.7–6.0%.
  - Debt and the per-adult unit both push WID's figure lower.

## 7. What is not here, and why

- **Net-wealth top shares from INSEE.** They are not published. Only the bounds above are possible. The ECB/Banque de France Distributional Wealth Accounts, which are calibrated to national accounts with a rich-list tail, are the right source for net shares; see [dwa.md](dwa.md).
- **ERFS top 1%.** INSEE publishes no shares or thresholds above P95 for niveau de vie in these tables. The 1996–2024 deciles stop at P95.
- **Insee Première "Niveau de vie et pauvreté en 2024", retropolated 1996–2019 series.** Not downloaded. INSEE says it differs from the series used here before 2020.
- **The 1970–2023 constant-field series** ([8731699](https://www.insee.fr/fr/statistiques/8731699)). Not used. Its income field is narrower (no financial income, no disability allowance) and INSEE says it differs from the 1996–2023 data.
- **Patrimoine waves 1986 and 1992.** Not in the long-series file.
- **CND 2018.** Published only in Accardo et al. (2021) / Insee Méthodes 138. Not downloaded here.
- **Broken download.** `donnees_ia88.xlsx` on the IA88 page returns an HTML page, not a spreadsheet, so it is not used.
- **Filenames that will change.** The `irsocerfs2023_*` files are the 2023 vintage. When INSEE publishes the next ERFS long series, the filenames will change and `fetch()` will report them as failed. Update `FILES`.
- **Collective-spending allocation in the current WID vintage.** Checked against the DINA Guidelines (Oct. 2025, p. 70), Bozio et al. (2024) and this vintage's metadata (Fisher-Post & Gethin 2023; education proportional). The health profile used for France in this vintage is not stated in the metadata.
