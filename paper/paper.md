---
title: "Show Me Your Pie: who holds France's wealth and income, slice by slice, 1900–2024, and how sure can we be?"
author: "Show Me Your Pie contributors (maintainer: github.com/Zboule)"
status: "Working paper, version 0.4. Open for review: see CONTRIBUTING.md."
date: "October 2026"
---

# Abstract

We describe how French household wealth and national income are split
between seven non-overlapping slices of the adult population, from the
poorest half to the richest 0.001% (about 530 adults), from 1900 to 2024.
The backbone is the World Inequality Database (WID.world), whose
distributional national accounts split all of national income and household
wealth across adults. We add: (i) an exact decomposition of each slice's
change into the growth of the whole pie and the change of its share;
(ii) alternative estimates of the very top, bounded below by the Forbes
billionaire total and above by the Challenges rich list under published
assumptions; (iii) comparisons with independent producers (ECB / Banque de
France, INSEE, IPP); and (iv) housing affordability in years of cash income
and in mortgage repayments.

In WID, the richest 0.001% held 5.6% of household wealth in 2024 against
1.4% in 1990. That figure is the least certain one here: the 53 French
billionaires counted by Forbes alone hold about 4.3% of French household
wealth, and the Challenges list under published assumptions implies up to
6.5%; an earlier estimate by the same research team gave 0.9% for 2014 where
the current vintage gives 3.4%. The poorest half held 4.8% of wealth in 2024
against 8.9% in 1990, while its average real wealth rose from €21,100 to
€26,800. Of the €9.7 tn rise in real household wealth over 1990–2024, the
richest 0.001%'s holdings rose by an amount equal to 5.8% to 9.0% of it
(7.7% in WID as published), the poorest half's by 2.7%. Most of that rise is
asset revaluation, and after 2014 WID's wealth shares are largely
mechanical. Taxes, benefits and public services raise the poorest half's
share of income from 20.3% before tax to 31.9% (2018, the last
non-extrapolated year). Independent sources agree with WID on the poorest
half's share of wealth, but not on the middle 40% or the top.

# 1. Introduction

Public debate about inequality usually rests on one or two numbers, such as
a top-10% share or a Gini coefficient. They hide where change happens and
how uncertain it is. This project asks three plain questions: who holds which
slice of France's pie, how have the slices changed, and how sure can we be?
It answers them with open data, open code and an open review process, and
with a public page written for non-specialists
([site/index.html](../site/index.html)).

Our contribution is not new primary estimation. It is a transparent
re-reading of the best available estimates, organised around three
principles that the reviews of earlier versions forced on us:

1. **Slices that partition the population.** Overlapping groups (the top 10%
   contains the top 1%) cannot show how the pie is split. Seven disjoint
   slices whose sizes follow orders of magnitude (50%, 40%, 9%, 0.9%, 0.09%,
   0.009%, 0.001%) can, and they never average away the very top.
2. **Growth and shares separated.** A falling share can hide a rising level.
   Each slice's change is split exactly into a growth effect and a share
   effect.
3. **Ranges where sources disagree.** At the very top we report an envelope
   of assumptions, not a point.

# 2. Concepts

Wealth is net personal wealth: housing, business and financial assets minus
debts. Income is either pre-tax national income (after pensions, before
taxes, including non-cash items such as imputed rents and company profits
attributed to shareholders) or post-tax national income (after all taxes,
plus cash benefits and the value of public services). The unit is the adult
aged 20 and over, with a couple's income and wealth split equally. Each
measure ranks people by that measure, so the "poorest half" before and after
tax are not the same people. The concepts and their literature are set out
in [docs/01-concepts.md](../docs/01-concepts.md).

# 3. Data

Table 1 lists the sources. Details, licences and the reasons for each
choice are in [docs/02-data-france.md](../docs/02-data-france.md) and
[DATA_LICENSES.md](../DATA_LICENSES.md).

