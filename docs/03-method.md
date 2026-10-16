# 3. Method: how each number is computed

Every figure on the page can be recomputed from the raw files with the
scripts in `pipeline/`. This page gives the formula behind each one, the
choices made, and why. Version 0.4 follows two rounds of adversarial reviews
by AI reviewer agents (methodology, numbers, code, sources, accessibility); see [reviews/](reviews/) and the
response in [reviews/response.md](reviews/response.md).

## 3.1 Pipeline

```
pipeline/fetch.py        downloads  ──►  data/raw/  (not versioned)
pipeline/build_data.py   data/raw + data/manual  ──►  site/data/france.json
pipeline/top_tail.py     scenario model for the top of wealth
pipeline/sources/*.py    independent sources: dwa, insee, prices, housing, rates
pipeline/tests/          tests (python3 -m unittest discover -s pipeline/tests)
site/index.html          reads site/data/france.json and draws the charts
```

Standard library only (Python ≥ 3.9). `fetch.py` exits with an error if any
source fails; files are written under a temporary name and renamed when
complete; the WID zip's ETag and Last-Modified are saved in
`data/raw/wid_vintage.json` and copied into the output, with a sha256 of
every input file. `build_data.py` stops if a cross-check source is missing
or fails its own checks, unless `--partial` is given (the output then lists
what was left out in `meta.sources_status`).

## 3.2 Choices and why

