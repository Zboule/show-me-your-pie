# Prices, pre-committed spending and housing levels

Purpose: measure purchasing power layer by layer more accurately than with one national
deflator, and turn the housing affordability index (method §3.8) into price levels
("years of income for a 70 m² flat"). Code: `pipeline/sources/prices.py` and
`pipeline/sources/housing.py` (standard library only, `python3 -I <module> data/raw`).
Hand-compiled inputs: `data/manual/precommitted_spending_surveys.csv`,
`data/manual/insee_spatial_price_gap.csv`.
Last checked 2026-10-16. Every number below was recomputed from the downloaded files.

## 1. What we have

### 1.1 Consumer prices by household category (INSEE BDM, annual)

| Key in `prices.load()` | idbank(s) | Coverage | What it is |
|---|---|---|---|
| `cpi_all` | 011814639 (base 2025), 001764363 (base 2015) | France, 1990–2025, 2025 = 1 | All-household CPI, annual average. The two bases agree within 0.3% where they overlap. |
| `cpi_all_incl_imputed_rents` | 011814653, 001765177 | France, 1990–2025 | Same, including owner-occupiers' imputed rents (closer to a national-accounts deflator). |
| `cpi_long` | 011813530 | France, 1901–2025 | INSEE euro/franc purchasing-power coefficient. Two decimals on a 2025 = 100 scale, so it is coarse before about 1950. |
| `cpi_decile_<g>` (10 series) | 010054292–010054301 (base 2015), checked against 011818277–011818286 (base 2025) | Metropolitan France, 1998–2025 | CPI by decile of *niveau de vie*. Rebased to 2025 = 1; over 2010–2025 the two bases differ by at most 0.013% (all ten deciles). |
| `cpi_q1_excl_tobacco_b2015` / `_b2025` | 001766925 / 011818265 | France, 1998– / 2015– | First quintile of niveau de vie, **excluding tobacco**. |
| `cpi_tenant_b2015`, `cpi_owner_b2015`, `cpi_owner_with_mortgage_b2015`, `cpi_retired_b2015` | 010054310, 010054308, 010054309, 010054291 | Metropolitan France, 1998–2025 | By housing tenure and for retired households. |
| `cpi_urban_workers_b2025` | 011814655 | France, 1996– | Urban households whose reference person is a blue- or white-collar worker (the historical "ménages urbains" index). |

INSEE does **not** publish a CPI by quintile, apart from the first quintile excluding tobacco.
It does publish one by **decile**, which is better. All decile indices use the same prices with
decile-specific weights. Base-2015 series are
"séries arrêtées" but run to 2025.

### 1.2 Pre-committed ("pré-engagées") spending

