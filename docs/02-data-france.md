# 2. Data available for France

What exists, what each source can and cannot say, and whether this project
uses it. "Used" means it feeds the published numbers; "cross-check" means it
is planned as a validation layer; "context" means it informs the method only.

## 2.1 Summary

| Source | Producer | Concept | Unit | Years | Top coverage | Status |
|---|---|---|---|---|---|---|
| WID.world France (DINA) | World Inequality Lab | Pre-tax income, post-tax national income, net wealth, wealth composition | adult 20+, equal split | income 1820–2024 (post-tax 1980–2024), wealth 1800–2024 | 127 fractiles down to top 0.001% | **Used** (backbone) |
| Indices des prix des logements anciens (Paris flats, provincial flats) | INSEE / Notaires | House price indices, base 2015 | region | 1992/1995–2025 | n/a | **Used** (carry the 2025 DVF level back in time) |
| Statistiques DVF | Etalab (DGFiP data) | Mean and median price per m² by département | département | last 5 years | n/a | **Used** (2025 price level, Licence Ouverte) |
| ECB MFI interest rates | ECB | Mortgage rate, new loans for house purchase, France | country | 2000– (monthly) | n/a | **Used** (repayment burden) |
| Challenges "500 fortunes", Forbes billionaires | Press | Professional / total wealth of the richest families | family / person | published euro totals 2004–2026; Forbes counts 2017–2025 | top ~500 families | **Used** (top-tail check and scenarios), see [notes/rich-lists.md](notes/rich-lists.md) |
| ERFS (Enquête Revenus fiscaux et sociaux) | INSEE | Disposable income per consumption unit (*niveau de vie*), poverty, Gini | person, consumption units | 1975–2024 (breaks 2010, 2012, 2020) | nothing above P95 | **Used** (cross-check, `pipeline/sources/insee.py`) |
| Revenu élargi / comptes nationaux distribués | INSEE | Income including all public services, 100% of national income | household, consumption units | 2019, 2022, 2023 | by twentieth / decile | **Used** (cross-check, 2019) |
| Histoire de vie et Patrimoine | INSEE | Household wealth survey, asset detail | household | 1998–2024 waves | misses the largest fortunes | **Used** (cross-check, gross wealth) |
| Distributional Wealth Accounts | ECB / Banque de France | Net wealth by decile, top 5%, bottom 50%, consistent with financial accounts | household | 2009–2025 (quarterly, Q4 used) | top 5% at best | **Used** (cross-check, `pipeline/sources/dwa.py`) |
| IPP studies of top incomes | Institut des politiques publiques | Taxable vs comprehensive income (incl. retained profits of controlled firms) of top groups | tax household | 2016 | down to the 75 richest households | **Used** (comparison table, `data/manual/ipp_top_income.csv`) |
| Filosofi | INSEE | Disposable income from tax + benefit files | household, local areas | 2012– | local detail, not the extreme top | Context (geography) |
| Impôt sur le revenu tabulations; ISF then IFI | DGFiP | Fiscal income by bracket; taxable wealth | tax household | long series | quasi-exhaustive, but fiscal income misses retained profits | Context (already inside WID) |
| IPC; IPC by household category | INSEE | Consumer prices, incl. by income quintile | n/a | long series | n/a | Plan (alternative deflator) |
| Comparaison spatiale des prix | INSEE | Price levels by territory | n/a | 2015, 2022 | n/a | Context |
| DVF (Demandes de valeurs foncières) | DGFiP / Etalab | Every property sale with price | transaction | 2014– | n/a | Plan (housing price levels) |
| Comptes de la santé; Compte de l'éducation | DREES; DEPP | Health and education spending, out-of-pocket share | aggregate | annual | n/a | Context (already inside post-tax income) |
| OpenFisca-France, Ines, TAXIPP | open source / DREES-INSEE / IPP | Tax-benefit microsimulation | household | legislation by year | n/a | Plan (simulating a given household) |

## 2.2 Why WID.world is the backbone

1. **It already does the hard parts you asked for.** "Post-tax national income"
   (`diinc`) is income after all taxes, cash benefits, in-kind transfers
   (health, education) and collective public spending, consistent with
   national accounts. In this vintage the French post-tax series come from
   Fisher-Post & Gethin [FPG2023] (method: [BGGGP2024; DINA-G]); 2019–2024
   apply the 2019 pre-tax/post-tax ratio by percentile.
