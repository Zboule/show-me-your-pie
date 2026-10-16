# Independent numbers audit

Auditor: independent re-computation, 2026-10-16. Scope: the numbers in
`site/data/france.json`, in `site/index.html` (both the static text and the text the page
generates from the data), in `README.md`, `docs/*.md` and `docs/notes/*.md`. Everything
was recomputed from `data/raw/` and `data/manual/` with the auditor's own scripts. No
project code was imported or run, and no project file other than this one was modified.

Conventions:
- "pt" = percentage point.
- Shares are WID's 4-decimal published values.
- A difference ≤ 0.05 pt, or ≤ 0.5% of a level, counts as a match.
- "External" means the number comes from a publication outside the repository and
  cannot be checked from local files.

## 0. Summary

The WID backbone is clean. The rest of the data and the text are not.

**What is right**
- `france.json` reproduces the raw WID file exactly. Across 43,245 checked values (all
  shares, averages, thresholds and g-percentile averages for the three concepts), not
  one differs.
- Layer shares and averages, transfers, the €701 bn / €1.3 bn headline, the
  Forbes 4.3% tile, the 818 / 1,115 / 1,242 bn top-tail table, the 0.43 → 1.11
  ratio and the three rich-list scenarios (5.6% / 6.9% / 8.6%, 16 and 26 corrected
  years) all reproduce, to rounding, from independent code.

**What is wrong is mostly in the text**
- Claims about ranges, extremes and "every year" are not true of the whole series.
- Some statements contradict what the page computes.
- Two page-logic defects distort what the reader sees:
  - a 6.4% step at 1950 in CPI mode;
  - a misleading bottom-half growth sentence in the growth-incidence curve.
- The rich-list scenario's k = 1 ignores couples. It adds only about 0.5 pt to the 2024
  top-0.001% share.

Section 3 ranks the discrepancies.

**Audit scripts**
- Core WID, top tail and scenarios:
  `<scratch>/audit/core/`
  - `widload.py`: loader. It asserts that no (variable, percentile, year) key is
    duplicated; there are none among 1,616,784 rows.
  - `c1_layers.py`: layers.
  - `c2_consistency.py`: share against average, and g-percentiles.
  - `c3_mid.py`: middle 40%.
  - `c4_headline.py`: tiles and the top-tail table.
  - `c5_dq.py`: data-quality flags.
  - `c6_jumps.py`: jumps, minima, discontinuity.
  - `c7_scen.py`: scenarios.
  - `c8_misc.py`: composition, deflator, adults.
  - `c9_json_vs_raw.py`: the full JSON against raw.
  - `c10_transfers.py`: transfers.
  - `c11_disc_series.py`: top-bin discontinuity over time.
  - `c12_gic.py`: growth-incidence filter.
  - `c13_cpi_factor.py`: CPI price-option factor.
  - `c14_k18.py`: scenario shares at k = 1.8.
- DWA: `.../scratchpad/audit/dwa/audit_dwa.py`, `audit_dwa_extra.py`, `audit_dq.py`.
- INSEE / IPP: `.../scratchpad/audit/insee/` (see §2.6).
- Prices / housing: `.../scratchpad/audit/prices/` (see §2.7).

Run each with `python3 -I <script>`. The `...` stands for
`<scratch>`.

## 1. WID backbone: layers (check 1)

The layers are computed independently from `s{concept}j992` with share[0,50) = s(p0p50),
share[50,90) = 1 − s(p0p50) − s(p90p100), and so on. A layer's average is
share × a(p0p100) × 100 / width. Every layer share and average in `france.json` matches
to the last digit, in every year of every concept: the largest share difference is
1.4e-16 and no average differs by more than €1.

| Concept | Year | Mean | B50 | M40 | 90–99 | 99–99.9 | 99.9–99.99 | 99.99–99.999 | Top 0.001% |
|---|---|---|---|---|---|---|---|---|---|
| hweal | 1900 | 41,392 | 1.57% | 13.23% | 30.23% | 29.61% | 16.27% | 6.48% | 2.61% |
| hweal | 1950 | 17,072 | 3.18% | 24.57% | 38.85% | 20.77% | 8.53% | 2.77% | 1.33% |
| hweal | 1980 | 98,498 | 8.45% | 40.00% | 34.38% | 11.33% | 3.71% | 1.33% | 0.80% |
| hweal | 2000 | 155,419 | 5.66% | 33.84% | 30.66% | 15.60% | 7.83% | 3.25% | 3.16% |
| hweal | 2014 | 245,065 | 4.99% | 36.31% | 32.91% | 14.56% | 5.79% | 2.05% | 3.39% |
| hweal | 2024 | 276,775 | 4.84% | 35.28% | 32.20% | 14.34% | 5.73% | 2.03% | 5.58% |
| ptinc | 1900 | 5,863 | 16.30% | 34.28% | 25.73% | 14.61% | 5.74% | 2.12% | 1.22% |
| ptinc | 1950 | 9,568 | 19.46% | 46.48% | 23.63% | 6.80% | 2.47% | 0.79% | 0.37% |
| ptinc | 1980 | 31,532 | 22.66% | 48.58% | 21.22% | 5.13% | 1.48% | 0.51% | 0.42% |
| ptinc | 2000 | 42,263 | 20.54% | 45.87% | 22.26% | 7.02% | 2.78% | 1.02% | 0.51% |
| ptinc | 2014 | 44,816 | 21.12% | 46.39% | 22.70% | 6.54% | 2.11% | 0.73% | 0.41% |
| ptinc | 2024 | 47,600 | 20.30% | 45.67% | 22.21% | 7.10% | 2.74% | 1.10% | 0.88% |
| diinc | 1980 | 31,532 | 28.37% | 46.68% | 18.56% | 4.34% | 1.25% | 0.44% | 0.36% |
| diinc | 2000 | 42,263 | 30.68% | 43.68% | 17.51% | 5.02% | 2.00% | 0.74% | 0.37% |
| diinc | 2014 | 44,816 | 32.17% | 45.09% | 16.75% | 4.04% | 1.26% | 0.44% | 0.25% |
| diinc | 2024 | 47,600 | 31.54% | 44.67% | 16.61% | 4.34% | 1.60% | 0.66% | 0.58% |

Post-tax national income exists only from 1980, so 1900 and 1950 are not available for
`diinc`. All layer averages match `france.json`; they are omitted from the table for
space and can be printed with `c1_layers.py`. For example, the 2024 wealth averages are
26,792 / 244,116 / 990,240 / 4.41 M / 17.6 M / 62.4 M / 1,544 M.

**Do the layers sum to 1?** They do, in every year, but with this construction the test
cannot fail: the seven differences telescope to exactly 1. The project's "shares sum to
1" test therefore checks nothing. Four checks that can fail were run instead:

