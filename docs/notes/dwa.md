# ECB Distributional Wealth Accounts (DWA): a cross-check for WID's wealth shares

Purpose: an independent estimate of how French household net wealth is split,
set beside the WID.world backbone. Script: `pipeline/sources/dwa.py` (standard
library only). It downloads one CSV from the ECB Data Portal and returns annual
(Q4) series. Last checked 2026-10-16. The data vintage ends in 2026-Q1.

```bash
python3 -I pipeline/sources/dwa.py data/raw     # writes data/raw/dwa/DWA_FR_NWA.csv
```

## 1. What DWA measure

- **Producer.** The European System of Central Banks. The ECB first published
  them on 8 January 2024 as **experimental statistics**, which "comply with
  many, but not all, of the quality requirements of official ECB statistics"
  [1]. France, like Austria, Germany, Italy and the Netherlands, compiles its
  own series with the common method; the ECB compiles the others centrally
  [2]. The Banque de France publishes the same series on Webstat as *Comptes
  distributionnels de patrimoine des ménages – séries France (DWA1)* [3].
- **Frequency.** Quarterly, published about five months after the quarter ends
  [1]. France starts in 2009-Q4.
- **Unit.** The **household**. Groups are ranked by household net wealth.
- **Wealth concept.** Deposits, debt securities, listed shares, unlisted
  shares and other equity, investment fund shares, life insurance and
  voluntary pensions, housing, and non-financial business assets, minus
  mortgages and other loans. The concept **excludes** pension entitlements
  (compulsory schemes and occupational schemes), durables and valuables,
  currency, derivatives, and other accounts receivable or payable. The
  Banque de France puts the coverage at about 90% of the household balance
  sheet, the gap being mostly occupational pensions [3]. The ECB table for
  the euro area gives 93% of assets and 88% of liabilities [2].
- **Prices.** Current euros, not deflated [1][3].
- **Published groups.** Bottom 50%, deciles 6–10, and quintiles. Shares are
  published for the bottom 50%, top 10% and top 5%. There is **nothing finer
  than the top 5%**: the Banque de France says the data "ne permettent pas
  pour le moment d'aller plus finement que le top 10 % ou le top 5 %" [3].

### Series used (key `DWA.Q.FR.S14.…`, net wealth `NWA`)

| Series | Content | Scale (`UNIT_MULT`) |
|---|---|---|
| `N.LE.NWA._Z.EUR` | Total net wealth of households | € millions |
| `N.LE.NWA._Z.EUR_R_NH` / `EUR_R_POP` | Per household / per capita | € thousands |
| `N.LE.NWA._Z.EUR_MN` / `EUR_MD` | Mean / median per household | € |
| `N.LE.NWA.{B50,D6..D10}.EUR` | Group total | € millions |
| `N.LE.NWA.{B50,D6..D10}.EUR_R_NH` | Mean per household within the group | € thousands |
| `N.LE.NWA.{D6..D10}.EUR_T` | Lower threshold of the decile (D6 = median, D10 = P90) | € thousands |
| `_Z._Z.NWA.{B50,T10,T5}.PT` | Share of net wealth | % |
| `_Z._Z.NWA._Z.GI` | Gini coefficient | % |

These series are all requested in a single API call:
`https://data-api.ecb.europa.eu/service/data/DWA/Q.FR.S14.N+_Z.LE+_Z.NWA.B50+D6+D7+D8+D9+D10+T10+T5+_Z.EUR+EUR_R_NH+EUR_R_POP+EUR_MN+EUR_MD+EUR_T+PT+GI.S.N?format=csvdata`.
The dimension order comes from the data structure `ECB_DWA1`.

Checks run on this vintage:

- The bottom 50% plus D6–D10 sum to 100% of the total in every quarter.
- The D10 share computed from levels matches the published T10 share within
  0.07 percentage points (largest gap: 2018-Q2).
- The D6 threshold equals the median: 140.27k against 140,231 € in 2009-Q4.

### Choices made in `dwa.py`

- **Annual value = Q4.** DWA are closing stocks (`STO = LE`), so Q4 is the
  position at 31 December. The series also starts in 2009-Q4, so an annual
  mean cannot be computed for 2009. The cost of this choice is small: the
  largest gap between the Q4 top-10% share and its four-quarter mean is 0.43
  percentage points (2020). Years without a Q4 value are dropped; 2026 has
  only Q1.
- **Shares are fractions**, as in `site/data/france.json`:
  - `bottom50`, `top10` and `top5` are the published series.
  - `D6`–`D10`, `middle40` (D6+…+D9) and `p90p95` (top10 − top5) are derived.
