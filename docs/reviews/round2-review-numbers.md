# Round-2 independent numbers audit

Auditor: independent re-computation, second round, 2026-10-16.

## Scope

- **Paper.** Every number quoted in `paper/paper.md`, i.e. all 67 keys in `paper/numbers.md` / `paper/numbers.json`, plus the 20 keys added while this audit ran (§2.11).
  - `paper/numbers.*`, `site/data/france.json` and two pipeline files were regenerated at 23:36, during the audit.
  - The page DOM was dumped at 23:19, from the earlier build.
  - Spot checks show identical values in the new `france.json`: IPP block, post-tax shares, corrected scenario years.
- **Page.** Every number that `site/index.html` generates in:
  - the hero;
  - the finding cards;
  - the chapter summaries and tables (`renderHero`, `renderFindings`, `renderPie`, `renderChange`, `renderGIC`, `renderTop`, `renderTopIncome`, `renderCrosscheck`, `renderHousing`);
  - the pure functions in `site/core.js`.
- **Method.** The numeric claims in `docs/03-method.md`, including the §3.7 scenario table.

## How it was done

- **Independent code.** All values were recomputed from `data/raw/` and `data/manual/` with new code written from the method text in `docs/03-method.md`. No pipeline code or `paper_numbers.py` was imported or run.
- **Generated page text.** It was read from the rendered DOM: headless Chrome against a local static server, default view plus `#ptinc`, `#diinc` and `#hweal~ggp_low`.
- **`site/data/france.json`.** It was read only to explain differences, never as an input.
- **Files changed.** None apart from this report.

**Match rule.**
- Page cells: the recomputed value, formatted with a port of the page's own formatters (`eur`, `pct`, `people`; `Intl.NumberFormat` half-away-from-zero rounding), must give the identical string.
- Paper and doc numbers: they must equal the recomputed value rounded to the precision shown.
- "Rounding" marks a last-digit difference whose cause has been identified.

**Scripts**, all run with `python3 -I`:

| Area | Location | Files |
|---|---|---|
| WID core, scenarios, DOM comparison | `<scratch>/audit2/core/` | `wid.py` (loader: asserts no duplicate keys, ports the JS formatters), `layers.py`, `c1_layers.py`, `c2_decomp.py`, `c3_hero.py`, `c4_misc.py`, `c5_scen.py`, `c6_partialbin.py`, `c7_top.py`, `c8_ipp.py`, `c9_dom.py` |
| DOM text extraction | `<scratch>/audit2/` | `domtext.py` |
| Rendered DOM dumps | `<scratch>/audit2/dom/` | – |
| Prices, housing, INSEE, DWA | `<scratch>/audit2/prices/` | `plib.py`, `a1_cpi.py`, `a2_decile_cpi.py`, `a3_housing.py`, `a4_dvf_consistency.py`, `a5_crosscheck.py` |
| Rich-list source check | `<scratch>/audit2/web/` | `scripts/` (`check.py`, `normlib.py`, `ctx.py`), `dl_*/` (raw downloads), `robots/` |

## 0. Summary

**The core arithmetic reproduces.** All of the following match, to the digit or within a last-digit rounding:
- the layers;
- the 1990–2024 decomposition for all three concepts;
- the hero equivalence;
- the four scenarios: every layer share in every year is within 1e-6 of the build;
- the top-tail table and the Challenges ÷ WID ratios;
- the top-bin Pareto check, the IPP ratios, the DWA gaps;
- the housing years, the repayment shares and the decile CPI.

**DOM comparison.** 316 generated cells were compared mechanically: the four change tables, the hero legends and the hero captions. A further 36 rows of the top-tail table were compared the same way.
- Five cells differ, all by one unit in the last digit.
- All five come from `france.json` storing shares at 6 decimals and averages as integers.

**Rich-list sources.** Six spot-checked rows quote their sources word for word (§2.10).

**What is wrong is wording and framing, not arithmetic.** Ranked in §3:
1. The CPI robustness figure is stated three different ways, and none of them is the growth effect. **(M-1)**
2. The paper's start-year sentence is false for two start years and leaves out the later ones. **(M-2)**
3. The rich-list scenarios leave gap years on WID inside their ranges. Under "no non-resident cut" this produces an artificial 2021 dip. **(M-3)**
4. Several smaller precision, citation and wording issues. **(m-1 … m-12)**

**Fixed since round 1:**
- the 1950 CPI step (M-1 in round 1);
- the growth-incidence summary on the bottom half (M-4);
- the 5–7 point DWA wording (M-3a);
- the "1.3–4×" IPP wording;
- the Forbes 2019 and 2005 table cells;
- the k = 1 adult-per-family issue (now 1.8 adults per member).

Still open from round 1: m-13 (CPI wording) and m-15 (HVP concept break).

## 1. WID backbone checks

| Check | Result |
|---|---|
| Duplicate (variable, percentile, year) keys among the variables used | none |
| 127 g-percentiles per concept | 99 + 9 + 9 + 10 for hweal, ptinc and diinc |
| T(y) = Σ g-percentile avg × width × adults, against `mhweali999` | 1990: €4,969.75 bn in both; 2024: €14,657.17 bn in both. The difference is under €0.0001 bn. |
| Layer shares against WID published group shares (differenced where needed), all years and concepts, 2,065 cells | max 0.0000952 (ptinc p99–p99.9, 1988). For codes WID publishes directly, the max is 0.00005. |
| Decomposition identity, growth + share = net, every layer, 3 concepts | exact (< 1e-3 € relative) |
| Σ net = ΔT; Σ share effects = 0 | residuals 2e-12 bn and 8e-13 bn |
| Share-of-growth column sums to 100% | yes, all three concepts |
| 1961 and 1963 wealth share vectors identical (method §3.5) | yes. The g-percentile averages differ only by a constant factor of 0.869. |
| `data_quality` flags (method §3.11) | wealth: 2 to 1969, 4 for 1970–2014, 0 for 2015–2024. Pre-tax: 3 for 1900–1969 (5 in 1970 and 1975), 5 to 2018, 4 for 2019–2024. Post-tax: 5 to 2018, 4 for 2019–2024. Matches. |