| Check | Result |
|---|---|
| Sum of the 127 g-percentile shares, 6 years × 3 concepts | 0.9994–1.0007. This is WID's 4-decimal rounding; there is no structural gap. |
| g-percentile averages × widths against the mean | Within 0.0004% everywhere. |
| Share-derived averages against WID's own `a` variables for the same groups (p0p50, p90p100, p99p100, p99.9p100, p99.99p100, p99.999p100) | Within 0.2% for wide groups. Up to 1.6% (ptinc 1982) and 2.0% (diinc 1984) for the top 0.001%, because a 4-decimal share of 0.0036 carries up to ±1.4% rounding. |
| **Middle 40% wealth:** the share-derived average against WID's published `ahwealj992 p50p90` | **WID's own `a` variable is 3.6–6.7% lower** in every recent year (2008: 214,744 against 224,873; 2023: 234,301 against 250,000). The g-percentile averages p50…p90 agree with the share-derived value (250,011 in 2023), so WID's `ap50p90` is the inconsistent series. The project does not use it. This is a WID-side defect, worth knowing if anyone switches to reading averages directly. |

**Year coverage.**
- ptinc in `france.json` has gaps in 1901–1909 and 1911–1914. WID itself has no annual
  values there.
- hweal is missing 1901, 1906 and 1908. Those years are absent from the raw WID file.
- `extrapolated_from` (ptinc and diinc 2019, hweal 2015) matches the raw `data_quality`
  flags exactly. For income, 2019–2024 have `data_quality` = 4 and earlier years 5; for
  wealth, 2015–2024 have 0 and 1970–2014 have 4.

## 2. Table of checked numbers

### 2.1 Headline tiles and page summaries (wealth, 1980 → 2024, WID as published)

| Claim | Where | Claimed | Recomputed | Match | Comment |
|---|---|---|---|---|---|
| Top 0.001% wealth share, 1980 | tile 1 (JS); method doc | 0.80% | 0.80% (raw 0.0080) | ✔ | |
| Same, with the 3-year average on | pie summary when "3-year average" is selected | 0.74% | 0.74% (mean of 0.73, 0.80, 0.69) | ✔ | This is why the page shows 0.80% or 0.74%. The tile ignores the smoothing toggle while the pie summary applies it, so the two disagree on screen. Smoothing is also asymmetric: 2024, the last year, is never averaged. See §3, m-7. |
| Top 0.001% wealth share, 2024 | tile 1; §3.7 table | 5.6% | 5.58% | ✔ | |
| Bottom 50% wealth share 1980 → 2024 | tile 2 | 8.5% → 4.8% | 8.45% → 4.84% | ✔ | 8.45% rounds to "8.5%" in JS. |
| Adults in the top 0.001%, 2024 | tiles, pie summary, README, docs | ~530 | 529.6 (52,956,956 × 1e-5) | ✔ | |
| Bottom-half adults | tile 2 | 26.5 million | 26.48 M | ✔ | |
| Layer sizes | method §3.4 | 26.5 M / 21.2 M / 4.8 M / 477,000 / 48,000 / 4,770 / 530 | 26.48 M / 21.18 M / 4.77 M / 476,613 / 47,661 / 4,766 / 530 | ✔ | |
| Euros "moved to the top 0.001%" | tile 4 | €701 bn | €700.6 bn = (0.0558 − 0.0080) × €14,657.2 bn | ✔ | The total equals `mhweali999` 2024 (€14,657.2 bn). |
| Euros per member | tile 4 | €1.3 bn each | €1.323 bn | ✔ | |
| Same from other start years | method §3.5: 1980 "gives a larger transfer than 1900 or 1950" | – | 1900: €435 bn; 1950: €623 bn; 1970: €758 bn; 1983: €743 bn; 2000: €355 bn | ✔ | The statement holds against 1900 and 1950. 1970 and 1983 give larger figures. |
| Is the 1980 value fragile? | – | – | 1979 start: €711 bn; 1981 start: €717 bn | – | Robust to ±1 year. But the 1970s top-bin series is erratic: 0.24% in 1975, 0.83% in 1976, 0.41% in 1970, 0.83% in 1971. A 1975 start gives €783 bn. |
| Other transfers 1980 → 2024 (wealth) | transfer chart | – | B50 −€529 bn; M40 −€692 bn; 90–99 −€320 bn; 99–99.9 +€441 bn; 99.9–99.99 +€296 bn; 99.99–99.999 +€103 bn; top 0.001% +€701 bn; total moved €1,540 bn; sum 0 | ✔ | |
| Forbes billionaires, 2024 | tile 3, top summary, §3.7 | 53 people | 53 (CSV row 2024) | ✔ | This is the April 2024 list. |
| Forbes total, constant 2025 € | tile 3, §3.7 | €630 bn | $673.5 bn × 0.92389 € / $ ÷ 0.98839 = €629.6 bn | ✔ | |
| Forbes share of household wealth | tile 3 | ~4.3% | 4.30% | ✔ | |
| "about one adult in a million" | top summary | – | 53 / 52.96 M = 1.0 per million | ✔ | |
| WID top 0.001% total, 2024 | §3.7, top summary | €818 bn | €818 bn from the share (0.0558 × T), €817 bn from raw `ahwealj992` | ✔ | The page uses the share-derived layer average for the top 0.001% and the raw average for the top 0.01%. The difference is ≤ €1 bn. |
| WID top 0.01% total, 2024 | §3.7 | €1,115 bn | €1,115 bn (raw `ahwealj992 p99.99p100` × adults × 1e-4) | ✔ | |
| Challenges 500, 2024, constant 2025 € | §3.7 | €1,242 bn | 1,228 ÷ 0.98839 = €1,242 bn | ✔ | |
| Challenges ÷ WID top 0.01% | §3.7, top summary | 0.43 (1996) → 1.11 (2024) | 0.432 → 1.114 | ✔ | The page prints "43.2%" and "111.4%". |
| §3.7 table, other rows | §3.7 | 1996: –/131/124/286/0.43; 2005: 73/208/231/426/0.54; 2014: 216/418/480/670/0.72; 2019: –/534/828/824/1.00 | 1996: 131/124/286/0.432; 2005: 73/208/231/426/0.543; 2014: 216/418/480/670/0.717; 2019: 534/828/824/1.005 | ✔ | Two problems. **2005 Forbes €73 bn is a lower bound** (CSV note: incomplete list), and the page drops it for that reason; the doc table shows it unflagged. **2019 Forbes is €343 bn**, yet the table shows "–". |
| "more than all of it since 2019" | §3.7 | – | 1.005, 1.032, 1.010, 1.016, 1.129, 1.114 (2019–2024) | ✔ | Barely: 2019 is 1.005. |
| 20% non-resident cut, 2024 | §3.7 | €994 bn; "1.2× WID top 0.001%" | €993.6 bn; 1.215× | ✔ | |
| "Forbes sits inside WID's top 0.001%" | §3.7 | – | WID top 0.001% ≥ Forbes in every year 2001–2024 (2024: 818 against 630) | ✔ | |
| Challenges francs → euros | `challenges_500.csv` notes | 1996 €80 bn (536 MdF); 1999 €122 bn (799 MdF); 2000 €191 bn (1,259 MdF); 2001 €177 bn (1,163 MdF) | At 6.55957: €81.7 bn / €121.8 bn / €191.9 bn / €177.3 bn | ✔ / ~ | 1996 uses IdO's €80 bn, 2% below the franc figure. Immaterial. |
| Challenges 2018 | `challenges_500.csv` | 670 (revised; 650 at publication) | 670 used | – | Documented choice. |
| Challenges 2024 total | `rich-lists.md` §4 | 1,228 Md€ | CSV 1,228 | ✔ | |

### 2.2 Rich-list scenarios (method §3.7; `top_tail.py` spec re-implemented from scratch)