2. **It goes down to the top 0.001%**, with 127 fractiles (P0–P1, …, P98–P99,
   then tenths, hundredths and thousandths of a percent inside the top 1%).
   No survey can do this.
3. **Long**: a consistent framework from 1900 to 2024 in constant euros,
   stitched from several methods (estate records before 1970, tax data
   1970–2014, extrapolation after 2014, Forbes calibration of the very top
   from 1988). The breaks are listed in [03-method.md §3.11](03-method.md#311-quality-flags-and-method-breaks)
   and shaded on the page.
4. **Open and reproducible**: bulk download, codes dictionary, published
   methodology and code.

### What WID does not do (and how we handle it)

| Limit | Consequence | Handling |
|---|---|---|
| Unit is per adult, equal split, no equivalence scale | Not directly comparable with INSEE *niveau de vie* | Stated on every chart; INSEE cross-check planned |
| Deflator is the national-income price index, not the CPI | Purchasing power of a given basket may differ, especially for the bottom | Documented; CPI-by-quintile variant in the plan |
| Recent years are extrapolated (data quality flags) | Wealth 2015–2024 (asset mix held at 2014, top lifted to Forbes) and income 2019–2024 are extrapolations | Grey band on the page, per measure; read from the flags at build time |
| Top 0.001% is a model estimate; nothing below it | The billionaires are inside one bin of ~530 adults | Since the 2025 update WID tops this bin up to at least the Forbes total (technical note 2025/01, cited in the France metadata of the vintage we use); we also compare it with Challenges and Forbes on the page |
| Post-tax income ranking is by post-tax income | Fractiles are not the same people across concepts | Stated in the method |
| No regional price adjustment | A Paris household looks richer than its purchasing power | Documented limit |

## 2.3 Files used in this version

Downloaded by `pipeline/fetch.py` into `data/raw/` (not redistributed):

| Folder / file | Origin | Module |
|---|---|---|
| `WID_data_FR.csv`, `WID_metadata_FR.csv`, `wid_vintage.json` | <https://wid.world/bulk_download/wid_all_data.zip> (HTTP range requests, ~10 MB; ETag recorded) | `pipeline/fetch.py` |
| `dwa/` | ECB Data Portal, dataflow DWA, France | `pipeline/sources/dwa.py` |
| `insee/` | INSEE income survey (ERFS), wealth survey, distributed national accounts (xlsx) | `pipeline/sources/insee.py` |
| `prices/` | INSEE BDM consumer price indices (all, by decile), national accounts table 2.103, Insee Première 1815 and 1959 | `pipeline/sources/prices.py` |
| `housing/` | INSEE BDM house price indices (Paris, Île-de-France, province), Etalab Statistiques DVF (département rows) | `pipeline/sources/housing.py` |
| `rates/` | ECB MFI interest rates, loans for house purchase, France | `pipeline/sources/rates.py` |

Compiled by hand in `data/manual/`, one source per row:

| File | Content |
|---|---|
| `challenges_500.csv`, `forbes_france_billionaires.csv` | Rich-list totals quoted in published articles, with the exact quote (see [notes/rich-lists-sources.md](notes/rich-lists-sources.md)) |
| `ipp_top_income.csv` | 21 figures quoted from IPP Note 92 and Bach et al. (2025) |
| `top_wealth_estimates.csv` | Other published estimates of top wealth (Garbinti et al. 2016 table 1, DGFiP, Assemblée nationale) |
| `ggp_richlist_comparison.csv` | Parameters of Garbinti et al.'s rich-list comparison (appendix H) |
| `precommitted_spending_surveys.csv`, `insee_spatial_price_gap.csv` | Survey figures on pre-committed spending; INSEE spatial price gaps |

### WID variables used

| Code | Meaning |
|---|---|
| `aptincj992`, `sptincj992`, `tptincj992` | Pre-tax national income: average, share, threshold |
| `adiincj992`, `sdiincj992`, `tdiincj992` | Post-tax national income: average, share, threshold |
| `ahwealj992`, `shwealj992`, `thwealj992` | Net personal wealth: average, share, threshold |
| `ahwhouj992`, `ahwbusj992`, `ahwfinj992`, `ahwdebj992` | Housing, business, financial assets, debt (1970–2014) |
| `npopuli992` | Adult population (20+) |
| `inyixxi999` | National income price index (= 1 in the price base year) |

Suffix `j992` = equal-split adults aged 20+. In WID's naming, `cainc` is
post-tax *disposable* (cash) income and `diinc` is post-tax *national* income;
for France the cash series currently stops in 1979, so it is not used.