## 2. Table of checked numbers

Legend: ✔ match · ≈ last-digit rounding (cause identified) · ✘ mismatch or unsupported.

### 2.1 Paper keys (`paper/numbers.md`) — WID shares and levels

| Key | Claimed | Where | Recomputed | Match |
|---|---|---|---|---|
| wealth_top0001_1900 / _1950 / _1980 / _1990 / _2014 / _2024 | 2.6 / 1.3 / 0.80 / 1.4 / 3.4 / 5.6% | paper Table 2, abstract | 2.6089 / 1.3299 / 0.7990 / 1.4356 / 3.3879 / 5.5772% | ✔ |
| wealth_bottom50_1900 / _1950 / _1980 / _1990 / _2014 / _2024 | 1.6 / 3.2 / 8.4 / 8.9 / 5.0 / 4.8% | paper Table 2, abstract | 1.5703 / 3.1797 / 8.4490 / 8.9397 / 4.9870 / 4.8370% | ✔ (1980: WID's published p0p50 is 0.0845, which shows as "8.5%"; the g-percentile sum is 8.449%) |
| wealth_top1_1900 / _1980 / _2024 | 55.0 / 17.2 / 27.7% | Table 2 | 54.971 / 17.168 / 27.680% | ✔ |
| bottom50_avg_1990 / _2024 | €21,100 / €26,800 | abstract, §5.2 | €21,066 / €26,775 | ✔ |
| wealth_rise_tn | €9.7 tn | abstract, §5.2 | €9,687.4 bn | ✔ |
| captured_top0001 / captured_bottom50 | 7.7% / 2.7% | abstract, §5.2 | 7.702% / 2.732% | ✔ |
| bottom50_net_bn / bottom50_at_start_share_bn | €265 bn / €866 bn | §5.2 | €264.69 bn / €866.02 bn (growth effect €667.30 bn, method §3.5) | ✔ |
| adults_top0001 | 530 | abstract | 529.6 (52,956,956 × 1e-5) | ✔ |
| pretax_bottom50_2024 / posttax_bottom50_2024 | 20.3% / 31.5% | abstract, §5.2 | 20.304% / 31.539% | ✔ (see m-6 on support) |
| pretax_top0001_2024 | 0.88% | §5.1 | 0.8827% | ✔ |
| poorest_equivalent | 51.9% | §5.2 | 51.865%. Cumulative from the poorest, negative bin p0p1 (−€421) included. Excluding it gives 51.861%. | ✔ |
| slices_vs_published_max | 0.00010 | §4, §6 ("below 0.00010") | 0.0000952 | ✔ in paper; ✘ in method §3.4 (m-4) |
| smooth_top0001_raw / _two_year | 5.58% / 5.37% | §6 | 5.577% / 5.367%. The four largest slices move by +0.011, +0.078, +0.072 and +0.032 pt (< 0.1). | ✔ |
| start_fell_bottom50 | "between 1966 and 2009" | §6 | Negative share effect to 2024 from starts 1961, 1963, 1966–2009 and **2011–2023**. Positive from ≤ 1960, 1962, 1964–65 and 2010. | ✘ as worded (M-2) |
| start_fell_middle40 | "between 1971 and 1997" | §6 | Negative from 1971–1997 **and 2002–2023**. Positive from ≤ 1970 and 1998–2001. | ✘ incomplete (M-2) |

### 2.2 Paper keys — very top, scenarios, vintages

| Key | Claimed | Where | Recomputed | Match |
|---|---|---|---|---|
| scenario_dwa_lower | 4.8% | abstract, §5.3, method table | 4.774% | ✔ |
| scenario_ggp_central | 5.6% (no year changed) | §5.3, method | 5.577%; no year changed. Smallest margin is −€227 bn (2023). | ✔ |
| scenario_ggp_low / years | 6.5% / 8 | §5.3, method | 6.454%; 8 years: 2016–2020, 2022–2024 (**2021 not corrected**) | ✔ (range wording: M-3) |
| scenario_no_cut / years | 8.1% / 14 | §5.3, method | 8.067%; 14 years: 2007, 2009, 2010, 2012–14, 2016–20, 2022–24 | ✔ (range wording: M-3) |
| "0.8 points below and 0.9 above" | – | method §3.7 | −0.803 / +0.877 pt | ✔ |
| topbin_threshold_m / topbin_projected_m / topbin_ratio | €799 M / €136 M / 5.9 | §5.3, page note | t(p99.999) = €798.7 M; α(p99.99→p99.998) = 1.900; projected €136.1 M; ratio 5.87 | ✔ |
| 1980 top-bin jump | €50 M vs €35 M | method §3.7 | €50.4 M vs €34.8 M | ✔ |
| "would require alpha below 1" | – | method | α implied by the t(p99.998) → t(p99.999) jump = 0.33 | ✔ |
| vintage_earlier / vintage_current | 0.9% / 3.4% | abstract, §5.3 | CSV 0.9; WID 2014 = 3.388% | ✔ (page shows "0.90%": m-9) |
| Vintage table, other rows | 23.4 / 8.2 / 2.8 vs 25.8 / 11.2 / 5.4 | page | CSV; WID 25.79 / 11.23 / 5.44 | ✔ |
| dwa_top5_gap | 5.8–7.6 | §5.3, findings note, cc-notes | 5.757 (2020) – 7.595 (2010), DWA Q4 of Y against WID Y | ✔ |
| dwa_bottom50_gap | −0.6 to +0.4 | §5.3, cc-notes | −0.610 (2014) to +0.360 (2009) | ✔ |
| Largest jumps of the top 0.001% share | +1.34 (2020–21), +1.18 (1998–99), +1.00 (2013–14) | method §3.7 | +1.343, +1.175, +0.999 | ✔ |
| Early calibration years | 0.74 → 1.17 → 1.45% | method §3.7 | 0.740 → 1.168 → 1.448 | ✔ |
| 2014 → 2024, the layers just below are flat | top 0.001% 3.39 → 5.58 | method §3.7, paper §5.3 | 99.99–99.999: 2.048 → 2.033; 99.9–99.99: 5.793 → 5.728; 99–99.9: 14.565 → 14.342 | ✔ |
| Odd years | 1975 0.24% between 0.84 / 0.83; 1984 0.38% between 0.51 / 0.52 | method §3.5 | 0.240 (0.840 / 0.830); 0.379 (0.510 / 0.520) | ✔ |

### 2.3 Paper keys — IPP, prices, housing, cross-checks

| Key | Claimed | Where | Recomputed | Match |
|---|---|---|---|---|
| ipp_ratio_top_1% / 0.1% / 0.01% / 0.001% | 0.87 / 1.13 / 1.7 / 2.7 | §5.4, page, method §3.8 | 0.866 / 1.131 / 1.669 / 2.664 (comprehensive ÷ WID nominal 2016) | ✔ |
| ipp_wid_top0001_bn / ipp_div_top0001_bn | 9.2 / 8.1 | §5.4 | 9.19 (0.481% × €1,912.6 bn nominal) / 8.117 | ✔ |
| WID 2016 pre-tax national income | €1.9 tn | method §3.8 | €1,912.6 bn nominal (€2,292.6 bn in 2025 €) | ✔. The unit is correct: the WID column is nominal 2016, comparable with IPP's nominal means. |
| cpi_growth_reduction_1980 | 6% | §6 ("lowers real growth since 1980 by about 6%") | factor(1980) = 1.06779, factor(2024) = 0.99767. 2024/1980 ratio 6.57% lower. Real growth 1980→2024: wealth 181.0% → 162.5%; pre-tax income 51.0% → 41.1%. | ✘ (M-1) |
| cpi_decile_gap_pts | 3.6 | §5.5 | 3.642 | ✔ |
| precommitted_first / _last / years | 13.4% / 30.3% / 1959 / 2025 | §5.5, page | 13.383% / 30.333% (peak 30.96% in 2015) | ✔ |
| years_paris_1996 / _2023 | 19 / 41 | §5.5, findings card, method §3.9 | 18.93 / 41.08 (peak 48.1 in 2020) | ✔ |
| repay_paris_2000 / _2023 | 155% / 236% | same | 155.4% / 236.1% (peak 272% in 2012) | ✔ |
| years_rest_1996 / _2023 | 8 / 13 | same | 7.84 / 13.04 | ✔ |
| repay_rest_2000 / _2023 | 60% / 75% | same | 60.1% / 75.0% | ✔ |
| cnd_bottom50_2019 | 38% (against WID 32%) | §5.2, cc-notes | 38.33% / 32.13% | ✔ |

### 2.4 Hero (DOM, all three concepts, 2024)

| Item | Page | Recomputed | Match |
|---|---|---|---|
| Wealth: bottom half / top 0.001% / equivalence | 4.8% / 5.6% / "poorest 51.9% … (27.5 million people)" | 4.837% / 5.577% / 51.865% (27.47 M) | ✔ |
| Pre-tax income: same | 20.3% / 0.88% / "poorest 13.2% … (7.0 million)" | 20.304% / 0.8827% / **13.25001%**, which formats to "13.3%" | ≈. The 6-decimal JSON share gives 13.2498%. Knife-edge, cosmetic. |
| Post-tax income: same | 31.5% / 0.58% / "poorest 1.5% … (799,000)" | 31.539% / 0.578% / 1.509% (799,000) | ✔ |
| Hero legends (3 × 7 shares) | – | all identical strings | ✔ |
| Hero range note | "4.8% to 6.5%, or 8.1% beyond published" | min/max of {dwa_lower, ggp_central, ggp_low, WID} = 4.774 / 6.454; no_cut 8.067 | ✔ |
| "about 530 people"; "26.5 million" | – | 529.6; 26.48 M | ✔ |
| "many of whom own very little or owe more than they own" | – | Only p0p1 has a negative average (−€421; p1 threshold −€101). p1–p10 average €212–€1,850. | ✔ because of the "or". Note that "owe more than they own" applies to about 1% of adults. |

**What the equivalence means.** Ranking adults from the poorest, the poorest 51.9% (27.5 M adults) together hold 5.58% of net wealth, the same as the top 0.001%. The arithmetic and the interpolation inside the crossing g-percentile (p51–p52) are correct.

### 2.5 Finding cards, summaries and change tables (DOM)

| Item | Page | Recomputed | Match |
|---|---|---|---|
| Card 1 | 530 adults, 5.6%; 1.4% in 1990; others 4.8–6.5% | as §2.1–2.2 | ✔ |
| Card 2 | 26.5 M; 4.8%; 8.9%; €21,100 → €26,800 | ✔ | ✔ |
| Card 3 | 7.7% vs 2.7% of the €9.7 tn | ✔ | ✔ |
| Card 4 | 20.3% → 31.5% (2024) | ✔ | ✔ (m-6) |
| Card 5 | 41 years (2023); 19 (1996) | 41.08 / 18.93 | ✔ |
| Card 6 | "0.90% or 3.4%" | 0.9 / 3.388 | ✔ value; ≈ display (m-9) |
| Findings note | ECB 5.8–7.6 points lower | 5.757–7.595 | ✔ |
| Change table, wealth 1990–2024 (77 cells) + summary + "+€206 bn / +€607 bn" | – | all identical | ✔ |
| Change table, pre-tax (77 cells) + summary (€998 bn; 1.5% / 18.4%; €184 bn / €215 bn) + €5.7 / €9.4 bn | – | all identical | ✔ |
| Change table, post-tax (77 cells) + summary | – | 74 identical. Share effects: B50 +€55.6 bn (page +€55.7), 90–99 −€51.0 bn (page −€51.1), 99.99–99.999 +€118 M (page +€119 M). | ≈ (m-8) |
| Change table, wealth, `ggp_low` (77 cells) + summary (9.0% / 2.7%; €258 bn) | – | all identical, rebuilding 2024 with the scenario | ✔ |
| Pie summaries (3 concepts, plus the scenario) | – | ✔ | ✔ |
| GIC summary, wealth | +2.5% / +0.71% / +6.7%; "8 groups left out" | 2.544 / 0.708 / 6.719; 8 under the code rule, **13 under the documented rule** | ✔ / ≈ (m-5) |
| GIC summary, pre-tax / post-tax | +0.82 / +0.64 / +2.5 (5 left out); +0.82 / +1.1 / +1.8 | 0.816 / 0.642 / 2.467 (5); 0.816 / 1.087 / 1.799 (0) | ✔ |
| Both income totals equal | €998 bn | ptinc and diinc T(1990) = €1,523.1 bn, T(2024) = €2,520.8 bn | ✔ |

### 2.6 Top-tail chapter (`renderTop`) and method §3.7

| Item | Claimed | Where | Recomputed | Match |
|---|---|---|---|---|
| Top table, 36 rows × 6 columns | – | page | 35 rows identical. 1992 WID top 0.001%: €82.75 bn → "€82.7 bn"; page "€82.8 bn". | ≈ (m-8) |
| WID top 0.001% 2024 | €817 bn | page, method | €817.45 bn (also from `ahwealj992` × adults) | ✔ |
| WID top 0.01% 2024 | €1,115 bn | method | €1,115.44 bn | ✔ |
| Forbes 2024 | €631 bn (53; €624 bn quoted) | page, method | 624 / 0.98839 = €631.3 bn; 4.31% of T | ✔ (basis: m-3) |
| Challenges 2024 | €1,242 bn | method | 1,228 / 0.98839 = €1,242.4 bn | ✔ |
| Challenges ÷ WID top 0.01% | 0.49 (2004) → 1.11 (2024); page 49.5% / 111.4% | method, page | 0.49466 / 1.11385 | ✔ (both roundings are consistent) |
| "first year with a published euro total" = 2004 | – | method | the CSV has no euro total before 2004 | ✔ |
| List coverage | 9,000 adults (10 members); 900 (1 member) | page | 500 × 10 × 1.8; 500 × 1 × 1.8 | ✔ |
| List after the 20% cut, 2024 | €994 bn; below WID's €1.2 tn (9,000 adults); exceeds €859 bn (900 adults) | page | €993.9 bn; W₉₀₀₀ = €1,234.9 bn; W₉₀₀ = €858.9 bn | ✔ |
| `rich_list_check` columns (16 years) | – | page table | all identical | ✔ |
| Scenario layer shares, all years, all 4 scenarios | – | `france.json` (comparison only) | max \|Δ\| 9.8e-7 | ✔ |

**Margins (RL_adj − W_n), 1 member per family.** Values in € bn; "fallback" means a year with no published list total, so it stays on WID.

| Year | 2004 | 2006 | 2007 | 2009 | 2010 | 2012 | 2013 | 2014 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| c = 20% | −75.4 | −54.1 | −8.5 | −15.1 | −40.5 | −16.2 | −9.6 | −76.9 | **+2.9** | +67.9 | +47.0 | +75.2 | +117.0 | fallback | +73.8 | +157.1 | +135.0 |
| c = 0 | −32.9 | **−0.8** | +64.5 | +34.3 | +20.1 | +49.7 | +71.0 | +18.2 | +112.3 | +204.0 | +200.3 | +238.2 | +282.1 | fallback | +291.1 | +398.8 | +383.5 |

**How proportional scaling is pinned down.** The method does not say how RL_adj is spread among the richest n. Proportional scaling (one factor on every g-percentile inside n) reproduces the build exactly, which identifies the rule. Add one sentence to §3.7 saying so.

### 2.7 IPP table (page `renderTopIncome`, method §3.8)

Groups are listed from the top 1% to the top 0.001%.

| Column | Claimed | Recomputed (n × mean, or share × nominal NI) | Match |
|---|---|---|---|
| WID pre-tax | 198.8 / 68.1 / **24.7** / 9.2 | 198.78 / 68.09 / **24.650** (24.6497) / 9.19 | ≈ 24.7 vs 24.6 (m-2) |
| IPP taxable | 100.3 / 33.9 / 12.9 / 4.7 | 100.26 / 33.86 / 12.87 / 4.66 | ✔ |
| IPP dividend-imputed | **161.6** / 60.8 / 22.6 / 8.1 | **161.548** / 60.84 / 22.57 / 8.12 | ≈ 161.6 vs 161.5 (m-2) |
| IPP comprehensive | 172.1 / 77.0 / 41.1 / 24.5 | 172.14 / 76.99 / 41.14 / 24.48 | ✔ |
| IPP economic (method only) | 219.4 / 128.0 / 88.9 / **65.0** | 219.41 / 127.95 / 88.94 / **64.949** | ≈ 65.0 vs 64.9 (m-2) |
| Group sizes | 507,000 / 51,000 / 5,070 / 510 adults; 378,000 … 380 households | 50.70 M adults in 2016 | ✔ |

### 2.8 Prices, CPI factor, housing annuity

| Item | Claimed | Where | Recomputed | Match |
|---|---|---|---|---|
| `cpiFactor`: CPI covers every year 1950–2025 | – | `core.js` | no missing year, so no fallback to 1 | ✔ |
| 1950 hold | no step | method §3.3 | held at 1.064253 before 1950 (unheld 1949 would be 1.064018) | ✔ (round-1 M-1 fixed) |
| CPI splice at 1990 | no step | method §3.3 | link factor 1.000099 | ✔ |
| "With the CPI the 1980 level is 6.8% higher" | 6.8% | method §3.3 | factor(1980) = 1.06779 | ✔ level |
| "… and real growth since 1980 correspondingly smaller" | – | method §3.3 | factor(2024) = 0.99767 ≠ 1, so the 2024/1980 ratio is 6.57% lower. Growth shrinks by 18.5 pts for wealth (about a tenth of it) and 9.9 pts for income (about a fifth of it). | ✘ (M-1) |
| Decile CPI 1998–2025 | +56.1 / +54.5 / +52.5% | page prices note, method §3.9 | 56.106 / 54.469 / 52.463 | ✔ |
| Annuity r / (1 − (1+r)^−25) | – | `core.js` | same formula; ECB `MIR.M.FR.B.A2C.A.R.A.2250.EUR.N` (new business, all fixations), yearly mean of 12 months, 2000 = 5.837%, 2023 = 3.009% | ✔ |
| ERFS constant → nominal | – | method §3.9 | The header says "euros 2023 constants". Converting with base-2015 vs base-2025 CPI differs by 0.06% (1996). Break years keep the newer column (2010, 2012, 2020). | ✔ |
| DVF 2025 flats mean | Paris €10,033; rest €3,288 | `france.json` | 10,032.7 (n = 29,662); 3,287.5. Rest = metropolitan France minus the 8 Île-de-France départements, with no DOM. DVF lacks 57/67/68. | ✔ |
| Index carry-back | Paris flats from 1992, province flats from 1995 | method §3.9 | mean of the 4 quarters; province starts 1994-Q4, so the first full year is 1995 | ✔ |
| "DVF Paris 1.9–4.7% above Notaires (2021–2025)" | – | method §3.9 | The Notaires table is no longer in `data/manual`. The 2021 / 2025 ratio is internally consistent, but the level cannot be checked. | unverifiable (m-11) |

### 2.9 Cross-checks (cc-notes, method §3.10)

| Item | Claimed | Recomputed | Match |
|---|---|---|---|
| WID − ERFS, top 10%, 1996–2018 | −1.8 to +3.5 points | −1.80 (2012, **old-method** column) to +3.48 (1996, **old-method** column). Newer method only: −1.70 to +3.30. | ≈ / method mix (m-7) |
| Opposite trends 1996–2018 | – | ERFS +2.30 pts against WID −1.84 pts | ✔ |
| HVP bottom 50%, "6–8%" | 6–8% | 7.68 / 7.18 / 6.65 (1998–2010, old method); 8 / 8 / 8 / 7 (2015–2024, integers, residual assets included) | ✔ loosely; spans a concept break (round-1 m-15 still open) |
| DWA Q4 of Y against WID Y | – | Aligned. A one-year shift would give 5.37–7.83. | ✔ |

### 2.10 Rich-list rows against their quotes (live fetch, robots.txt respected)

**robots.txt:**
- These hosts set only `User-agent: *` rules, none of which cover the article paths: fashionunited.fr, webmanagercenter.com, habarizacomores.com, boursorama.com, lequotidiendupharmacien.fr.
- None names ClaudeBot, Claude-Web or anthropic-ai.
- web.archive.org/robots.txt returns 404.

**Method.** Raw HTML was fetched with curl and the tags stripped. Before matching, NBSP and narrow NBSP, apostrophes, «» and thousands separators were normalised. Each fragment between "…" or "|" was then tested for verbatim presence.

| Row | Source fetched | Fragments | Number and year | Note |
|---|---|---|---|---|
| Challenges 2024, 1,228 | fashionunited.fr (AFP, 2024-07-18) | 3/3 | ✔ 1,228; 245 M threshold; Arnault 190 | |
| Challenges 2004, 153 | web.archive.org copies of lemagchallenges (n° 228, July 2004) | 2/2 | ✔ 153; No. 1 14,246 M | The 153 appears as an aside in a "Coulisses" piece on tax exile ("comparée aux 153 milliards…"), not as the list's headline total. |
| Challenges 2006, 200 | webmanagercenter.com, 2007-07-11 and 2006-07-12 | 2/2 | ✔ "de 200 à 280 milliards" | Retrospective and rounded, as the CSV note says |
| Challenges 2012, 267 | habarizacomores.com blog, 2012-07-12 | 2/2 | ✔ 267; threshold 60 | A reposted Challenges text. The CSV's "WEAK SOURCE" flag is fair. |
| Forbes 2024, €624 bn / 53 | web.archive.org copy of forbes.fr (2024-07-30); boursorama (2024-04-04) | 3/3 | ✔ | The euro total is Forbes France's **July** figure for the April list (m-3). |
| Forbes 2021, $510 bn / €450 bn | fashionunited.fr (2021-04-06); lequotidiendupharmacien.fr (2021-04-13) | 2/2 | ✔ | Both totals are lower bounds ("un peu plus de", "plus de"). |

### 2.11 Keys added to `paper/numbers.md` during this audit (regenerated 23:36, not yet quoted in the paper)

| Key | Claimed | Recomputed | Match |
|---|---|---|---|
| forbes_billionaires_n / forbes_floor | 53 / 4.3% | 53; €631.3 bn ÷ €14,657 bn = 4.307% | ✔ |
| top0001_range_low / _high | 4.3% / 6.5% | Forbes floor 4.307% / ggp_low 6.454% | ✔ arithmetic; ~ label. Forbes counts citizens, including non-residents (the reason the scenarios cut 20%), and the 2024 euro total is a July valuation. So 4.3% is not a strict lower bound for resident adults, and mixing a floor with scenario estimates changes what "range" means. Say so if it is adopted in the paper. |
| poorest_equivalent_low / _high | 48.3% / 54.1% | dwa_lower 48.32% / ggp_low 54.08% (ggp_central 51.86%; no_cut, beyond published assumptions, 57.84%). The bottom curve is rescaled by b50_scen / b50_WID, which is valid because each scenario rescales everything below P95 by one factor. | ✔ |
| captured_top0001_low / _high | 6.5% / 9.0% | 6.49% (dwa_lower) / 9.03% (ggp_low) | ✔ |
| dwa_middle40_gap | 4.7–6.8 | DWA (1 − B50 − T10) minus WID p50p90: 4.71 (2020) – 6.76 (2010) | ✔ |
| pretax_bottom50_2018 / posttax_bottom50_2018 / posttax_bottom50_2019 | 20.3 / 31.9 / 32.1% | 20.34 / 31.89 / 32.13% | ✔ |
| wealth_top1_1950 / _1990 / _2014 | 33.4 / 17.7 / 25.8% | 33.397 / 17.708 / 25.793% | ✔ |
| start_rose_bottom50_after_1950 | "1962, 1964, 1965, 2010" | Starts after 1950 with a positive share effect: **1951–1960**, 1962, 1964, 1965, 2010 | ✘ The list omits 1951–1960. Either name the key "after 1960" or include them (M-2). |
| repay_paris_peak / _year | 272% / 2012 | 272.0% / 2012 | ✔ |

## 3. Discrepancies, ranked, with fixes

There is no critical error: no headline number is wrong. The three "M" items are statements a careful reader can show to be false or misleading from the project's own data.

### M-1. The CPI robustness figure is stated three ways, and none is the growth effect

**Where.**
- `docs/03-method.md` §3.3: "the 1980 level is 6.8% higher and real growth since 1980 correspondingly smaller".
- `paper/paper.md` §6: "lowers real growth since 1980 by about 6%".
- Key `cpi_growth_reduction_1980` = "6%".

**What the data show.**
- factor(1980) = 1.0678 and factor(2024) = 0.9977, so the 2024/1980 real ratio is **6.6% lower** under the CPI. That figure would round to 7%.
- "6%" matches 1 − 1/1.0678 = 6.35%, which ignores that factor(2024) ≠ 1.
- Real *growth* falls much more:
  - wealth 1980→2024: +181.0% → +162.5% (about a tenth of the growth);
  - pre-tax income: +51.0% → +41.1% (about a fifth of the growth).
- This is round-1 m-13, still open.

**Fix.**
- Compute the key as 1 − factor(2024)/factor(1980), which gives 6.6%.
- Paper §6: "Using INSEE consumer prices lowers the 2024 level relative to 1980 by about 7%: real growth of mean wealth since 1980 is 162% instead of 181%, and of pre-tax income 41% instead of 51%."
- Method §3.3: same wording.

### M-2. The start-year sentence in paper §6 is false for two start years and silent on 14 more

**Where.** Paper §6; keys `start_fell_bottom50` and `start_fell_middle40`.

**The paper says:** "the poorest half's share fell from every start year between 1966 and 2009, and rose from starts before 1966"; and "the middle 40%'s share fell from every start between 1971 and 1997".

**Bottom 50%, share effect to 2024.**
- Negative from 1961, 1963, 1966–2009 and **2011–2023**.
- Positive only from starts ≤ 1960, 1962, 1964–1965 and 2010.
- So "rose from starts before 1966" is false for 1961 and 1963 (share 5.49%, the duplicated odd year in method §3.5).
- The share also fell from every recent start except 2010.

**Middle 40%.** It also fell from every start 2002–2023, and rose only from 1998–2001.

**New key.** The key `start_rose_bottom50_after_1950` = "1962, 1964, 1965, 2010", added during this audit, leaves out 1951–1960, all of which also rose. It is correct only as "after 1960".

**Effect.** The key's "between X and Y" framing implies the effect turns positive after 2009 and 1997. It does not.

**Fix.**
- Generate the key as the full set of runs.
- Write: "the poorest half's share fell from every start year from 1966 to 2023 except 2010 (and from the odd years 1961 and 1963); it rose from most starts before 1966, when its share was lower still. The middle 40%'s share fell from every start year after 1970 except 1998–2001."

### M-3. Rich-list scenarios leave gap years on WID inside their ranges, which creates an artificial dip under "no cut"

**Where.** Method §3.7 table ("8 (2016–2024)", "14 (2007–2024)"); paper §5.3; the page's scenario charts.

**What happens.**
- Challenges has no published euro total for 2005, 2008, 2011, 2015 or 2021.
- Those years stay on WID while their neighbours are corrected.
- **`no_cut`.** The top-0.001% series on the page (multiples, stack, levels) runs 2020 **5.22%** → 2021 **4.78%** (WID) → 2022 **6.59%**. That is a drop and rebound that comes from the gap, not from the data, and it is the one visible artificial dip.
- **Other gap years.** 2005, 2008, 2011 and 2015 are understated relative to the scenario's own logic, but sit between or below their neighbours (2008: 2.68 → 2.20 → 1.83; 2011: 2.19 → 2.25 → 2.40; 2015: 3.52 → 3.62 → 3.88), so they do not dip.
- **`ggp_low`.** 2021 sits 0.7 pt below the scenario's own logic. The CSV's "autour de 1.000 milliards" would give RL_adj €894 bn against W₉₀₀ €781 bn (+€112 bn margin) and a corrected 5.47%.
- **3-year smoothing.** With smoothing on, corrected and uncorrected years are averaged together.
- **Band chart.** It plots only list years, so it hides the dip, but the main charts show it.

**Fix (any of):**
- interpolate the correction factor (RL_adj ÷ W_n, or the corrected share) across gap years;
- or mark gap years in the scenario series and break the line;
- in the table, write "8 of the 9 years 2016–2024 (2021: no published total)" and "14 of the 18 years 2007–2024".

### Minor

**m-1. Knife-edge corrections and the "whole g-percentiles" claim.**
- **ggp_low 2016.** It is corrected by **+€2.9 bn** (0.7% of W₉₀₀).
- **no_cut 2006.** It misses correction by **−€0.8 bn** on a rounded retrospective total ("200").
- **Paper §4 wording.** "WID's wealth of the richest n adults is read from whole g-percentiles … so no assumption about the shape inside that bin is needed" is not accurate:
  - n = 900 takes 70% of the second-highest g-percentile (p99.998–p99.999, €94.5 M – €798.7 M, mean €112 M) under a uniform split;
  - n = 9,000 splits p99.98–p99.99.
- **Effect of a within-bin Pareto shape.** Fitted to each bin's own thresholds and mean (α ≈ 6.1–6.4), it raises W₉₀₀ by €1.8–2.6 bn:
  - 2016's margin falls to +€1.2 bn;
  - the 2024 shares move by ≤ 0.02 pt (6.454 → 6.436; 8.067 → 8.045);
  - no year flips on its own.
- **Combined effect.** With the earlier CSV value for 2016 (454 instead of 456), the Pareto shape flips 2016, and the count becomes 7.
- **Fix.**
  - Align the paper with method §3.7: "whole g-percentiles except a uniform split of the next one".
  - Report the "8 years" as sensitive to ±€3 bn in 2016.

**m-2. Double rounding in the IPP block.**
- `france.json` stores € bn at 2 decimals; the page and method §3.8 print 1 decimal.
- So 24.6497 → 24.65 → **24.7** (true 24.6), 161.548 → 161.55 → **161.6** (true 161.5) and 64.949 → 64.95 → **65.0** (true 64.9).
- **Where:** page IPP table (WID top 0.01%, dividend top 1%); method §3.8 table (also economic top 0.001%).
- Ratios are unaffected.
- **Fix:** store at least 3 decimals.

**m-3. Forbes series on a mixed basis.**
- **What is stated.** Method §3.3 and the page note say "Forbes dollar totals are converted at each year's average rate".
- **What is used.** Only 2022 is converted from dollars. 2017, 2020, 2021 and 2024 use quoted euro figures:
  - 2017 "environ 228" against $245 bn × 0.8852 = €216.9 bn (5% higher);
  - 2021 "plus de 450" (a lower bound) against $510 bn × fx = €431 bn (4% higher);
  - 2024 €624 bn is Forbes France's **30 July 2024** figure for the April list, at a different valuation date and exchange rate.
- **Fix:** say "euro totals as quoted where available (2017, 2020, 2021, 2024), otherwise dollars at the yearly average rate", and flag 2021 as a lower bound.

**m-4. Method §3.4 "the largest difference today is 0.00009".**
- The actual value is 0.0000952 (ptinc p99–99.9, 1988).
- numbers.md "0.00010" (rounded up) and the paper's "below 0.00010" are correct.
- **Fix:** write "0.000095" in the method.

**m-5. Growth-incidence exclusion rule: doc and code disagree.**
- Method §3.6 says groups "below 1% of the overall mean in either year" are left out. The code uses 1% of min(mean₀, mean₁) for both years.
- Wealth 1990–2024 excludes **8** groups under the code and **13** under the documented rule.
- The page prints 8.
- The growth figures in the summary do not depend on it.
- **Fix:** document the min rule.

**m-6. Post-tax 2024 is presented without its caveat in the abstract and finding card.**
- **Where:** "Taxes, benefits and public services raise the poorest half's share of income from 20.3% to 31.5%" (abstract; card 4, "(2024)").
- **Why it needs the caveat.** Post-tax 2019–2024 carries WID quality flag 4, with 2019 pre/post ratios by g-percentile (method §3.10). The 2024 gap therefore reflects the 2019 tax-benefit system.
- **For comparison:** 2018, the last year not extrapolated, gives 20.3% → 31.9%.
- **Fix:** add "(2024, extrapolated from 2019 tax and benefit ratios)", or quote 2018.

**m-7. ERFS gap mixes old and new methods.**
- Both ends of "−1.8 to +3.5 points over 1996–2018" (cc-notes, method §3.10) come from superseded columns in break years (2012 old, 1996 old). Method §3.9 says the newer method is kept.
- The newer method alone gives **−1.7 to +3.3**.
- **Fix:** restrict `gap()` to the newer chain, or say that break years include both.

**m-8. Last-digit flips from JSON precision.**
- Five page cells differ by one unit from full precision:
  - post-tax share effects +€55.7 / −€51.1 bn / +€119 M (true +55.65 / −51.05 / +118 M);
  - top table 1992 €82.8 bn (true 82.75);
  - pre-tax hero "13.2%" (true 13.25001%).
- **Cause:** shares are stored at 6 decimals and averages as integers. A difference of two 6-decimal shares times a €2 tn total can move a share effect by about €1 M; here that crosses a rounding boundary.
- **Fix (optional):** store shares at 8 decimals.

**m-9. Display precision and signs.**
- Card 6 shows "0.90%" for a source figure of 0.9%, which suggests precision the source does not have. It comes from `pct()` using 2 decimals below 1%.
- cc-notes prints "−0.6 to 0.4 points" without "+", while the paper has "-0.6 to +0.4" with an ASCII hyphen.
- **Fix:** format the vintage value at the source's precision, and add the sign in `sg()`.

**m-10. Inconsistent citation for the rich-list parameters.**
- Method §3.7 cites "Garbinti, Goupille-Lebret & Piketty (2021, appendix H)".
- Paper §4 and `ggp_richlist_comparison.csv` cite the 2016 data appendix (WID WP 2016/6, Appendix H.2).
- Paper §5.3 cites WP 2016/5 for the 0.9% vintage, which is correct for that table.
- **Fix:** cite WP 2016/6 for the parameters in the method too.

**m-11. Unverifiable or carried-over items.**
- "DVF Paris 1.9–4.7% above Notaires (2021–2025)" cannot be checked from repository files now that the Notaires table has been removed. Mark it as external or keep the source table.
- The HVP concept break at 2015 is still not marked (round-1 m-15).
- "Prices about 7% higher in the Paris urban area" (static page text) was not rechecked in this round.

**m-12. Wording.**
- Income change summaries say "The bottom half's real holdings went up by €184 bn" for a yearly *income* flow. Use "yearly income".
- The housing endpoints (19 → 41 years; 155% → 236%) are correct but hide the peaks: 48 years in 2020 and 272% in 2012. Consider "peaking at 48 years in 2020".
- Paper Table 2's 1980 bottom-50% figure, 8.4% (g-percentile sum 8.449%), will read as 8.5% to anyone checking WID's published 0.0845. A footnote that shares are summed from g-percentiles would prevent a false error report.

## 3b. Status against `paper/paper.md` as revised at 23:38, during this audit

The page DOM was re-dumped against the 23:36 data build and the 23:17 `site/index.html`. The text is identical to the 23:19 dump and the same five last-digit cells differ.

`site/index.html` was edited again at 23:39, after the final dump, so page-text changes made after that time are not covered by this audit. `docs/03-method.md` (23:18) did not change during the audit.

`paper/paper.md` was rewritten while the audit ran. As of 23:38:

| Item | Status in the 23:38 paper |
|---|---|
| M-1, CPI | **Open.** §6 still says "lowers real growth since 1980 by about 6%". |
| M-2, start years | **Partly fixed.** Bottom half: "fell from every start year between 1966 and 2009 and from most later ones; it rose from starts between 1950 and 1960 and from 1962, 1964, 1965, 2010" is now correct (1961 and 1963 fell, 2011–2023 fell). Middle 40%: "fell from every start between 1971 and 1997" still omits 2002–2023. |
| M-3, gap years | **Open.** "8 years corrected" and "14 years corrected"; the page dip in 2021 is unchanged. |
| m-1, "read from whole g-percentiles … no assumption about the shape" | **Open** (§4). |
| m-6, post-tax 2024 | **Fixed.** The abstract now quotes 2018 (20.3% → 31.9%). §5.2 says the 2024 figures "contain no new information". Verified: the 2024 pre-tax g-percentile shares equal 2023's exactly (bottom 50% 20.3037%, top 0.001% 0.8827% in both years). |
| New: Forbes floor 4.3% | §5.3 now says "a floor, up to residence and valuation". Acceptable with that caveat. |
| **New, m-13: envelopes are inconsistent** | The top-0.001% share range is now "4.3% to 6.5%" (low end = Forbes floor). The ranges for the same group's capture of growth, "6.5% to 9.0%", and for the poorest-equivalent, "48.3% to 54.1%", use the ECB scenario (4.8%) as their low end. At the 4.3% floor, the capture would be **5.8%**. The poorest-equivalent at the floor is 48.4%, so that range happens to hold. Fix: use one envelope throughout, either scenarios only (4.8–6.5% / 6.5–9.0%) or floor to ggp_low (4.3–6.5% / 5.8–9.0%). |

## 4. Year alignment, units, price base

- **Units.** All euro amounts are constant 2025 € through `inyixxi999` (2025 = 1). T(y) agrees with `mhweali999` to €0.0001 bn.
- **IPP.** The comparison correctly uses nominal 2016: real × `inyixxi999(2016)` = €1,912.6 bn.
- **Challenges and Forbes.** They are deflated by the same-year deflator.
- **Timing.**
  - Forbes 2024 is a July euro quote (m-3).
  - Challenges (July) is paired with WID year Y with no shift, as stated on the page.
  - DWA is Q4 of Y against WID Y.
  - ECB rates are calendar-year means.
  - ERFS: income year Y against the year-Y price.
- **Duplicates.** No duplicate keys in the WID variables used.
- **Scenario years.** Gap years 2005, 2008, 2011, 2015 and 2021 stay on WID (M-3).