| Claim | Where | Claimed | Recomputed | Match | Comment |
|---|---|---|---|---|---|
| WID as published, top 0.001%, 2024 | §3.7 table | 5.6% | 5.58% | ✔ | |
| Spread (k = 10, c = 20%): years changed | §3.7 | none | none. WID's richest 5,000 adults hold €1,103 bn in 2024 against RL_adj €994 bn; €818 bn against €662 bn in 2019; €297 bn against €99 bn in 1996 | ✔ | The page does not offer this scenario, so the docs describe an option the reader cannot select (§3, m-5). |
| Concentrated (k = 1, c = 20%): years changed | §3.7 | 16 | 16: 2007–2013 and 2016–2024 | ✔ | |
| Concentrated, 2024 | §3.7 | 6.9% | 6.95% | ✔ | |
| Upper (k = 1, c = 0) | §3.7 | 26 (1997–2024) | 26 years, but **not 1997–2024 as a block**. 1999 and 2003 are unchanged, and 1997–2024 spans 28 years. | ~ | The page's scenario note prints "26 years (1997–2024)" with the same ambiguity. |
| Upper, 2024 | §3.7 | 8.6% | 8.64% | ✔ | |
| All scenario layer shares, all years | `france.json` `scenarios.layers` | – | Maximum difference from the auditor's re-implementation: 6.3e-7 | ✔ | Totals are preserved; every scenario row sums to 1.000000. |
| Is k = 1 consistent with WID's unit? | §3.7 | "values … Garbinti et al. use" | GGP use k = 1, 10 and 15 **with 80% of members married**. Under WID's equal split, a married member is two adults each holding half. Even a single-member family is about 1.8 equal-split adults. With k = 1.8 and c = 0, 21 years change; with k = 2, 19 years. 2024 top-0.001% share at k = 1.8: 6.46% (c = 20%) and 8.07% (c = 0), against 6.95% and 8.64% (`c14_k18.py`). | ~ (method) | See §3, m-1. |

### 2.3 Method-doc and page statements on WID wealth dynamics

| Claim | Where | Claimed | Recomputed | Match | Comment |
|---|---|---|---|---|---|
| "The two largest one-year jumps of that share (2.4% → 3.4% in 2013–2014, 3.4% → 4.8% in 2020–2021)" | method §3.5; page limits: "Its largest one-year jumps (2014 and 2021)" | 2014 and 2021 are the two largest | Largest rises: 2020→21 +1.34 pt; **1998→99 +1.18 pt**; 2013→14 +1.00 pt; 1935→36 +0.92 pt. In absolute size, 1940→41 (−1.36 pt) is the largest of all. | ✘ | The 2014 jump is the **third**-largest rise. The 1999 jump is bigger and is not discussed. The levels 2.39 → 3.39 and 3.44 → 4.78 are correct. |
| Forbes 24 → 43 billionaires (2013 → 2014); $304 bn → $512 bn (2020 → 2021) | method §3.5 | as stated | CSV: 24 → 43; 304.3 → 512.2 | ✔ | Forbes list Y lines up with the WID-year-Y jump, which suggests WID tops year Y up with the April-Y list (a March-Y valuation). |
| "1980, close to the twentieth century's low point for top wealth shares" | hero note; concepts §1.7; method §3.5 | – | The 1900–2000 minimum is **1984** for the top 10%, 1%, 0.1% and 0.01%, and **1975** (0.24%) for the top 0.001%. Among 98 years, 1980 ranks 8th lowest for the top 1% and 15th for the top 0.001%. | ~ | Defensible as "close to". But 1980 is a local spike for the top 0.001% (0.73% in 1979, 0.80% in 1980, 0.69% in 1981). |
| Discontinuity: 2024 top-bin threshold €799 M against €112 M average of the bin below; 2010: €284 M against €115 M | method §3.7 | as stated | 2024: t(p99.998) €94.5 M, a(p99.998–999) €112.0 M, t(p99.999) €798.7 M, a(top) €1,543.6 M. 2010: €96.9 M, €115.2 M, €283.8 M, €480.5 M. | ✔ | Internally possible: the bin below averages €112 M on [€94.5 M, €798.7 M], so it is heavily bottom-loaded, a local Pareto α of about 6.4 against about 2.07 in the top bin. The ratio t(p99.999) / a(below) is already 2.4 in 1988 and 3.0 in 1999, rising to 4.5 in 2014 and 7.1 in 2024. So the separate estimation of the top bin long predates the 2025 Forbes top-up, which only widens the gap. |
| "the shares then move only with the asset totals in the national accounts" (post-2014) / "Part of the recent rise … is calibration" | method §3.5; page | – | Not testable locally: no pre-top-up series in the file. | n/a | See m-3 and m-10 on the 1999 jump. |
| GGP (2016 WP) 0.9% in 2014 against current WID 3.4% | method §3.8d; `top_wealth_estimates.csv` | 0.9% / 3.4% | CSV 0.9; raw 2014 = 3.39% | ✔ | **The doc gives no reason for the gap. A reader will assume the 2025 Forbes top-up, but that cannot account for it alone.** Forbes 2014 is €216 bn, 1.75% of total wealth. Even if WID's raw model had no billionaire wealth at all, the top-up adds at most 1.75 pt (0.9 → ≤ 2.65%). At least 0.75 pt comes from other vintage changes. The other rows (GGP 23.4 / 8.2 / 2.8% for the top 1 / 0.1 / 0.01%) are in §2.6. |
| Wealth-composition series (housing share of gross assets) | method §3.8; page chart | hou / (hou + bus + fin), deciles averaged for B50 and M40 | `france.json` composition matches raw `ahw{hou,bus,fin,deb}j992` exactly, and the decile averaging is reproduced | ✔ | **But the components do not reconcile with the current net-wealth series**: hou + bus + fin − deb against `ahwealj992` is −11% (p90p100, 1970), −23% (p90p100, 2014), −26% (p99p100, 2014), **−40% (p99.9p100, 2014)**, and +256% for p0p10 in 2014. At the macro level the identity holds exactly. So the group composition comes from a different vintage or scaling. The housing share is a ratio, but the missing top wealth is almost certainly business or financial, so the top groups' housing share is probably overstated. See §3, m-11. |
| Concepts doc examples: "€233k pre-tax income puts you at P99"; "top 1% earn €562k on average"; "receive 11.8%" | concepts §1.5 table | 233k / 562k / 11.8% | 2024 `ptincj992`: t 233,015; a 562,442; s 11.82% | ✔ | The year is not stated (2024). |
| "about 53 million adults in 2024 … top 0.0001% about 53" | concepts §1.6 | – | 52.96 M | ✔ | |
| "127 fractiles"; "top 1% (28 groups)" | method §3.6, page | – | 99 + 9 + 9 + 10 = 127; 9 + 9 + 10 = 28 | ✔ | |
| Coverage: income 1820–2024 (post-tax 1980–2024), wealth 1800–2024; "cash-only series … stops in 1979" | data doc §2; method §3.2 | – | sptincj992 1820–2024; sdiincj992 1980–2024; shwealj992 1800–2024; scaincj992 1900–1979 | ✔ | |
| Extrapolated years: wealth after 2014, income after 2018 | page limits; concepts §1.7 | – | `data_quality` 0 for wealth 2015–2024; 4 for income 2019–2024 | ✔ | |
| "WID national-income price index" as the deflator | method §3.2/3.3, page | – | Metadata: `inyixxi999` = GDP deflator (UN SNA) for 1980–2024, and **2025 = IMF WEO projection** | ~ | The whole price base ("constant 2025 euros") rests on a projected 2025 deflator and will move when WID revises 2025. See §3, m-12. |
| Price base and units | `france.json` meta | 2025 € | `deflator[2025]` = 1.0; JSON deflator equals raw `inyixxi999` to 5 decimals (worst relative error 1.3% in 1900, because 0.00034 has two significant digits; ≤ 0.003% after 1950) | ✔ | The pre-1950 rounding only matters if something nominal before 1950 is deflated with the JSON deflator. Nothing is at present. |
| Forbes USD conversion | method §3.3 | yearly-average `xlcusxi999` | 2024: 0.92389 €/$ | ✔ / ~ | Forbes values fortunes in early March; the annual average differs by under 1% in 2024, but more in volatile years. |
| IPP table: WID column [10.39, 3.56, 1.29, 0.48]% for 2016 | `france.json` `ipp_top_income` | – | `sptincj992` 2016 = 0.1039 / 0.0356 / 0.0129 / 0.0048 (equal-split). `sptinci992` (individual) ends in 2014. | ✔ | IPP's unit is the tax household (foyer), so equal-split adults are the closest available WID unit. |
| GIC exclusion rule | method §3.6: "below 1% of the overall mean in either year" | 1% of each year's mean | The page uses `0.01 × min(mean0, mean1)` for both years. For wealth 1980 → 2024 (the default view) it drops p0–p6; the spec drops p0–p12. For wealth 1950 → 2024 it drops only p0; the spec drops p0–p12. | ✘ | The generated sentence "the bottom-half groups averaged X% a year" reads **+0.02%/yr** under the page rule and **+0.51%/yr** under the documented rule, for 1980 → 2024 wealth. It is also an unweighted mean of group growth rates over the groups kept, not the growth of the bottom half's average. That growth is **+1.09%/yr** (16,646 → 26,792). See §3, M-4. |
| GIC, other values (default view, wealth 1980 → 2024) | page summary | – | Mean +2.38%/yr; top 0.001% g-percentile +7.00%/yr | ✔ | WID's 1980 bottom g-percentiles are evenly spaced (984, 1,967, 2,951, 3,935, 4,918 €), which looks interpolated rather than observed. Real wealth for p1–p15 falls 2–5%/yr. Treat the bottom of the wealth curve as a modelling artefact. |