- **Households and population are derived.** DWA publish neither, so the
  script computes total ÷ per-household value and total ÷ per-capita value.
  **Both are frozen from 2023-Q3**, the reference quarter of the last survey
  wave: 31.86 million households and 68.59 million people. Per-household
  levels after that date therefore move only with the totals.
- **All money is nominal euros.**

## 2. Method

Steps of the common method, following the ECB methodological note [2],
Engel, Gayà Riera, Grilli & Sola (2022) [4], and the Banque de France
note [3]:

1. **Survey.** For France the source is the HFCS, fed by the INSEE and Banque
   de France survey *Histoire de vie et Patrimoine*. Five waves are used,
   anchored to the quarter nearest the middle of fieldwork: **2009-Q4,
   2014-Q4, 2017-Q4, 2021-Q1 and 2023-Q3** [3].
2. **Population and instrument adjustments.**
   - Household weights are scaled up proportionally to the national-accounts
     household count, which includes people living in institutions.
   - Housing and business assets are matched to the national accounts.
   - The split of debt is estimated from bank statistics.
   - Managed accounts are reallocated.
   - Deposits are corrected for under-reporting [3].
3. **Missing rich.** This is the second-largest adjustment, after the final
   calibration [2].
   - **Rich list.** Households from a list of rich French families are added.
     The list comes from press rankings and is adjusted for:
     - the number of households per family, estimated from the FIBEN, LIFI
       and INPI shareholder data, and set to **4 households per family** when
       no estimate was possible;
     - the country of residence;
     - valuation differences from ESA 2010.
     Only entries above the richest survey household are kept [3].
   - **Which list.** The Banque de France note does not name the list. ECB
     Working Paper 2687, Table 1, gives France's list as **"Challenges
     (504)"**: 504 observations at the time of the **third** HFCS wave [4].
     That the same list is used for every wave is likely but not stated in
     either source.
   - **Pareto tail.** A Pareto law is fitted on the survey plus the rich list
     above **w0 = €1 million**, following Vermeulen. For France, synthetic
     households are drawn in two intervals only: from the first
     discontinuity in the survey's tail (w10) up to the richest survey
     household (w11), and from there up to the poorest list entry (w12).
     No synthetic households are drawn above w12, because the list is judged
     dense enough there [3].
   - **Portfolios of the added households** come from the 2018 Global Family
     Office Report, IPP report no. 36 and administrative data. The results
     were checked against IPP's ISF study (October 2021) [3].
4. **Calibration.** After step 3, the survey covers only **65–76%** of
   national-accounts net wealth, depending on the wave [3]:

   | Wave | Coverage |
   |---|---|
   | 2009-Q4 | 75.9% |
   | 2014-Q4 | 65.4% |
   | 2017-Q4 | 76.3% |
   | 2021-Q1 | 67.6% |
   | 2023-Q3 | 73.4% |

   Each instrument is then scaled proportionally to its national-accounts
   total. This keeps each instrument's Gini and every household's rank within
   that instrument [3][4].
5. **Quarterly series.** Between waves, values are linearly interpolated per
   decile and per instrument, then re-aligned to the quarterly accounts.
   After the last wave, values are extrapolated with no assumed change in
   portfolios; they move only through the prices and totals of each
   instrument [3][4].
   - The ECB warns that quarters after the latest wave are estimates and will
     be revised when the next HFCS wave is released [1].
   - Shocks between waves, such as COVID-19, show up only through
     aggregate totals, not through portfolio changes [4].

## 3. DWA vs WID: units and concepts

| | DWA | WID (our backbone) |
|---|---|---|
| Unit ranked | Household | Adult aged 20+, wealth split equally within couples |
| Group size | 10% of **households** (about 3.2m in 2024) | 10% of **adults** (about 5.3m in 2024) |
| Wealth concept | Excludes pension entitlements, currency and valuables (about 90% of the balance sheet) | Net personal wealth of the household sector in the national accounts |
| Top tail | Survey plus a press rich list (Challenges, per WP 2687 for wave 3), Pareto tail above €1m, proportional calibration | Capitalized income-tax data plus surveys (GGP 2021) to 2014; from 2014, fixed-portfolio extrapolation plus a Forbes top-up of the top g-percentile ([rich-lists.md](rich-lists.md)) |
| Real anchors after 2014 | Survey waves 2017, 2021, 2023 | None: `data_quality` is 4 up to 2014 and 0 from 2015 in `WID_data_FR.csv` |
| Prices | Nominal euros | Constant 2025 euros |