| Source | Use | Years |
|---|---|---|
| WID.world, France (Garbinti, Goupille-Lebret & Piketty 2018, 2021; Fisher-Post & Gethin 2023; WIL Technical Note 2025/01) | Backbone: 127 g-percentiles of wealth, pre-tax and post-tax income | 1900–2024 (post-tax 1980–) |
| ECB / Banque de France distributional wealth accounts | Cross-check; illustrative lower scenario | 2009–2025 |
| INSEE ERFS income survey, Histoire de vie et Patrimoine wealth survey, distributed national accounts | Cross-checks; cash income for housing | 1975–2024 |
| IPP (Bach, Bozio, Guillouzouic & Malgouyres 2025) | Top incomes with retained profits | 2016 |
| Challenges "500 fortunes"; Forbes French billionaires (totals quoted in published articles, one quote per year) | Rich-list bounds and scenarios | 2004–2026; 2017–2025 |
| INSEE consumer and house price indices; DVF transaction statistics; ECB mortgage rates; INSEE national accounts | Prices, housing, fixed costs | 1959–2025 |

All inputs are fetched by `pipeline/fetch.py` and their sha256 recorded in
the built dataset; the WID vintage is identified by its ETag.

# 4. Methods

The full specification is in [docs/03-method.md](../docs/03-method.md).

**Slices.** Each slice is the sum of the WID g-percentiles it covers; its
share is that sum over the sum of all g-percentiles. WID's own published
group shares are an independent check; the largest difference is below
0.00010 (rounding).

**Decomposition.** For slice L between years B and E, with share s and real
total T,

    ΔW_L = (s_B + s_E)/2 · (T_E − T_B)  +  (s_E − s_B) · (T_B + T_E)/2
           growth effect                    share effect

which is exact and order-independent (a two-factor Shapley split). We also
report ΔW_L / (T_E − T_B), the slice's change as a share of the total change,
only when the total rose by at least 5% between B and E; otherwise the ratio
is not meaningful and is not shown.

**The very top.** WID raises its top g-percentile to the Forbes billionaire
total from 1988 (Technical Note 2025/01). We bound the top 0.001% share of
wealth with:

- *Forbes floor:* the Forbes total for French billionaires (citizens; quoted
  in published articles) as a share of WID's total wealth. The billionaires
  are a subset of the richest 530 adults if they are French residents, so this
  is a lower bound up to residence and valuation differences.
- *Rich list:* following the parameters of Garbinti, Goupille-Lebret &
  Piketty's data appendix H (WID WP 2016/6), each Challenges family is split
  into 1 or 10 members of 1.8 equal-split adults on average, and 20% of the
  list's wealth is attributed to non-residents (or none, beyond the published
  assumptions). Where the adjusted list exceeds WID's wealth for that many
  adults, the richest adults get the list's total and everyone else is scaled
  down, keeping the total; otherwise WID is kept, because a rich list is a
  lower bound on what the richest own. No gross-to-net haircut is applied.
- *Illustrative lower scenario (ECB / Banque de France):* WID's top-5% share
  is set to the distributional wealth accounts' value by scaling every
  g-percentile above P95 by one factor and the rest by another. This is our
  assumption, not a published estimate: the accounts publish nothing finer
  than the top 5%, and the same top-5% figure is consistent with a wide range
  of top 0.001% shares. It also raises the poorest half above the accounts'
  own figure, and the accounts themselves calibrate on a rich list, so it is
  not independent of the Challenges scenarios.

WID's wealth of the richest n adults is the whole top g-percentile plus a
uniform share of the following ones: the rich-list scenarios cover at least
900 adults, more than WID's top g-percentile (~530), so no assumption about
the shape inside the top bin is needed (see §5.3 on why its entry threshold
should not be used); a Pareto shape inside the next bin would move the 2024
result by at most 0.02 points.