### 2.4 Page static text and documentation consistency (non-WID logic)

| Claim | Where | Claimed | Recomputed / observed | Match | Comment |
|---|---|---|---|---|---|
| Method item 7: "Housing. INSEE's index of existing-home prices (1996 onwards) divided by each layer's nominal income after tax." | `site/index.html`, "How this is computed" | an HPI ÷ post-tax income index | The page draws no such index. `renderHousing` plots **years of pre-tax income** (`concepts.ptinc`) for a 70 m² flat in Paris and in the rest of France. `france.json.hpi` is not used by the page. | ✘ | Stale text. §3.8c says pre-tax income is used *because* post-tax national income includes in-kind services. |
| "Below the top 0.001% only rich lists exist" | page method item 6 | – | Concepts §1.6 uses the same wording ("Below 0.001% no statistical source exists"), so the two are consistent. "Below" here means "a smaller fraction than". | ~ | Ambiguous: a reader may take "below the top 0.001%" to mean the layers under it. Suggest "Inside the top 0.001%". |
| Page drops Forbes before 2010 as lower bounds | page top table note | – | method §3.7 table prints Forbes 2005 = €73 bn without the caveat | ✘ | Inconsistent. Either flag it as a lower bound or remove it. |
| §3.7 table: Forbes 2019 "–" | method §3.7 | – | Forbes 2019 is in the CSV: 41 people, $329.9 bn, €343 bn | ✘ | Missing value. |
| "Spread" scenario row | method §3.7 | offered | not among the page's `#scenario` options (`wid`, `concentrated`, `upper`) | ~ | The doc describes a scenario the reader cannot select. |
| §3.8d "IPP comprehensive income … is 1.3× to 4× larger at the top: top 0.001% 2.0% … or 5.1% … vs WID 0.5%" | method §3.8d | 1.3×–4× | 5.08 / 0.48 = **10.6×** for the 2023 note. The 2025 paper gives 1.38 / 1.04 = 1.33× (top 1%) to 1.97 / 0.48 = 4.1× (top 0.001%). | ✘ | The range describes the 2025 paper only; the same sentence cites the 2023 note at 10×. |
| CPI price option: "INSEE's CPI is too coarse before 1950, so earlier years stay on WID" | `site/index.html` `priceFactor`; method §3.8c | value_cpi = value × defl / cpi from 1950 | The factor defl / cpi is 1.0645 in 1949 and 1.0644 in 1950. The page sets it to 1 before 1950, so with "Consumer prices" selected **every real level steps up 6.4% between 1949 and 1950**. That step is an artefact. Transfers or growth rates from a pre-1950 start year to a post-1950 end year mix the two indices. | ✘ | Fix: rescale the WID-deflated pre-1950 values by the 1950 factor (chain-link), or disable CPI for start years before 1950. |
| "real growth since 1980 is about 6% smaller with the CPI" | method §3.8c | ~6% | The 2024 level relative to 1980 is 6.6% lower (factor ratio 0.934, the same for all concepts). Mean income growth 1980 → 2024: +51.0% (WID) against +41.0% (CPI). Wealth: +181% against +162%. | ~ | True only as "the end level is 6.6% lower". The growth itself is about one fifth smaller for income. Say which you mean. |
| "Shares sum to 1 (±0.001)" build assertion and test | method §3.4, §3.8b | a check | Cannot fail by construction (telescoping differences) | ~ | Replace it with the non-trivial checks in §1. |

### 2.5 DWA (ECB / Banque de France) cross-check

Recomputed from `data/raw/dwa/DWA_FR_NWA.csv` (Q4 values) and raw `shwealj992` by an
independent script. Every cell of the `docs/notes/dwa.md` §4 table (2009–2024) matches
within 0.05 pt, apart from the 2025 middle-40% cell. The six rows of the §5 totals table
match to €0.1 bn and 0.001 in the ratio. The `france.json` `comparison` entries equal the
raw Q4 published shares (difference ≤ 1e-16) and raw `shwealj992` exactly. Years align
(DWA Q4 of Y against WID Y, no off-by-one, no duplicate years).