The top 10% of households is not the top 10% of adults. A rich household
typically holds a couple, and WID splits the couple's wealth in two and ranks
each adult. In 2024 France had 1.66 adults per DWA household (52.96m WID
adults ÷ 31.86m households). Which way this pushes the top shares depends on
household size along the wealth distribution. **We have not measured that, so
we do not sign the effect.**

## 4. Comparison of shares (DWA Q4 vs WID, France)

DWA: published shares, Q4. WID: `site/data/france.json`
(`concepts.hweal.share`, `concepts.hweal.layers.p50p90.share`). WID's top 5% is
computed from `concepts.hweal.gp` as the sum of bin average × bin width for
bins from p95 up, divided by the total. It matches the raw `shwealj992 p95p100`
exactly in every year shown. All values are percentages of total net wealth;
gap = DWA − WID in percentage points.

| Year | Top 10%: DWA / WID / gap | Top 5%: DWA / WID / gap | p90–95: DWA / WID | Bottom 50%: DWA / WID / gap | Middle 40%: DWA / WID |
|---|---|---|---|---|---|
| 2009 | 51.0 / 56.6 / −5.6 | 37.6 / 43.5 / −5.9 | 13.4 / 13.1 | 5.0 / 5.3 / −0.4 | 44.0 / 38.0 |
| 2010 | 51.1 / 58.3 / −7.2 | 37.7 / 45.3 / −7.6 | 13.5 / 13.1 | 5.2 / 4.7 / +0.4 | 43.7 / 36.9 |
| 2014 | 52.9 / 58.7 / −5.8 | 39.2 / 46.0 / −6.8 | 13.7 / 12.7 | 5.6 / 5.0 / +0.6 | 41.5 / 36.3 |
| 2017 | 53.2 / 58.8 / −5.6 | 39.6 / 46.1 / −6.6 | 13.7 / 12.7 | 4.9 / 5.0 / −0.0 | 41.9 / 36.2 |
| 2019 | 54.1 / 59.1 / −5.1 | 40.4 / 46.5 / −6.1 | 13.7 / 12.6 | 4.9 / 4.9 / −0.1 | 41.1 / 35.9 |
| 2021 | 54.5 / 59.7 / −5.2 | 40.9 / 47.2 / −6.3 | 13.6 / 12.5 | 5.0 / 4.9 / +0.2 | 40.4 / 35.4 |
| 2022 | 53.4 / 59.6 / −6.2 | 39.6 / 47.1 / −7.5 | 13.8 / 12.5 | 5.1 / 4.9 / +0.3 | 41.4 / 35.5 |
| 2023 | 54.2 / 59.7 / −5.4 | 40.5 / 47.3 / −6.8 | 13.8 / 12.4 | 5.0 / 4.9 / +0.2 | 40.7 / 35.4 |
| 2024 | 54.4 / 59.9 / −5.4 | 40.7 / 47.5 / −6.8 | 13.8 / 12.4 | 5.0 / 4.8 / +0.2 | 40.6 / 35.3 |
| 2025 | 54.7 / – | 40.9 / – | 13.8 / – | 5.0 / – | 40.6 / – |