| Choice | Alternatives | Why this one |
|---|---|---|
| WID.world distributional national accounts as backbone | INSEE income and wealth surveys | Only source covering the whole distribution down to the top 0.001% and adding up to national totals. Surveys miss the top ([01-concepts.md §1.6](01-concepts.md#16-measuring-the-very-top)). Independent sources are used as cross-checks (§3.10). |
| Unit: adults 20+, equal split within couples | Household, consumption units | WID's unit. Stated on every chart. Not comparable in level with INSEE's *niveau de vie*. |
| Three measures | Cash disposable income | Post-tax national income includes health, education and public services. WID's cash disposable series for France stops in 1979, so cash income comes from INSEE where needed (housing). |
| Seven non-overlapping layers | Deciles, overlapping top groups | Layers that partition the population show how the pie is split; their sizes follow the orders of magnitude of the top, so the very top is never averaged away. |
| Growth/share decomposition | "Transfers" (Δshare × end total) | Version 0.1 valued share changes at the end-year total and called them transfers. Reviewers showed this reads as a zero-sum flow the data do not show (§3.5). |
| Scenarios in both directions | Rich lists only | A tool that can only raise the top cannot express that the top might be overstated (§3.7). |
| Default start year 1990 | 1980 | WID starts lifting its top group to Forbes totals in 1988; a pre-1988 start compares two methods at the very top. Any year can be selected; the page warns when the start is before 1988. |

## 3.3 Real values

WID averages and thresholds are in constant euros of the price base year
(where `inyixxi999 = 1`; currently 2025, a year WID partly projects).
Nominal series from other sources are converted with the same index:

```
real(y) = nominal(y) / inyixxi999(y)
```

Rich-list totals are used as quoted in published articles: in euros when an
article gives euros (Forbes 2017, 2020, 2021, 2024), otherwise in dollars
converted with WID's yearly market rate `xlcusxi999` (Forbes 2022). The 2021
euro figure ("plus de 450") is a lower bound, and the 2024 figure (€624 bn)
comes from a July article, so it may not use Forbes's March valuation.

**Consumer-price option.** `value_cpi = value_wid × inyixxi999(y) / cpi(y)`,
both equal to 1 in the base year. INSEE's CPI from 1990, extended back with
INSEE's long euro/franc coefficient (two decimals, too coarse before 1950);
for years before 1950 the 1950 ratio is held, so no artificial step appears.
With the CPI, real growth of mean wealth per adult over 1980–2024 is 163%
instead of 181% (see `paper/numbers.md`).

## 3.4 Layers

| Key | Label | Adults (2024) |
|---|---|---|
| `p0p50` | Bottom 50% | 26.5 million |
| `p50p90` | Middle 40% | 21.2 million |
| `p90p99` | Top 10% to 1% | 4.8 million |
| `p99p99.9` | Top 1% to 0.1% | 477,000 |
| `p99.9p99.99` | Top 0.1% to 0.01% | 48,000 |
| `p99.99p99.999` | Top 0.01% to 0.001% | 4,770 |
| `p99.999p100` | Top 0.001% | 530 |

Each layer is summed from WID's 127 g-percentile averages, which are
published at full precision:

```
wealth[a,b) = Σ over g-percentiles in [a,b) of avg × width
share[a,b)  = wealth[a,b) / Σ over all g-percentiles
avg[a,b)    = wealth[a,b) / (b − a)
```

WID's published group shares (4 decimals) are kept as `share_published`. The
build stops if any layer differs from them by more than 0.0002; the largest
difference today is below 0.0001 (0.000095, rounding). Years with a missing g-percentile
would fall back to differencing the published shares (`layer_fallback_years`;
none today).

## 3.5 How each slice changed

For a layer L between start year B and end year E, with s its share and T the
real total:

```
ΔW_L          = s_L(E)·T(E) − s_L(B)·T(B)                 change in real holdings
growth effect = (s_L(B) + s_L(E))/2 · (T(E) − T(B))       had the share stayed put
share effect  = (s_L(E) − s_L(B)) · (T(B) + T(E))/2       due to the share moving
ΔW_L = growth effect + share effect                          (exact)
change as a share of the total change = ΔW_L / (T(E) − T(B))
```

The last ratio is shown only when the total rose by at least 5% between B
and E: when the total falls or barely moves it explodes or changes sign
(e.g. 2020–2024 would give 234% for the top 0.001%) and carries no meaning.

Average weights make the split exact and independent of the order (a
two-factor Shapley decomposition). The page shows both effects and the net,
plus the share effect valued at T(B) and at T(E) for comparison.

Example, wealth, WID as published, 1990–2024: total real household wealth
rose by €9.7 tn. The top 0.001% (530 adults) received 7.7% of that rise
while holding 1.4% of wealth in 1990; the bottom 50% (26.5 million adults)
received 2.7% while holding 8.9%. The bottom half's real holdings rose by
€265 bn; had it kept its 1990 share they would have risen by €866 bn
(8.9% × €9.7 tn). Its growth effect in the decomposition, at the average of
its 1990 and 2024 shares, is €667 bn.

What it is not: layers are ranks, not the same people; nothing says euros
were taken from one group and given to another. For wealth, much of the
total's rise is asset-price revaluation (housing in particular) rather than
saving; separating price and volume effects is planned (§3.13).

**Start-year sensitivity.** The share effect up to the end year, for every
possible start year, for the top 0.001%, the top 1%, the middle 40% and the
bottom 50%. Spikes in early years come from odd single data points in WID's
historical series (e.g. the top 0.001% wealth share is 0.24% in 1975 between
0.84% and 0.83%, and 0.38% in 1984 between 0.51% and 0.52%; 1961 and 1963
have identical share vectors).

## 3.6 Growth incidence curve

For each of WID's 127 g-percentile groups j:

```
g_j = (avg_j(E) / avg_j(B) × pricefactor(E) / pricefactor(B))^(1 / (E − B)) − 1
```

Groups whose average is below 1% of the smaller of the two years' overall means are left
out. The x axis is the group's index, so the top 1% (28 groups) is spread out.
The summary quotes the bottom 50% *layer's* own growth (version 0.2 averaged
the rates of its groups, which understated it), and flags start years before
1988 for wealth.

## 3.7 The very top: calibration, rich lists, scenarios

### What WID already does

WIL Technical Note 2025/01 (Bajard et al. 2025, pp. 4–5, cited in this
vintage's France metadata) harmonises Forbes billionaire data from 1988 to
2024 and, where WID's billionaire wealth is lower than Forbes, adds the
difference to the top g-percentile, taking it proportionally from the rest
of the distribution. So from 1988 WID's top 0.001% is calibrated to Forbes.
The largest one-year jumps of the top 0.001% wealth share are 2020–21
(+1.34 pts), 1998–99 (+1.18 pts) and 2013–14 (+1.00 pt); the first years go
0.74% (1987) → 1.17% → 1.45% (1989). Over 2014–2024 the layers just below
the top 0.001% are flat while the top 0.001% rises from 3.39% to 5.58%,
which points to the calibration rather than a broad rise in top fortunes.
Year-to-year jumps in this calibrated group can therefore reflect changes in
what the Forbes list covers as much as changes in wealth.

### Comparison with rich lists

```
WID top 0.001% total(y) = share_top0.001(y) × T(y)
```

shown with WID's top 0.01% total, the Challenges top-500 total (July, gross
professional wealth of families at market prices, residents and
non-residents) and the Forbes French billionaires total (citizens). Both
rich-list series are totals *quoted in published articles*, one source and
the exact quote per year in `data/manual/` (see
[notes/rich-lists-sources.md](notes/rich-lists-sources.md)); years with no
published total are left empty rather than computed. In 2024, in 2025 euros:
WID top 0.001% €817 bn, Forbes €631 bn (53 billionaires, €624 bn quoted),
Challenges €1,242 bn, WID top 0.01% €1,115 bn. Challenges ÷ WID top 0.01%
went from 0.49 (2004, the first year with a published euro total) to 1.11
(2024). Challenges is valued in July, WID yearly: the two can be months
apart, and listed luxury shares move by ±20–30% within a year.

### Scenarios (`pipeline/top_tail.py`, `build_scenarios`)

Rich list. Garbinti, Goupille-Lebret & Piketty (2016, rev. 2017, WID WP 2016/6, appendix H) split each
Challenges family into 1, 10 or 15 members, 80% of them married, and remove
about 20% of the list's wealth as held by non-residents. Under WID's
equal-split unit one member is 1.8 adults on average.

```
n      = 500 × members × 1.8           adults covered
RL_adj = Challenges × (1 − c)
W_n    = WID wealth of the richest n adults (the whole top g-percentile plus
         a uniform share of the next ones; n ≥ 900 adults covers ~530 in the
         top bin and ~70% of the next one in 2024)
if RL_adj > W_n: richest n get RL_adj, everyone else × (T − RL_adj)/(T − W_n)
```

Challenges totals are those quoted in published articles (euro totals from
2004); years inside that range with no published total (2005, 2008, 2011,
2015, 2021) are filled by geometric interpolation between the neighbouring
published years and listed in `interpolated_list_years`, so scenario lines do
not drop back to WID for a single year.

The rule is one-sided because a rich list is a lower bound on what the
richest n own (unlisted assets, missed fortunes); a list below WID does not
show WID is too high. W_n and RL_adj are exported every year
(`rich_list_check`) and shown in the page's table.

ECB / Banque de France (lower). The distributional wealth accounts put the
top 5% of households 5.8–7.6 points below WID's top 5% of adults every year
2009–2024. The scenario sets WID's top-5% share to the DWA value and scales
every g-percentile above P95 by the same factor, everyone else by the
complementary factor. This is our illustration, not a published estimate:
the accounts publish nothing finer than the top 5%, and the same top-5% value
is consistent with top 0.001% shares from about the Forbes floor (4.3%) to
WID's 5.6%. It also lifts the poorest half to 5.47% in 2024, above the
accounts' own 5.00%; households are not adults; and the accounts calibrate
their French top tail on a rich list, so this scenario is not independent of
the Challenges ones. The headline range uses the Forbes floor as its lower
end.

| Scenario key | Top 0.001% share, 2024 | Years changed | Parameters |
|---|---|---|---|
| WID as published | 5.6% | – | – |
| `dwa_lower` | 4.8% | 16 (2009–2024) | top 5% at DWA level |
| `ggp_central` | 5.6% | none | 10 members (18 adults) per family, c = 20% |
| `ggp_low` | 6.5% | 8 (2016–2024) | 1 member (1.8 adults) per family, c = 20% |
| `no_cut` | 8.1% | 18 (2007–2024) | 1 member per family, c = 0 (beyond published assumptions) |

The honest headline for the top 0.001% share of wealth in 2024 is therefore
a range: about 4.8% to 6.5% under published assumptions (0.8 points below
and 0.9 above WID's 5.6%), and 8.1% if no rich-list wealth is attributed to
non-residents. An earlier WID-team estimate
for 2014 (Garbinti et al., WID WP 2016/5, table 1) gives 0.9% for the top
0.001% against 3.4% in today's vintage: the method, not only the data,
drives the very top.

### WID's top bin is internally inconsistent

The threshold to enter the top 0.001% sits far above what the thresholds just
below imply. With the local Pareto slope from p99.99 to p99.998 (alpha 1.9 in
2024), the p99.999 threshold would be about €136 M; WID's is €799 M, 5.9×
higher, which would require alpha below 1 (infinite mean). A smaller jump
exists before the Forbes calibration (1980: €50 M vs €35 M projected). The
most likely cause is the refit of the distribution after the top-up. Version
0.2 read this as "fortunes between €100 M and €800 M are thin"; that reading
is withdrawn, since the data support it no more than the reading that the
threshold is an artifact. It does not affect the scenarios: they cover at
least 900 adults, so WID's top g-percentile (~530 adults) is always taken
whole. (A Pareto split of that bin, with alpha from the threshold chain, is
implemented for lists covering fewer adults but is not used here.)

## 3.8 Income at the very top (IPP comparison)

IPP (Bach, Bozio, Guillouzouic & Malgouyres 2025; IPP Note 92, 2023) measure
2016 top incomes of tax households with retained profits attributed in
several ways. The page compares **euros**, not shares, because the
denominators differ by about 2× (WID: national income, €1.9 tn; IPP: fiscal
or comprehensive income of households, €1.0–1.2 tn).

| 2016, € bn | WID pre-tax (adults) | IPP taxable | IPP dividend-imputed | IPP comprehensive (2025) | IPP economic (Note 92 rev.) |
|---|---|---|---|---|---|
| Top 1% | 198.8 | 100.3 | 161.6 | 172.1 | 219.4 |
| Top 0.1% | 68.1 | 33.9 | 60.8 | 77.0 | 128.0 |
| Top 0.01% | 24.7 | 12.9 | 22.6 | 41.1 | 88.9 |
| Top 0.001% | 9.2 | 4.7 | 8.1 | 24.5 | 65.0 |

Reading: WID is close to IPP's dividend-proportional variant, which is the
usual DINA rule. With retained profits attributed through actual ownership
chains, IPP's group totals are 2.7× WID's for the top 0.001% and 1.7× for the
top 0.01%, about the same for the top 0.1% (1.13×) and less for the top 1%
(0.87×). These ratios are ours, computed from IPP's published group means;
IPP do not compare with WID. IPP's own comparison with a dividend-based
imputation gives 3.03 and 1.82 at the top (Table A2), and IPP put the top
1%'s income share above Garbinti et al.'s (13.8% in 2016 vs 10.8% for 2014,
pp. 3 and 13). WID therefore likely understates the very top's income; for
the top 1% the answer depends on comparing euros or shares. Groups differ
(378 households, containing more people than WID's 507 adults, which pushes
our ratios up), and this is one year only. Version 0.2's "shares match
taxable income" and "4×" were artifacts of the different denominators.

## 3.9 Housing and fixed costs

- **Income.** INSEE income survey (ERFS), mean disposable income per
  consumption unit by tenth of persons, converted from constant euros to
  nominal with INSEE's CPI; at series breaks the newer method is kept.
  Groups: tenths 1–5, 6–9, 10. This is cash income after taxes and benefits,
  the income of a person living alone; a couple counts 1.5 units.
- **Prices.** Both regions use open data only: the 2025 DVF mean price per m²
  of flats (Etalab "Statistiques DVF", Licence Ouverte) carried back with
  INSEE's price index for Paris flats (from 1992) and for provincial flats
  (from 1995). These are constant-quality estimates, not observed yearly
  averages. DVF includes off-plan new-build sales; a comparison made for an
  earlier version found Paris DVF averages a few percent above the
  Notaires-INSEE level, so both levels are probably a few percent too high
  (that comparison can no longer be rerun from this repository). (Version 0.3 used the Notaires level for
  Paris; it was replaced because that table is not openly licensed.)
- **Years of income** = 70 × price per m² / income.
- **Yearly repayment share** = 70 × price × r / (1 − (1 + r)^−25) / income,
  with r the ECB's yearly average French mortgage rate (2000–). No deposit,
  insurance or taxes.
- Results for the bottom half of persons in Paris: 19 years of income in
  1996, 41 in 2023; the repayment would take 155% of income in 2000 and 236%
  in 2023. Outside the Paris region: 8 → 13 years, repayment 60% → 75%.
- **Pre-committed spending**: INSEE national accounts, share of household
  disposable income (1959–2025). By income group only survey points exist,
  with different definitions (DREES 2011; France Stratégie 2001–2017).
- **Housing share of gross assets**: WID composition 1970–2014 (groups ranked
  by wealth). These series do not add up exactly to today's net wealth
  figures (they come from an earlier estimation); read them for trends.
- **Prices by income.** INSEE's CPI by decile rose 56.1% for the poorest half,
  54.5% for the next 40% and 52.5% for the richest tenth (1998–2025, unweighted
  means of decile indices). Small next to housing; not applied per layer.

## 3.10 Cross-checks with independent sources

See [notes/dwa.md](notes/dwa.md) and [notes/insee.md](notes/insee.md). Gaps on
the page are computed from the data.

| Indicator | Agreement | Disagreement |
|---|---|---|
| Wealth, bottom 50% | WID − ECB/BdF between −0.6 and +0.4 points, 2009–2024 (level; the 2009–14 trends differ) | INSEE survey (gross wealth) higher, 6–8% |
| Wealth, middle 40% | – | ECB/BdF 4.7–6.8 points above WID every year 2009–2024 (40.6% vs 35.3% in 2024) |
| Wealth, top 5% / 10% | Same upward direction 2009–2024 | WID 5.8–7.6 points above ECB/BdF every year, already before 2014; INSEE survey far lower |
| Income after tax, top 10% | Close in recent years | WID − ERFS from −1.8 to +3.5 points over 1996–2018 across INSEE's method segments (−1.7 to +3.3 with the newest method only), opposite trends |
| Income after public services, bottom 50% (2019) | – | INSEE distributed accounts 38% vs WID 32%: INSEE does not re-rank people, uses consumption units, and attributes education and collective spending by use; WID (Fisher-Post & Gethin 2023; DINA guidelines) attributes health close to lump-sum and education and other spending in proportion to disposable income. The page does not separate these effects. |
| Top income (2016) | WID ≈ IPP dividend-imputed | IPP ownership-based 1.7–2.7× WID at the top 0.01–0.001% (§3.8) |
| Top 0.001% wealth, two vintages | – | 0.9% (2016 paper) vs 3.4% (today) for 2014 |

Reading: independent sources agree with WID on the level of the poorest
half's share of wealth. They disagree on the middle 40% (WID lower) and on
the top 5% (WID higher), and sources and vintages diverge most at the very
top, in both directions.

**Post-tax income after 2018.** WID's metadata states that the 2019–2022
post-tax series apply the 2019 pre-tax/post-tax ratio by g-percentile;
2023–2024 carry the same quality flag. Post-tax changes after 2018 therefore
contain no information on taxes or benefits after 2019.

## 3.11 Quality flags and method breaks

The page shades years by WID's own `data_quality` flag (darker = lower) for
every year, not only the recent extrapolation, and marks 1988 for wealth.

| Measure | Years | WID flag | Method |
|---|---|---|---|
| Wealth | 1900–1969 | 2 | estate multiplier |
| Wealth | 1970–2014 | 4 | capitalised tax data, survey, national accounts |
| Wealth | 2015–2024 | 0 | 2014 asset mix per group held fixed, moved with asset totals |
| Wealth, top g-percentile | 1988– | – | lifted to Forbes totals (TN 2025/01) |
| Pre-tax income | 1900–1969 | 3 | fiscal tabulations (1901–09, 1911–14 missing) |
| Pre-tax income | 2019–2024 | 4 | extrapolated |
| Post-tax income | 1980– | – | Fisher-Post & Gethin (2023); 2019+ fixed 2019 ratios |

The population aged 20+ rose from 26.8 million (1900) and 38.2 million
(1980) to 53.0 million (2024) and aged strongly; fixed-percentile wealth
shares move with age structure independently of any redistribution.

## 3.12 Tests

`pipeline/tests/test_build.py` compares things computed two ways, so the
tests can fail:

- the Pareto split against its closed form for several alphas; the alpha
  from a threshold chain; input guards;
- a toy scenario where the corrected top must equal the list exactly, the
  non-resident cut, and a straddling layer checked by hand;
- layers summed from g-percentiles against WID's published shares, and the
  middle 40% against WID's directly published share;
- monotone layer averages and thresholds; threshold/average coherence;
- g-percentiles rebuilding WID's published mean every year (within 2%);
- comparison series wired to the right WID group;
- the rich-list deflation and non-resident cut;
- scenario direction (rich lists never lower, ECB never raises the top);
- the scenario table in this document against the build (an oracle);
- IPP amounts present and group sizes in a 10× ladder; no NaN or Infinity in
  the JSON.

## 3.13 Planned extensions

1. Separate price and volume effects in wealth changes (asset composition).
2. Obtain WID's uncorrected France top series to show the top 0.001% with and
   without the Forbes calibration.
3. A calibrated Pareto tail fitted jointly to WID thresholds and rich-list
   observations (Vermeulen 2018; Bach, Thiemann & Zucco 2019).
4. Within-age-group shares (1970–2014).
5. Combined income + wealth (Weisbrod–Hansen), by layer.
6. Restricted microdata through CASD ([04-restricted-data-plan.md](04-restricted-data-plan.md)).