| Claim | Where | Claimed | Recomputed | Match | Comment |
|---|---|---|---|---|---|
| Checks: B50 + D6..D10 = total; D10 from levels against T10 ≤ 0.07 pt (largest 2018-Q2); D6 threshold = median 140.27k against 140,231 | dwa.md §1 | as stated | relative error 2e-9; 0.0665 pt at 2018-Q2; 140.27k against 140,230.62 | ✔ | |
| Households and population frozen from 2023-Q3 | dwa.md §1 | 31.86 M; 68.59 M | 31.865 M; 68.584 M | ✔ / ~ | 68.584 rounds to 68.58. |
| 1.66 adults per household (52.96 M ÷ 31.86 M); 10% = 3.2 M households / 5.3 M adults | dwa.md §3 | as stated | 1.66; 3.19 M / 5.30 M | ✔ | |
| §4 table 2009–2024 (top 10, top 5, p90–95, B50, M40; DWA / WID / gap) | dwa.md §4 | 9 rows × 12 values | all within 0.05 pt (e.g. 2024: 54.45 / 59.88 / −5.43; 40.66 / 47.50 / −6.84; 13.79 / 12.38; 5.00 / 4.84 / +0.16; 40.57 / 35.29) | ✔ | |
| §4 2025 middle 40% (DWA) | dwa.md §4 | 40.6 | **40.36** | ✘ | Appears to be copied from 2024. |
| Top-10% change 2009–2024 | dwa.md §4 | DWA +3.4, WID +3.2 | +3.42, +3.23 | ✔ | |
| Top-5% change 2009–2024 | dwa.md §4 | +3.0, +4.0 | +3.02, +3.99 | ✔ | |
| B50 within 0.61 pt, all years 2009–2024 | dwa.md §4 | 0.61 | 0.61 (2014) | ✔ | |
| Top-10% gap range, every year 2009–2024 | dwa.md §4 | 4.8–7.2 | 4.77 (2020) – 7.20 (2010) | ✔ | The low end comes from 2020, which is not in the table. |
| Top-5% gap range | dwa.md §4 | 5.8–7.6 | 5.76 (2020) – 7.59 (2010) | ✔ | |
| p90–95: DWA higher | dwa.md §4 | 0.25–1.41 | 0.25 (2009) – 1.41 (2024) | ✔ | |
| Middle 40% "about 41% vs about 35%" | dwa.md §4 | ~41 / ~35 | DWA 40.45–43.99, WID 35.29–38.00 | ~ | Holds only from about 2014. |
| B50 2009 → 2014: DWA 5.0 → 5.6, WID 5.3 → 5.0 | dwa.md §4 | as stated | 4.99 → 5.60; 5.35 → 4.99 | ✔ | WID's path is not monotonic. |
| WID 2010 jump +1.7 pt, DWA flat | dwa.md §4 | as stated | +1.69; DWA +0.11 | ✔ | |
| WID top 5% from `gp` "matches raw p95p100 exactly" | dwa.md §4 | exact | gp sum differs from the raw share by up to 0.005 pt | ~ | The build reads `share.p95p100` directly, so the sentence describes a method that is not used. |
| §5 totals (DWA 8,550 … 13,841 €bn; WID 11,151 … 14,657; ratio 0.976 … 0.955) | dwa.md §5 | 6 rows | all match | ✔ | |
| "DWA total is 0.7–4.5% below WID's" | dwa.md §5 | 0.7–4.5% below | True for the 6 years shown. **For all years 2009–2024 the range is 0.37% *above* (2010) to 4.46% below (2024).** | ✘ | Generalises from the years shown. The lowest ratio is 2024 (0.955), not 2014. |
| Q4 against four-quarter mean ≤ 0.43 pt (2020) | dwa.md §1 | 0.43 | 0.43 (2020) | ✔ | |
| 2022 drop 54.5 → 53.4; total net wealth +0.8% | dwa.md §6 | as stated | 54.53 → 53.44; +0.77% | ✔ | |
| F5 €1,972 bn → €1,823 bn (−7.6%); F511 €330 bn → €286 bn (−13.2%) | dwa.md §6 | as stated | **No F5 or F511 series in the local CSV**; the arithmetic is consistent (−7.56%, −13.33%) | unverifiable | The raw extract is not archived. |
| §3.8d: B50 "within 0.6 pt 2009–2024" | method §3.8d | 0.6 | 0.61 | ✔ | |
| §3.8d: "WID 5–7 pts above ECB/BdF every year" (top 10% / top 5%) | method §3.8d | 5–7 | top 10%: 4.77–7.20; **top 5%: 5.76–7.59** (above 7 in 2010, 2011, 2018 and 2022) | ✘ | Fits neither group exactly, and fails clearly for the top 5%. |
| Page: "WID puts 5–7 points more in the top 5% than the ECB accounts in every year since 2009" | `site/index.html` cc-notes | 5–7 | **5.76–7.59** | ✘ | Published-page error. |
| Page: B50 "about 5% in WID and in the ECB / Banque de France accounts" | cc-notes | ~5% | WID 4.74–5.35, DWA 4.87–5.60 | ✔ | |
| "quintiles" among the published groups | dwa.md §1 | – | none in the downloaded data | n/a | Cannot be checked locally. |

### 2.6 INSEE (ERFS, CND, HVP) and IPP

These were recomputed from `data/raw/insee/*.xlsx` (parsed with zipfile and ElementTree), raw WID and `data/manual/ipp_top_income.csv`.
Scripts: `.../scratchpad/audit/insee/{xlsx,dump_all,wid_extract,insee_recompute,hvp_recompute,ipp_check,ipp_levels,comparison_check,erfs_consistency}.py`.

These reproduce exactly and are not listed row by row:
- every cell of the ERFS vs WID table in `insee.md` §4 (17 rows × 11 columns) and its growth rates;
- the CND 2019 / 2022 / 2023 tables;
- the HVP tables;
- every INSEE value in `france.json` `comparison`;
- all eight IPP shares (derived as n × mean / (N × mean_all) where the CSV gives means).