**Housing.** Years of cash disposable income (INSEE ERFS, per consumption
unit, by tenths of persons) needed for 70 m² of existing flat, and the yearly
repayment of a 25-year loan at the year's average French mortgage rate (ECB),
with price levels from the 2025 DVF transaction average carried back with
INSEE's indices.

# 5. Results

## 5.1 A century of slices

Table 2: share of wealth held by the richest 1% (the four top slices), the
richest 0.001% and the poorest half (WID as published).

| Year | Richest 1% | Richest 0.001% | Poorest 50% |
|---|---|---|---|
| 1900 | 55.0% | 2.6% | 1.6% |
| 1950 | 33.4% | 1.3% | 3.2% |
| 1980 | 17.2% | 0.80% | 8.4% |
| 1990 | 17.7% | 1.4% | 8.9% |
| 2014 | 25.8% | 3.4% | 5.0% |
| 2024 | 27.7% | 5.6% | 4.8% |

Wealth concentration fell sharply from 1900 to 1980 and rose again after.
The rise of the richest 0.001% after 1988 overlaps with WID's Forbes
calibration and must be read with §5.3. Income is far less concentrated: the
richest 0.001% held 0.88% of pre-tax income in 2024.

## 5.2 How the slices changed, 1990–2024

Real household wealth rose by €9.7 tn between 1990 and 2024. The richest
0.001%'s holdings rose by an amount equal to 7.7% of that rise in WID (5.8%
to 9.0% across the alternative estimates of §5.3, the low end being the
Forbes floor), while the group held 1.4%
of wealth at the start; the poorest half's rose by 2.7%, while it held 8.9%.
The poorest half's real holdings rose by €265 bn; had it kept its 1990 share
they would have risen by €866 bn. Its average real wealth per adult went from
€21,100 to €26,800: it got richer in absolute terms and poorer in relative
terms. These are ranks, not the same people, and most of the rise in total
wealth is the revaluation of housing and shares, not saving; after 2014,
WID holds each group's 2014 asset mix and moves it with asset totals, so
share changes since then are largely mechanical.

In 2024 the richest 0.001% held as much wealth as the poorest 51.9% of
adults put together in WID; between 48.3% and 54.1% across the alternative
estimates. Many adults in the poorest half own very little or owe more than
they own.

Taxes, benefits and public services change the picture for income: in 2018,
the last year WID does not extrapolate, the poorest half received 20.3% of
pre-tax income and 31.9% of post-tax income (each ranked by its own income).
WID's 2024 figures (20.3% and 31.5%) contain no new information: the 2024
pre-tax distribution repeats 2023 and post-tax incomes apply 2019 ratios. The
post-tax figure depends on how public services are attributed (health close
to lump-sum, education and other spending in proportion to income in WID);
INSEE's distributed accounts, which attribute education by use and do not
re-rank people, give the poorest half 38% in 2019, against 32.1% in WID.

## 5.3 How sure are we about the very top?

1. **Bounds.** For 2024 the top 0.001% share of wealth is 5.6% in WID. The
   53 billionaires counted by Forbes alone hold 4.3% (a floor, up to
   residence and valuation). The rich list under published assumptions gives
   5.6% with ten members per family (no correction needed) and 6.5% with one
   (8 years corrected); with no non-resident cut, beyond published
   assumptions, 8.1% (18 years corrected; years with no published Challenges
   total are interpolated between neighbouring years). The illustrative
   ECB-based scenario
   gives 4.8%. We summarise the top 0.001% in 2024 as 4.3% to 6.5%. These are
   envelopes of assumptions, not confidence intervals: WID publishes no
   sampling or model uncertainty.
2. **Vintages.** An earlier estimate by the same team (WID WP 2016/5, table 1)
   put the top 0.001% at 0.9% in 2014; the current vintage gives 3.4%. The
   Forbes calibration is one reason; the published material does not let us
   apportion the revision between it and other changes. The revision is not
   confined to the top: the same table gives the poorest half 6.3% and the
   middle 40% 38.4% of wealth in 2014, against 5.0% and 36.3% in the current
   vintage.