**National accounts, macro** (`precommitted_share_of_rdb` and related keys; INSEE comptes
nationaux annuels base 2020, table 2.103, 1959–2025, file `t_2103_fr.xlsx` of the May 2026
edition, page https://www.insee.fr/fr/statistiques/8988851). INSEE's definition (c1358):
housing **including imputed rents**, water, energy, telecoms, TV, school canteens, insurance
(excluding life insurance) and financial services including FISIM. **Mortgage repayments are not
included.** The base-2014 series (BDM 010562201 and 010562212, 1 − RDB arbitrable / RDB,
1959–2021) is kept as `precommitted_share_of_rdb_b2014`. It runs about 1–1.5 points below
base 2020.

| Year | 1960 | 1970 | 1980 | 1990 | 1996 | 2000 | 2010 | 2017 | 2020 | 2022 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Pre-committed, % of household gross disposable income | 13.5 | 19.4 | 22.6 | 27.1 | 28.5 | 28.1 | 29.9 | 30.6 | 29.9 | 29.5 | 30.1 | 30.3 |
| of which housing-related | 10.7 | 15.5 | 16.8 | 19.1 | 22.0 | 21.4 | 23.1 | 24.4 | 24.1 | 23.5 | 22.7 | 23.1 |

**By income group.** These sources use different denominators. Never mix rows across them.

| Source | Year | Groups | Denominator | Values |
|---|---|---|---|---|
| INSEE Première 1815, Fig. 7 (`ip1815_consumption_structure_2017`, downloaded xlsx) | 2017 | Quintiles of RDB per consumption unit (national accounts distributed) | % of consumption **excluding imputed rents** | Q1 31.5, Q2 29.1, Q3 24.9, Q4 21.9, Q5 19.0, all 23.8 |
| DREES ER 1055, Table 1 (manual CSV) | 2011 (Budget de famille) | Poor / modest non-poor / middle / affluent | % of **disposable income**, incl. mortgage repayments | 61 / 39 / 31 / 23; all 30 |
| France Stratégie NA 102, p.1 chart (manual CSV) | 2001, 2006, 2011, 2017 | Same four groups | % of **total expenditure** (incl. loan repayments) | Poor 31 → 33 → 38 → 41; modest 30 → 31 → 35 → 37; middle 28 → 29 → 30 → 32; affluent 25 → 24 → 26 → 28; all 27 → 28 → 30 → 32 |
| France Stratégie NA 102, text | 2017 | Poor | % of disposable income | 60 |
| France Stratégie NA 102, Tables 2–3 (manual CSV) | 2017 | Deciles D1–D9 | EUR per consumption unit per month | Niveau de vie thresholds 925 … 3,005 vs arbitrable-income thresholds 377 … 2,338 (D9/D1: 3.25 vs 6.20) |

The four groups are: poor = below 60% of median niveau de vie (13.5% of households in 2017);
modest non-poor = from the poverty line to D4 (26.5%); middle = D4 to Q3 (35%);
affluent = above Q3 (25%). IP1815 also gives RDB per consumption unit and consumption per
consumption unit by quintile (`ip1815_rdb_consumption_per_uc_2017`) and savings rates for
2011–2017. The 2011 edition of the same INSEE decomposition
(https://www.insee.fr/fr/statistiques/3148891) exists only as `.xls` and was not parsed.

### 1.3 Housing price levels and indices

| Key in `housing.load()` | Source | Coverage | Notes |
|---|---|---|---|
| `dvf_<group>_<type>_mean_eur_m2` | Etalab "Statistiques DVF", monthly by département | 2021–2025 | Exact sales-weighted annual mean. Groups: `paris`, `idf`, `rest_metro`, `metro`, `dvf_all`. Types: `apartments`, `houses`, `all`. |
| `dvf_<group>_<type>_median_approx_eur_m2` | same | 2021–2025 | **Approximate**: weighted average of monthly département medians. |
| `hpi_*` (13 series) | INSEE BDM, 010567012, 010567056/58/59/60, 010567062/72/74 (Province), 010567076/78/88/90 (Île-de-France), 010567118 | 1992/1995/1996–2025 | Notaires-INSEE indices, raw (brute) series, 2015 = 100, annual mean of 4 quarters. |
| `backcast_rest_metro_{apartments,houses,all}_eur_m2`, `backcast_metro_all`, `backcast_idf_all`, `backcast_paris_apartments` | DVF 2025 mean × INSEE index(y) / index(2025) | 1995/1996–2025 | Level of the 2025 mix of dwellings sold, carried back at constant quality. Not an observed average. |
| `spatial_price_gap_2022` (prices module) | INSEE Première 1959, xlsx | 2022 | Paris urban unit vs province excluding Corsica: Fisher +7.2%, excluding rents +5.0%, rents +39.6%. On the province basket +8.2%, on the Paris basket +6.2%. |
| `spatial_price_gap_2015` (manual CSV) | INSEE Première 1590, Fig. 1 | 2015 | Fisher +8.8%, excluding rents +6.2%, rents +48.9%. On the province basket +9.2%. |

Levels in current euros per m² (flats):

| | 1996 | 2000 | 2005 | 2010 | 2015 | 2020 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|
| Paris (DVF 2025 × INSEE Paris flats index) | 2,528 | 3,002 | 5,217 | 7,183 | 8,330 | 11,180 | 9,933 | 10,033 |
| Metropolitan France outside Île-de-France (back-cast) | 1,047 | 1,161 | 2,168 | 2,559 | 2,480 | 2,876 | 3,250 | 3,288 |

DVF observed means for flats, 2021 → 2025: Paris 10,880 → 10,033; Île-de-France 6,449 → 6,432;
metropolitan France outside Île-de-France 3,072 → 3,288. The DVF figure includes off-plan sales
(VEFA) and the year's actual mix of flats; quality-constant levels such as the Notaires-INSEE
ones are lower. An earlier version compared the two using a Notaires table that is not openly
licensed; that table and comparison were removed.

## 2. What is missing

- **No CPI by quintile** (only Q1, excluding tobacco). Deciles start in **1998**. Before that,
  only the all-household CPI (1990 at annual level from BDM, 1901 via the coefficient) and the
  "ménages urbains ouvriers ou employés" index (1996 here; older bases exist in the IPC-1990
  dataflow, not fetched).
- **No yearly pre-committed series by income group.** There are survey points only (2001, 2006,
  2011, 2017; Budget de famille is about every 5–6 years) and one national-accounts
  distribution (2017, quintiles, as a share of consumption, not of income). The 2017 Budget de
  famille shares by **quintile** of disposable income were not found as published numbers;
  France Stratégie gives them only as charts by four groups. The DREES Dossier n°25 (full
  report behind ER 1055) could not be downloaded: the DREES site resets connections and the
  Wayback copy is truncated.
- **No official yearly price level for the rest of France before 2021.** The Notaires de France
  publish province medians only in press notes (city-level, varying coverage). We use DVF 2025
  × INSEE Province index instead. Official DVF aggregates cover only the last 5 years, and
  Alsace-Moselle never.
- **Spatial price levels** exist only for 2015 and 2022 (and the urban unit of Paris, not
  Île-de-France). There is no regional CPI *level* series.

## 3. How to use these series

### (i) Deflate each layer's income with its own price index

```
real_L(y) = nominal_L(y) / P_L(y)        P_L = CPI of the decile(s) mapped to layer L, 2025 = 1
```

WID gives average post-tax income per adult in constant 2025 euros using its national-income
deflator D (`deflator` in `site/data/france.json`). The layer-specific re-deflation is
`avg_L(y) × D(y) / P_L(y)`.

A suggested mapping, which is an assumption: bottom 50% ← mean of deciles 1–5; middle 40% ←
deciles 6–9; top 10% and above ← decile 10 (`gt_d9`). INSEE has nothing finer than the top
decile, so the four top layers share one index.

**Effect size: small.** Over 1998–2024 the index rose 55.5% for households below D1 and 50.8%
for those above D9. That is 3.1% cumulative, about 0.12 point a year. Over 2015–2024 the ten deciles
are within about 1% of each other (+19.2% to +20.5%). Prices barely change who gained. Pre-committed spending
and housing (below) matter much more.

### (ii) Income left after pre-committed spending, per layer

```
arbitrable_L(y) = income_L(y) × (1 − s_L(y))
s_L(y) = s_g(survey year) × s_macro(y) / s_macro(survey year)      # assumption: group shares move with the macro share
```

`s_g` is a survey share for the group(s) mapped to layer L. Use **only** shares of disposable
income: DREES 2011, or France Stratégie's 60% for the poor in 2017. Shares of total spending
(France Stratégie) or of consumption excluding imputed rents (IP1815) need a conversion we do
not have. `s_macro` is `precommitted_share_of_rdb`.

Points to keep in mind:

- **Different definitions.** The survey definition includes mortgage repayments (capital is
  saving, not consumption) and excludes imputed rents. The national-accounts definition does
  the reverse. Owner-occupiers' imputed rent is income in both WID and the national accounts,
  so the macro concept is the consistent one to subtract from WID income. The survey one is
  closer to how households feel it.
- **Lower bound at the bottom.** WID post-tax income at the bottom is larger than survey
  disposable income (in-kind transfers, imputed rents). Multiplying it by a survey share
  overstates pre-committed euros, so `arbitrable_L` is a lower bound for the bottom layers.
- **Too coarse for the top.** The richest survey group (affluent, top 25%) contains WID's whole
  top 10%. A flat 23% for the top 1% overstates their pre-committed share; housing spending
  grows far less than income at the top. Use it as an upper bound.

### (iii) Housing affordability: years of income and repayment burden

Version 0.3 of the page (after review) uses **cash disposable income** rather
than WID income, and adds the cost of borrowing. The full method is in
[03-method.md §3.9](../03-method.md#39-housing-and-fixed-costs); in short:

```
income_g(y)   = ERFS mean niveau de vie of tenths in group g, nominal euros per consumption unit
years_g(y)    = 70 × price_m2(region, y) / income_g(y)
repayment_g(y)= 70 × price_m2 × r(y) / (1 − (1 + r(y))^−25) / income_g(y)
```

with r the ECB's yearly average mortgage rate for France (2000–), and prices
in both regions from the 2025 DVF mean carried back with INSEE's indices
(Paris flats; provincial flats). The Notaires level table used in earlier
versions was removed from the repository because it is not openly licensed.

| Bottom half of persons (tenths 1–5) | 1996 | 2000 | 2023 |
|---|---|---|---|
| Paris, years of income | 18.9 | 20.2 | 41.1 |
| Paris, yearly repayment / income | – | 155% | 236% |
| Outside the Paris region, years of income | 7.8 | 7.8 | 13.0 |
| Outside the Paris region, yearly repayment / income | – | 60% | 75% |

Read: a person living alone with the bottom half's average disposable income
would need 41 years of income to buy 70 m² in Paris in 2023. A couple has 1.5
consumption units, so its figures are a third lower.

The earlier version of this note (23.4 years in 2024) divided by WID
post-tax national income per adult, which includes in-kind services and
imputed rents and is not cash; it is superseded.

Caveats:
- Prices exclude notary fees, the deposit and insurance.
- The level outside the Paris region is a back-cast from the 2025 DVF mean.
  DVF includes off-plan new-build (VEFA) sales and keeps only single-property
  sales, and DVF averages are known to run above quality-constant levels, so the
  rest-of-France level is probably a few percent too high.
- ERFS income has series breaks (2010, 2012, 2020); the newer method is kept
  where a year appears twice.

## 4. CPI vs WID national-income deflator

`cpi_all` (011814639, all households, France) against WID `inyixxi999` (`deflator` in
`site/data/france.json`, 2025 = 1):

| Period | CPI | CPI incl. imputed rents | WID deflator | CPI / WID |
|---|---|---|---|---|
| 1996–2024 | +56.1% (1.60%/yr) | +55.5% (1.59%/yr) | +52.7% (1.52%/yr) | 1.022 |
| 1998–2024 | +53.2% (1.66%/yr) | +52.4% (1.63%/yr) | +50.0% (1.57%/yr) | 1.022 |
| 1996–2019 | +35.8% (1.34%/yr) | +36.7% (1.37%/yr) | +32.7% (1.24%/yr) | 1.024 |
| 2019–2024 | +15.0% (2.83%/yr) | +13.8% (2.61%/yr) | +15.1% (2.85%/yr) | 0.999 |

Index values: CPI 0.6346 (1996), 0.9907 (2024); WID 0.64737 (1996), 0.98839 (2024).
Deflating with the CPI instead of WID's deflator makes 1996–2024 real income growth about
2.2% smaller for every layer: about 0.08 point a year, all of it before 2019.

By decile, 1998–2024 (`cpi_decile_*`): D1 +55.5%, D1–D2 +56.2%, D4–D5 +54.8%, D8–D9 +52.9%,
D10 +50.8%. First quintile excluding tobacco: +50.7%. The low figure comes from excluding
tobacco, whose price index rose 3.4-fold over 2003–2024 (BDM 011814410), so it is not
comparable with the decile series.

## 5. Caveats on mapping to WID layers

- **Units differ.** INSEE ranks households (or people) by disposable income per consumption
  unit (OECD-modified scale, 1 / 0.5 / 0.3). WID ranks adults by their own post-tax national
  income, split equally within couples. The bottom 50% of adults is not the bottom 5 deciles of
  niveau de vie, but the overlap is large. Any mapping is an assumption and should be stated
  next to the chart.
- **Income concepts differ.** WID post-tax national income includes in-kind transfers, imputed
  rents and undistributed profits. Survey disposable income does not. Shares "of disposable
  income" from surveys applied to WID income, which is larger at the bottom, would *overstate*
  the euros of pre-committed spending there.
- **Coverage.** Decile CPIs cover metropolitan France; DVF excludes Alsace-Moselle and Mayotte;
  "région parisienne" in the spatial comparison is the Paris urban unit.
- **Vintages.** `t_2103_fr.xlsx` sits under an edition-specific page id (8988851, May 2026).
  Update `T2103` in `prices.py` when INSEE publishes the next edition. The DVF statistics file is
  a rolling 5-year window: 2021 will drop out at the next refresh, so keep the downloaded file
  if the 2021 anchor matters.

## Sources

- INSEE BDM SDMX: https://bdm.insee.fr/series/sdmx/data/SERIES_BDM/<idbank>
- INSEE, Revenu et pouvoir d'achat des ménages en 2025 (comptes nationaux base 2020), table 2.103: https://www.insee.fr/fr/statistiques/8988851
- INSEE, définition "Dépenses pré-engagées": https://www.insee.fr/fr/metadonnees/definition/c1358
- Accardo J., Billot S., "Plus d'épargne chez les plus aisés, plus de dépenses contraintes chez les plus modestes", Insee Première n°1815, 2020: https://www.insee.fr/fr/statistiques/4764600
- Lelièvre M., Rémila N., "Des inégalités de niveau de vie plus marquées une fois les dépenses pré-engagées prises en compte", DREES Études et Résultats n°1055, 2018: https://drees.solidarites-sante.gouv.fr/sites/default/files/2020-08/er1055-2.pdf
- Cusset P.-Y., Prada-Aranguren A. G., Trannoy A., "Les dépenses pré-engagées : près d'un tiers des dépenses des ménages en 2017", France Stratégie, La Note d'analyse n°102, 2021: https://www.strategie-plan.gouv.fr/publications/depenses-pre-engagees-pres-dun-tiers-depenses-menages-2017
- INSEE Première n°1959, "En 2022, les prix en région parisienne dépassent de 7 % ceux de la province": https://www.insee.fr/fr/statistiques/7649921
- INSEE Première n°1590, "En 2015, les prix en région parisienne dépassent de 9 % ceux de la province": https://www.insee.fr/fr/statistiques/1908158
- Etalab, Statistiques DVF: https://www.data.gouv.fr/fr/datasets/statistiques-dvf/ (processing code: https://github.com/datagouv/datagouvfr_data_pipelines/tree/main/data_processing/dvf)