| Claim | Where | Claimed | Recomputed | Match | Comment |
|---|---|---|---|---|---|
| Income after tax: WID "within 1–2 pts of INSEE ERFS" | method §3.8d; page cc-notes ("within about one to two points") | ≤ 2 pt | Top-10% gap is **3.18 (1996), 3.30 (1997), 3.00 (1998), 2.0–2.4 (2000–04)** and 3.79 in 1990 (plotted). The bottom 50% is ≤ 1.7. | ✘ | The claim holds from 2005 on. |
| "Opposite trends 1996–2018" | §3.8d; cc-notes | opposite | Top 10%: ERFS +2.3 against WID −1.8. Bottom 50%: −0.7 against +1.9. | ✔ end to end | The span crosses two ERFS breaks and ends on ERFS's 2018 spike (24.8, against 23.9 in 2017 and 2019). Over 2012²–2018 the bottom 50% moves the same way in both. |
| CND 2019 bottom 50% 38% vs WID 32% | §3.8d; cc-notes | 38 / 32 | 38.25 / 32.13 | ✔ | WID 2019 is already extrapolated (`data_quality` 4); 2018 gives 31.9. |
| "because WID allocates health/education/collective spending in proportion to income" | §3.8d; cc-notes (stated as fact) | cause | `insee.md` itself calls this unverified and lists other causes, such as CND concentration shares without re-ranking. The current WID metadata for `sdiincj992` does say "Education is distributed proportionally to posttax disposable income" (checked locally). | ~ | Partly supported by the metadata, for education only. Present it as a likely cause, not the cause. |
| Wealth B50: INSEE survey higher, 6–8% | §3.8d | 6–8 | 6.2–8 | ✔ | |
| Wealth top 10% / 5%: survey "far lower" | §3.8d | – | top 10% 46–49 against 57–60; top 5% 33–34 against 46–47 | ✔ | |
| "INSEE's survey shows a much smaller top 1%" | cc-notes | – | 15–16 against 26.1–27.7 | ✔ | |
| IPP: WID column | `france.json` `ipp_top_income` | j992 2016 | `sptincj992` 2016 exactly. `sptinci992` and `sptinct992` end in 2014. | ✔ | IPP's unit is the foyer fiscal (tax household). WID's tax-unit series (t992) runs 13–17% above j992 at the top in 2014, but has no 2016 value. |
| "WID's shares match IPP's taxable income almost exactly" | page ipp-summary; §3.8d | ≈ | Share ratios 0.97 / 0.95 / 1.00 / 0.97 | ✔ as shares | The shares are of different totals: WID pre-tax national income 2016 is €1,913 bn nominal, IPP taxable income €999 bn. Units also differ (foyers against equal-split adults). State both next to the table. |
| "about 4 times WID's 0.48%" (top 0.001%, 2025 paper) | page ipp-summary | 4× | 0.0197 / 0.0048 = 4.10 | ✔ arithmetic | A euro-level comparison is not cleaner: the groups differ in size (378k foyers against 507k adults for the top 1%) and in income concept. |
| "1.3× to 4× larger … 2.0% (2025 paper) or 5.1% (revised 2023 note) vs WID 0.5%" | §3.8d | 1.3–4× | 2025 paper 1.33–4.10×; 2023 note 1.65–**10.6×** | ✘ | Internally inconsistent. |
| GGP 2014 top 1 / 0.1 / 0.01 / 0.001% wealth against current WID | `top_wealth_estimates.csv`; §3.8d (top 0.001% only) | 23.4 / 8.2 / 2.8 / 0.9 | current WID 25.79 / 11.23 / 5.44 / 3.39 | n/a | The differences against GGP are +2.4, +3.0, +2.6 and +2.5 pt. By layer, almost all of it sits in the top bin: 99.9–99.99 +0.4 pt, 99.99–99.999 +0.15 pt, top 0.001% +2.5 pt. A +2.5 pt top-bin change is larger than the most a Forbes top-up could add (1.75 pt in 2014), which supports §2.3: the vintage change is not only the top-up. |
| CND total "within 2%" of WID | `insee.md` §3 | < 2% | +2.18% | ✘ (minor) | |
| 2023 "net national income" €2,083 bn | `insee.md` §2 | 2,083 | 2,083.1 is IA118 row 14, *revenu primaire élargi*. Net national income is **€2,369.9 bn** (row 16). | ✘ | As written, the series implies national income fell in 2023. |
| Top 10% "23–26% in both sources every year"; B50 "30–33%" | `insee.md` §4 | 23–26 / 30–33 | 22.5–26 / 29.8–33 | ✘ (minor) | |
| "Each break … lifts the top" | `insee.md` §4 | both | 2010 break +0.4 pt; 2012 break −0.1 pt | ✘ (minor) | |
| HVP dots 1998–2010 against 2015–2024 | `comparison.wealth_*` | one series "gross wealth" | 1998–2010 are *hors reste* (old method, metropolitan France); 2015–2024 are IF371 integers *including* residual assets. Like for like, the 2015 B50 is 6.7 against 8 plotted. | ✘ | The visible jump is mostly a change of concept. |
| 1975–2024 INSEE file against IG1 | `insee.md` §1 | consistent | 2023 matches; **2005 differs** (S20 9.1 against 9.0; S80/S20 4.18 against 4.22) | ~ | |
| `ipp_top_income.csv` note "~530 adults" (2016) | manual CSV | 530 | 507 (50.70 M adults in 2016) | ✘ (minor) | |
| Chart tooltip on years with two ERFS values (1996, 2010, 2012, 2020) | page `lineChart` | – | `indexOf` returns the first, older-method value (2020: 23.6 against 23.1 on the new chain) | ✘ (minor) | Code defect. |

### 2.7 Prices, pre-committed spending and housing

These were recomputed from `data/raw/prices/*`, `data/raw/housing/*`, `data/raw/insee_hpi.xml` and the manual CSVs.
Scripts: `.../scratchpad/audit/prices/{auditlib,cpi_audit,growth_cpi_audit,housing_audit,precommit_spatial_audit,misc_audit,rounding_check,borderline_quality}.py`.

| Claim | Where | Claimed | Recomputed | Match | Comment |
|---|---|---|---|---|---|
| CPI by income group, 1998–2024: +54.9% / +53.0% / +50.8% | method §3.8c; page prices-note (generated) | as stated | +54.88 / +52.99 / +50.80. Mean of the indices and mean of the ratios agree to 0.01 pt. | ✔ | Groups are household *niveau de vie* deciles 1–5, 6–9 and 10, not WID adult layers. |
| "per-layer deflator would change real growth by at most ~3%" | method §3.8c | ~3% | −3.16% (B50), −1.96% (M40), −0.54% (top 10) against the WID deflator | ✔ (≈3.2%) | Holds only for 1998–2024. |
| CPI splice at 1990 (long coefficient against the base-2025 index) | `france.json` `cpi_all` | – | ratio 1.000099; no step | ✔ | |
| CPI and deflator equal 1 in 2025 | json | 1 / 1 | 1.0 / 1.0 | ✔ | INSEE's long coefficient has two decimals, so the CPI is ±0.11% in 1950 and ±17% in 1901. Clipping at 1950 is justified, but see the 1950 step in §2.4. |
| Pre-committed share, 1959 → 2025 | page prices-note (generated) | 13.4% → 30.3% | 13.38% → 30.33% (`insee_t_2103`) | ✔ | |
| Pre-committed share table (12 years) and housing-related share | prices-housing.md §1.2 | 13.5 … 30.3; 10.7 … 23.1 | all match | ✔ | |
| "about 30% of household disposable income" | concepts §1.2 | ~30% | 29.5–30.6% since 2010 | ✔ | |
| Base 2014 below base 2020 "about 1–1.5 pt" | prices-housing.md §1.2 | 1–1.5 | 0.52–1.55 pt | ~ | |
| DREES 2011: 61% (poor) against 23% (affluent) | page prices-note (static) | 61 / 23 | manual CSV 61 / 23 | ✔ vs CSV | External publication. |
| "Prices about 7% higher in the Paris region" | page limits; concepts §1.2 | 7% (2022) | 7.2% Fisher (IP1959, 2022) | ✔ | The area is the Paris *urban unit*, not Île-de-France, and the figure includes rents. The 2015 edition gave 8.8%. |
| Paris price/m² levels and DVF back-casts (1996 … 2025) | prices-housing.md §1.3 | 2,415 … 9,580; 2,528 … 10,033; 1,047 … 3,288 | all match; JSON within €0.5 | ✔ | |
| DVF Paris mean over Notaires level | prices-housing.md | 1.9% (2021) – 4.7% (2025) | 1.92 – 4.73% | ✔ | |
| Housing-years table (16 cells) and "23 years in 2024 vs 12 in 1996" | prices-housing.md §3(iii) | 12.2 … 23.4 | Arithmetic matches **only with post-tax income (`diinc`), the DVF Paris level and p90p100**. On the page's basis (pre-tax income, Notaires level, p90p99), a 70 m² flat in Paris costs the bottom 50% **34.75 years in 2024 against 16.6 in 1996** | ✘ | The notes describe a different chart from the one published. |
| Page housing years, Paris (B50 / M40 / 90–99 / top 1%) | page (generated from json) | – | 1991: 25.4 / 9.5 / 4.6 / 1.2. 2000: 17.3 / 6.2 / 2.9 / 0.63. 2010: 33.8 / 11.9 / 5.4 / 1.24. 2020: 48.1 / 17.3 / 7.8 / 1.77. 2024: 34.75 / 12.4 / 5.7 / 1.19 | ✔ | Within 0.02% of the raw recomputation. Deflator rounding in the JSON is ≤ 0.001% here. |
| Page housing years, rest of France | page | – | 1995: 7.3 / 2.6 / 1.3 / 0.34. 2024: 11.9 / 4.2 / 2.0 / 0.41 | ✔ | |
| "at the average price of existing flats" | page housing caption | existing flats | Paris uses a quality-constant Notaires level. The rest of France uses a DVF mean that includes off-plan sales, at the 2025 mix. | ✘ | The two charts are on different bases. The DVF Paris mean is 4.7% above Notaires in 2025. |
| "Rest of France" coverage | page | outside the Paris region | Metropolitan France minus the 8 Île-de-France départements. Alsace-Moselle is missing from DVF but is inside the INSEE Province index. | ~ | |
| 2025 prices drawn | page | – | `ptinc` ends in 2024, so the DVF anchor year (2025) is never drawn | ~ | |
| HPI annual means (1996, 2000, 2010, 2015, 2024, 2025) | `france.json.hpi` | 41.55 … 126.97 | match; 2025 has 4 quarters | ✔ | The series is the **CVS** (seasonally adjusted) one, while the notes call it raw. The page never reads `hpi` (see §2.4). |
| `diinc` extrapolated "after 2019" | prices-housing.md §3(iii) | after 2019 | `data_quality` drops to 4 **in** 2019 | ✘ | Off by one. The page's "after 2018" is correct. |
| Notes §4 decile growth D8–D9; CPI/WID ratio 1996–2024 | prices-housing.md §4 | +52.9; 1.022 | +52.85; 1.0225 | ✘ (rounding) | |
| Tobacco index ×3.4, 2003–2024 | prices-housing.md §4 | 3.4× | series 011814410 is not in any downloaded file | unverifiable | This contradicts the note's "Every number below was recomputed from the downloaded files". |
| 011818265 (Q1 excluding tobacco, base 2025) start | prices-housing.md §1.1 | 2015– | 2011– | ✘ | |