3. **Calibration.** From 1988 WID lifts its top group to Forbes totals. Over
   2014–2024 the slices just below the top 0.001% are flat while the top
   0.001% rises: the rise is concentrated in the calibrated group, so its
   year-to-year jumps can reflect what the Forbes list covers as much as
   changes in wealth.
4. **An internal inconsistency.** In 2024 the threshold to enter WID's top
   0.001% is €799 M, while the local Pareto slope of the thresholds just below
   implies about €136 M, a ratio of 5.9. No smooth distribution produces this
   jump; a smaller one exists before the calibration, and it most likely comes
   from refitting the distribution.
5. **Other sources.** The ECB / Banque de France accounts agree with WID on
   the poorest half's share of wealth (differences of -0.6 to +0.4 points),
   but put the middle 40% 4.7–6.8 points higher and the top 5% 5.8–7.6 points
   lower than WID in every year 2009–2024.

## 5.4 Top incomes and retained profits

For 2016, WID's pre-tax income of the top 0.001% (€9.2 bn) is close to IPP's
estimate when retained profits are attributed in proportion to dividends
(€8.1 bn), the usual distributional-accounts rule. With retained profits
attributed through actual ownership chains, IPP's group totals are 2.7 times
WID's for the top 0.001%, 1.7 times for the top 0.01%, 1.13 times for the top
0.1% and 0.87 times for the top 1% (our ratios, computed from IPP's published
group means; IPP do not compare with WID). IPP's own comparison with a
dividend-based imputation gives ratios of 3.03 and 1.82 at the top (their
Table A2), and IPP put the top 1%'s *share* of income above Garbinti et al.'s
(13.8% in 2016 against 10.8% for 2014; pp. 3 and 13). So WID likely
understates the very top's income; for the top 1% the answer depends on
whether one compares euros or shares. IPP's groups are tax households (378
for the top 0.001%, containing more people than WID's 507 adults), which
pushes our ratios up. One year only.

## 5.5 Housing and fixed costs

For one person living alone with the average cash income of the poorer half
of persons, a 70 m² flat in Paris cost 19 years of income in 1996 and 41 in
2023; repaying it over 25 years would have taken 155% of income in 2000,
peaking at 272% in 2012, and 236% in 2023. Outside the Paris region the
figures are 8 and 13 years, and 60% and 75%. These compare national incomes
with regional prices and ignore deposits; the mortgage rates for 2000–2002
are ECB estimates. Pre-committed spending (housing, energy, telecoms,
insurance) rose from 13.4% to 30.3% of household disposable income between
1959 and 2025. Consumer prices by income decile rose at similar rates (within
3.6 points over 1998–2025), but consumer price indices exclude house
purchases, so they cannot show how affordable buying a home has become.

# 6. Robustness

- **Start year.** Measured to 2024, the poorest half's share of wealth fell
  from every start year between 1966 and 2009 and from most later ones; it rose
  from starts between 1950 and 1960 and from 1962, 1964, 1965, 2010. The
  middle 40%'s share fell from every start between 1971 and 1997 (starts in
  1971–1997; 2002–2023). The very top
  depends strongly on the start year because of method breaks (1988, 2014)
  and odd single years (1975, 1984).
- **Prices.** Using INSEE consumer prices instead of WID's national-income
  deflator lowers the real growth of mean wealth per adult over 1980–2024
  from 181% to 163%; shares are unchanged.
- **Smoothing.** Averaging the last two years changes the 2024 shares of the
  four largest slices by less than a tenth of a point, and the top 0.001% by
  0.2 points (5.58% to 5.37%), reflecting the volatility of listed fortunes.
- **Precision.** Slices from full-precision g-percentiles differ from WID's
  rounded shares by less than 0.00010.