(WID's France series ends in 2024.)

**What agrees:**
- The bottom 50% is close in both: about 5% of wealth, within 0.61 points in
  every year from 2009 to 2024.
- Both show the top 10% gaining over 2009–2024: +3.4 points in DWA and +3.2
  in WID.
- Both show the top 5% gaining: +3.0 points in DWA and +4.0 in WID.

**What differs:**
- **WID's top shares are higher in every year from 2009 to 2024**: by 4.8–7.2
  points for the top 10% and 5.8–7.6 points for the top 5%.
- **The whole gap sits in the top 5%.** Between p90 and p95, DWA is
  *higher* than WID by 0.25–1.41 points, a gap that has widened over time.
  Above p95, WID is higher by 5.8–7.6 points.
- **The middle 40% mirrors that gap.** It holds about 41% of wealth in DWA
  against about 35% in WID.
- **The bottom 50% moves in opposite directions over 2009–2014:** DWA rises
  from 5.0% to 5.6%, WID falls from 5.3% to 5.0%.
- **WID jumps in 2010** (top 10% +1.7 points); DWA is flat that year.

**Likely reasons.** These are sourced mechanisms; we have not quantified
them.
1. **Top-tail method.** WID uses capitalized income-tax data, which are
   exhaustive at the very top, and a Forbes top-up. DWA rely on a survey that
   is thin at the top, on Challenges families split into households (4 per
   family by default), and on a Pareto fit from €1m. A gap concentrated above
   p95 is what a weaker capture of the very top would produce.
2. **Calibration.** 24–35% of national-accounts wealth is missing from the
   corrected survey. DWA allocate it per instrument in proportion to survey
   holdings. Where the survey understates top holdings of equity and business
   assets, this allocation spreads the missing wealth too evenly.
3. **Wealth concept.** DWA leave out pension entitlements and currency. We
   have not checked which pension entitlements WID's `hweal` includes, so
   how much this contributes is unknown (see §5).
4. **Unit.** Households against equal-split adults, as in §3. The direction is
   not established.
5. **Post-2014 years.** WID's distribution is extrapolated with the 2014 asset
   mix plus the Forbes top-up; DWA have survey anchors in 2017, 2021 and 2023.
   Neither side is a direct observation after its last anchor. This bears on
   **trends only**: the level gap is already there in 2009 and 2014 (−5.6 and
   −5.8 points for the top 10%), when both sides rest on their own data.

## 5. Totals (sanity check)

WID's `mhweali999` (total net personal wealth) is in constant 2025 euros: it
equals `ahweali992` × adults. Multiplying it by the WID deflator
(`deflator` in `france.json`) gives nominal euros, comparable with DWA Q4:

| Year | DWA (€bn, nominal) | WID (€bn, constant 2025) | Deflator | WID (€bn, nominal) | DWA ÷ WID |
|---|---|---|---|---|---|
| 2009 | 8,550 | 11,151 | 0.7859 | 8,764 | 0.976 |
| 2014 | 9,669 | 12,324 | 0.8206 | 10,114 | 0.956 |
| 2017 | 10,894 | 13,292 | 0.8391 | 11,154 | 0.977 |
| 2021 | 13,669 | 15,377 | 0.8951 | 13,765 | 0.993 |
| 2023 | 13,796 | 14,869 | 0.9682 | 14,396 | 0.958 |
| 2024 | 13,841 | 14,657 | 0.9884 | 14,487 | 0.955 |

The DWA total is 0.7–4.5% below WID's. That is less than DWA's roughly 10%
narrower concept would imply if WID covered the full balance sheet, and the
ratio varies by year (0.956 in 2014, 0.993 in 2021). The source of the
difference is not established. Timing is assumed comparable: DWA is the Q4
stock, and we have not checked whether WID's annual wealth is year-end or
year-average.

## 6. Caveats

- These are experimental statistics. Quarters after 2023-Q3 will be revised
  with the next HFCS wave [1].
- Household and population counts are frozen from 2023-Q3 in this vintage.
- There are no groups above the top 5%. DWA cannot check WID's layers above
  p95: the top 1%, 0.1%, 0.01% or 0.001%.
- Between waves the distribution is interpolated per decile; after the last
  wave, portfolios are held fixed. Short-run moves in shares mostly reflect
  asset prices (equities against housing), not observed redistribution. The
  2022 drop in the top 10% (54.5% → 53.4%) coincides with a fall in
  households' equity in DWA's own series: equity and fund shares
  (`A.LE.F5._Z.EUR`) went from €1,972bn to €1,823bn (−7.6%) and listed
  shares (`F511`) from €330bn to €286bn (−13.2%) between 2021-Q4 and
  2022-Q4, while total net wealth rose 0.8%.
- WP 2687 Table 1 names Challenges as France's rich list for the third wave.
  The same list is probably used for the other waves, but this is not
  stated. Challenges is also our `data/manual/challenges_500.csv`, so DWA's
  top tail is **probably not fully independent of our rich-list
  comparison**.
- `PT` shares are published to two decimals. Derived shares carry rounding
  of about 0.01 points.

## References

1. ECB press release, 8 January 2024, "ECB publishes new statistics on the distribution of household wealth". https://www.ecb.europa.eu/press/pr/date/2024/html/ecb.pr240108~ae6f7ef287.en.html
2. ECB, "Experimental Distributional Wealth Accounts (DWA) for the household sector – Methodological note", 8 January 2024. https://data.ecb.europa.eu/sites/default/files/2024-01/DWA%20Methodological%20note_0.pdf
3. Banque de France, "Comptes distributionnels de patrimoine des ménages – Sources et méthodologie" (file dated 2026-09). https://www.banque-france.fr/system/files/2026-09/F26z_note_methodologique_DWA.pdf
4. Engel, J., Gayà Riera, P., Grilli, J. and Sola, P. (2022), "Developing reconciled quarterly distributional national wealth – insight into inequality and wealth structures", ECB Working Paper 2687, July 2022 (Table 1: "FR – Challenges (504)"). https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp2687~a91d434d45.en.pdf
5. Data: ECB Data Portal SDMX API, dataflow `DWA` (structure `ECB_DWA1`). https://data-api.ecb.europa.eu/service/data/DWA/