## 3. Discrepancies and bugs, ranked

**Critical: none.** No headline number on the page is wrong. The JSON is a faithful copy
of WID, and the layer, transfer, top-tail and scenario arithmetic all reproduce
independently.

### Major

**M-1. The CPI price option introduces a 6.4% step in every real level between 1949 and 1950.** (`site/index.html` `priceFactor`; method §3.8c)
- `priceFactor` returns 1 before 1950 and defl / cpi = 1.0644 from 1950. In 1949 the
  factor would be 1.0645, so the step is purely an artefact.
- With "Consumer prices" selected, it contaminates the levels chart, transfers in
  end-year euros, and the GIC for any start year before 1950.
- Fix: hold the factor at its 1950 value for earlier years (chain-link), or disable the CPI
  option for spans that cross 1950.

**M-2. The housing text describes charts that do not exist, and the notes' headline describes a different chart from the one published.**
- Page method item 7 and method §3.8 describe an HPI ÷ post-tax-income affordability
  index. The page draws years of *pre-tax* income from price *levels*, and
  `france.json.hpi` is never read.
- `prices-housing.md` §3(iii) says a 70 m² flat in Paris costs the bottom 50% "23 years in
  2024 vs 12 in 1996" (post-tax income, DVF-anchored Paris level, p90p100). On the page's
  basis (pre-tax, Notaires level, p90p99) it is **34.75 vs 16.6 years**.
- The Paris chart uses Notaires' quality-constant level. The rest-of-France chart uses a
  DVF mean that includes off-plan sales, at the 2025 mix. The caption "average price of
  existing flats" fits neither exactly. DVF Paris is 4.7% above Notaires in 2025.
- Fix:
  - Rewrite item 7 and §3.8, and drop or use `hpi`.
  - Recompute the notes table on the page's basis.
  - Put both charts on one price basis, or state the difference.

**M-3. Two published cross-check sentences state ranges that the data contradict.**
- (a) Page cc-notes and method §3.8d say "WID puts 5–7 points more in the top 5% than
  the ECB accounts in every year since 2009". The actual gap is **5.76–7.59 pt**, above 7
  in 2010, 2011, 2018 and 2022. "5–7" is roughly the top-10% range (4.77–7.20).
- (b) Page cc-notes and §3.8d say WID income after tax is "within about one to two
  points" of INSEE ERFS. The top-10% gap is **3.0–3.3 pt in 1996–1998**, 2.0–2.4 pt in
  2000–2004, and 3.8 pt in 1990, which is plotted.
- Fix:
  - (a) "about 6 to 7.5 points" for the top 5%.
  - (b) "within 2 points since 2005, about 3 in the late 1990s".

**M-4. The GIC summary sentence on the bottom half is misleading on the default view.**
- The generated "the bottom-half groups averaged X% a year" is an unweighted mean of
  g-percentile growth rates over the groups that survive the near-zero filter.
- For wealth 1980 → 2024 it prints **+0.02%/yr**. Under the more natural reading of the
  spec (1% of *each year's* mean, which drops p0–p12 instead of p0–p6), it would be
  **+0.51%/yr**. The bottom-50% layer's own average grew **+1.09%/yr** (€16,646 →
  €26,792).
- The code's filter `0.01 × min(mean0, mean1)` is a defensible reading of "1% of the
  overall mean in either year", but the summary is too sensitive to it.
- For 1950 → 2024 the filter keeps groups from €171, whose growth is computed from
  near-zero bases.
- WID's 1980 bottom g-percentiles are evenly spaced (984, 1,967, 2,951, … €), which looks
  interpolated.
- Fix:
  - Report the bottom-50% layer's average growth, or a population-weighted figure.
  - Make the filter rule explicit in the doc and in the code.

### Minor

- **m-1. Rich-list scenarios use k = 1 adult per family without GGP's marriage assumption.**
  - Method §3.7 says k = 1, 10 and 15 are "the values Garbinti et al. use". GGP pair them
    with 80% of members married, and under WID's equal split a married fortune belongs to
    two adults.
  - At k = 1.8 the 2024 top-0.001% share is **6.46%** (c = 20%) and **8.07%** (c = 0),
    against 6.95% and 8.64% at k = 1. So k explains about 0.5–0.6 pt; most of the scenario
    effect comes from the size of the Challenges total.
  - Fix: state the marriage assumption and either use k ≈ 1.8 or label k = 1 as ignoring
    couples.
- **m-2. IPP comparison wording.**
  - Method §3.8d's "1.3× to 4× larger" contradicts its own 5.1% example, which is 10.6×
    WID's 0.48%. Write "1.3–4.1× (2025 paper), 1.7–10.6× (2023 note)".
  - "WID's shares match IPP's taxable income almost exactly" is true of shares only. The
    denominators are €1,913 bn (WID pre-tax national income 2016, nominal) and €999 bn
    (IPP taxable income).
  - Group sizes also differ: the top 1% of 37.8 M foyers is 378k units; the top 1% of
    50.7 M adults is 507k. So no level comparison is clean either.
  - Fix: name the denominators and units next to the table.