# 7. Limitations

1. The unit (equal-split adults) is not comparable in level with INSEE's
   *niveau de vie*, and each measure ranks people by itself.
2. The series stitch several methods: estate records before 1970, tax data
   from 1970 to 2014, a fixed-portfolio extrapolation after 2014, and the
   Forbes calibration from 1988. Decompositions from earlier start years mix
   methods, and the scenarios only cover 2004 (rich list) or 2009 (ECB)
   onward.
3. After 2014, wealth share changes are largely mechanical (fixed 2014
   portfolios plus the Forbes top-up). WID's 2024 pre-tax income distribution
   repeats 2023, and post-tax income for 2019–2024 applies 2019 ratios.
4. WID and the ECB / Banque de France accounts disagree by about 5 to 7
   points on the middle 40% and on the top 5%. The accounts and the rich-list
   scenarios probably share the Challenges list, so they are not independent.
5. Challenges is gross, family-level, market-priced wealth including
   non-residents; no gross-to-net or liquidity haircut is applied.
6. The ratio of a slice's change to the total change is undefined when the
   total falls or barely moves, and is then not shown.
7. Housing figures use a single-person consumption unit, national incomes
   against Paris prices, constant-quality price back-casts, and estimated
   mortgage rates before 2003.
8. We do not follow the same people over time, do not separate asset-price
   effects from saving, and use one national price index.
9. The population aged 20+ doubled since 1900 and aged strongly, which moves
   wealth shares by itself.
10. WID publishes no sampling or model uncertainty; our ranges are envelopes
    of assumptions, not confidence intervals.

The decisive improvement would come from administrative microdata (see
[docs/04-restricted-data-plan.md](../docs/04-restricted-data-plan.md)).

# 8. Reproducibility and review

The dataset is rebuilt with the commands in the README. The test suite
checks the model against closed forms and hand-computed cases, the slices
against WID's published shares, the page's calculations (in JavaScript)
against hand-computed cases, the scenario table in the method document
against the build, and every number in this paper against
`paper/numbers.json`, which is generated from the data by
`pipeline/paper_numbers.py`.

Four adversarial reviews (methodology, numbers, code, sources) were run on
version 0.2, and a second round on version 0.4; reports and responses are in
[docs/reviews/](../docs/reviews/). Each review was carried out by a separate
AI reviewer agent (Claude) with a critical brief and no access to the others'
conclusions; the numbers reviews recomputed the figures with their own code
from the raw files. **These are not peer reviews by outside experts**, and since
the analysis was also built with Claude, author and reviewers may share blind
spots. Human reviewers are invited through GitHub issues (see
[CONTRIBUTING.md](../CONTRIBUTING.md)).

**AI assistance.** Data collection, code, documentation and the review
rounds were carried out with Claude (Anthropic), under the maintainer's
direction. All numbers are reproducible from public sources, and every
hand-entered value carries its source.

**Data availability.** Code under the MIT licence; documentation under
CC BY 4.0; data belong to their producers (see
[DATA_LICENSES.md](../DATA_LICENSES.md)).

# References

See [docs/references.md](../docs/references.md) for the full list with
links. Main works: Garbinti, Goupille-Lebret & Piketty (2018, 2021);
Piketty, Saez & Zucman (2018); Blanchet, Fournier & Piketty (2022); Bajard et
al. (2025); Bozio et al. (2024); Fisher-Post & Gethin (2023); Blanchet,
Chancel & Gethin (2022); Bach, Bozio, Guillouzouic & Malgouyres (2025); André,
Germain & Sicsic (2023); Auten & Splinter (2024) and Saez & Zucman (2020);
Vermeulen (2018); Bach, Thiemann & Zucco (2019).

---

*Every number in this paper is listed in [numbers.md](numbers.md) with its
key; the test suite fails if the paper and the data disagree.*