- **m-3. "The two largest one-year jumps of the top-0.001% share (2014 and 2021)".**
  (method §3.5; page limits list)
  - Over the full series this is false: 1998→99 (+1.18 pt) is larger than 2013→14
    (+1.00 pt), and 2014 is the third-largest rise.
  - It is true only from 2000 on. State the period, and discuss the unexplained 1999 jump.
- **m-4. `dwa.md` errors.**
  - §5 "DWA total is 0.7–4.5% below WID's" holds for the six years shown only. Over
    2009–2024 the range is 0.37% *above* (2010) to 4.46% below.
  - §4: the 2025 middle-40% value of 40.6 should be 40.4 (it was copied from 2024).
  - Middle 40% "about 41% vs about 35%" holds only from about 2014.
- **m-5. Method §3.7 table.**
  - Forbes 2005 (€73 bn) is an unflagged lower bound; the page drops it.
  - Forbes 2019 (€343 bn) is missing ("–").
  - The "Spread" scenario is documented but not selectable on the page.
- **m-6. "Upper bound: 26 years (1997–2024)"**, in the docs and in the page's scenario
  note. 1999 and 2003 are not corrected, so the scenario series has holes. Write "26 of
  the 28 years 1997–2024" or list them.
- **m-7. Tile against smoothing.**
  - The 1980 tile always shows 0.80%. The pie summary shows 0.74% with the 3-year average
    on.
  - Smoothing is asymmetric: the last year is never averaged, so the smoothed 1980 → 2024
    transfer is €709 bn against €701 bn.
  - Fix: apply the toggle to the tiles, or label the tiles as unsmoothed.
- **m-8. Start-year noise.**
  - 1980 is a local spike for the top 0.001% (1979 0.73%, 1980 0.80%, 1981 0.69%).
  - The 1970s top bin is erratic (1975 0.24%, 1976 0.83%).
  - The €701 bn headline becomes €711 bn (1979 start, +1.5%), €717 bn (1981, +2.3%) and
    €783 bn (1975).
- **m-9. The shares-sum-to-1 test cannot fail by construction** (build assertion and test,
  method §3.4 / §3.8b). Replace it with: g-percentile shares sum to 1; share-derived
  averages ≈ WID `a` variables; layer averages ≈ g-percentile aggregates.
- **m-10. Top-up and vintage attribution.**
  - Docs and page imply the top-bin discontinuity and the Forbes top-up are post-2014
    features. The ratio t(p99.999) / a(p99.998–999) is already 2.4 in 1988 and 3.0 in
    1999.
  - GGP 2014 to the current vintage: the top bin rose +2.5 pt, more than any Forbes
    top-up could add (≤ 1.75 pt, Forbes 2014 = 1.75% of wealth). The layers just below
    barely moved (+0.4 and +0.15 pt).
  - Say that the vintage change is not only the top-up.
- **m-11. Wealth composition.** The series `ahw{hou,bus,fin,deb}j992` do not add up to
  current group net wealth: −23% for the top 10% and −40% for the top 0.1% in 2014, while
  the macro identity holds. The housing-share chart for top groups rests on an
  inconsistent component vintage. Say so on the chart.
- **m-12. Price base.** "Constant 2025 euros" relies on the IMF WEO *projection* for the
  2025 deflator (WID metadata). It will shift on revision.
- **m-13. "Real growth since 1980 is about 6% smaller with the CPI."** The 2024 / 1980
  level ratio is 6.6% lower. The growth itself is about 20% smaller (income +51% against
  +41%). Reword.
- **m-14. WID-internal inconsistency.** WID's own `ahwealj992 p50p90` is 3.6–6.7% below the
  share- and g-percentile-consistent value after 2008. The project is unaffected because
  it derives averages from shares. Do not switch to reading `a` variables for
  intermediate groups.
- **m-15. INSEE cross-check presentation.**
  - The HVP dots change concept between 2010 (*hors reste*) and 2015 (IF371, including
    residual assets, integers) with no visual break. The visible jump in the bottom 50% is
    mostly the change of concept: like for like, 2015 is 6.7 against 8 plotted.
  - `insee.md` §2 calls €2,083 bn "net national income" for 2023. That is *revenu
    primaire élargi*; net national income is €2,370 bn.
  - The tooltip shows the older-method ERFS value in break years.
  - The "because WID allocates public spending in proportion to income" explanation is
    stated as fact. WID metadata confirms it for education only.
- **m-16. Small text errors.**
  - `insee.md` §3 "within 2%": actually 2.18%.
  - `insee.md` §4 ranges: 23–26% should be 22.5–26%; 30–33% should be 29.8–33%.
  - "each break lifts the top": the 2012 break lowers it.
  - `prices-housing.md` "`diinc` extrapolated after 2019": it is from 2019.
  - D8–D9 decile CPI growth: +52.9 should be +52.8.
  - 011818265 starts in 2011, not 2015.
  - The base-2014 gap is 0.5–1.55 pt, not 1–1.5.
  - The `hpi` series is CVS, not raw.
  - The tobacco ×3.4 figure and the F5 / F511 figures in `dwa.md` §6 are not in any
    downloaded file.
  - `ipp_top_income.csv` note: ~530 adults in 2016 should be ~507.
- **m-17. README layer coverage.** README says the layers cover 1900–2024. Post-tax income
  covers only 1980–2024; pre-tax income has no annual data for 1901–1909 and 1911–1914.
- **m-18. Timing.**
  - Forbes values fortunes in early March but is converted at the annual-average €/$ rate
    (under 1% in 2024).
  - Challenges (July list, valuation date unknown) and HVP (wealth at the start of year Y)
    are paired with WID year Y with no timing note.
- **m-19. CPI toggle scope.** The top-tail chart and the billionaire tile ignore the CPI
  toggle without saying so.

## 4. Year alignment, duplicates and splices (check 4)

- **No duplicated keys:** none in the raw WID file (1,616,784 rows). No duplicated years in
  any `france.json` series. ERFS break years carry two values by design, as separate
  series.
- **Forbes list year Y against WID year Y:** consistent with WID's own top-up. The WID
  share jumps in 2014 and 2021 coincide with the Forbes 2014 and 2021 list jumps, so WID
  uses the April-Y list for year Y.
- **Challenges July Y against WID Y:** no shift is applied. That is acceptable, given the
  unknown valuation date.
- **DWA Q4 of Y against WID Y:** correct. A one-year shift would change the gaps by up to
  1.3 pt.
- **Splices:**
  - CPI at 1990: no step.
  - CPI option at 1950: 6.4% step (M-1).
  - ERFS breaks: kept separate, as documented.
  - HVP 2010 / 2015: concept change not shown (m-15).
  - Rich-list scenarios: years 1996, 1999 and 2003 stay on WID inside the 1997–2024 run
    (m-6).
- **Units and price base:**
  - Everything shown in euros is in constant 2025 euros through `inyixxi999`. Nominal
    Challenges, Forbes, and Paris and DVF prices are converted with it.
  - Forbes is converted with `xlcusxi999` first.
  - No nominal value is compared with a real one without conversion.
  - The JSON deflator is rounded to 5 decimals: harmless after 1950 (≤ 0.003%), up to 1.3%
    in 1900. Nothing nominal is deflated before 1950 at present.
