# 1. Concepts: what "how rich" means

This page explains the vocabulary the project is built on. Every later choice
(data, method, charts) refers back to it. References are in
[references.md](references.md).

## 1.1 Three ways to be rich

| Measure | Type | Answers |
|---|---|---|
| **Income** | flow (€/year) | What can you spend this year without getting poorer? |
| **Consumption** | flow (€/year) | What do you actually use? (smoother than income) |
| **Wealth** | stock (€) | What do you own, net of debts? Security, power, inheritance |

The Stiglitz–Sen–Fitoussi Commission [SSF2009] and the OECD framework on the
joint distribution of household income, consumption and wealth [OECD2013] both
insist on looking at all three, and *jointly*: two households with the same
income are not equally well off if one owns its home outright.

Real estate appears twice:
- as an **asset** (part of wealth: housing assets minus mortgage debt);
- as a **service**: an owner-occupier "pays rent to themselves". National
  accounts count this *imputed rent* as income, so owners and tenants with the
  same cash income are compared fairly.

## 1.2 The income ladder

Each step adds one correction. The ones you asked about (taxes, health,
education) are steps 3 to 5.

1. **Factor / market income**: wages + capital income (rents, interest,
   dividends, profits, including *retained* corporate profits in the
   distributional national accounts).
2. **Pre-tax income**: factor income after the pension system (pensions
   counted when received, contributions not deducted).
3. **Disposable income**: minus direct taxes and social contributions, plus
   cash benefits. INSEE's official *niveau de vie* is disposable income per
   consumption unit.
4. **Adjusted disposable income**: plus social transfers in kind, mainly
   **health care and education**, valued at their cost to the state
   [Verbist et al. 2012; OECD2013]. A family with two children at a public
   school receives a service worth several thousand euros per year.
5. **Post-tax national income** (DINA): every euro of national income is
   allocated to someone, including collective public spending (police,
   defence, roads) and net of indirect taxes such as VAT. The distribution then
   adds up exactly to national income [PSZ2018; DINA-G; BGGGP2024]. How
   in-kind spending is attributed matters: WID's benchmark gives health close
   to the same amount per person and shares education and other spending in
   proportion to disposable income [DINA-G p. 70; FPG2023], while INSEE
   attributes education by actual use [INSEE-AGS2023].
6. **"Arbitrable" income** (INSEE): minus pre-committed spending (housing
   including imputed rent, water, energy, telecoms, TV services, school
   canteens, insurance excluding life, financial services) [INSEE-c1358],
   about 30% of household disposable income (30.3% in 2025) [INSEE-T2103].
   Close to the felt margin of manoeuvre.
7. **Real income** (purchasing power): any of the above divided by a price
   index. Subtleties:
   - *Which index?* The national-income deflator (used by WID), the consumer
     price index, or an index specific to each income group (inflation differs
     across the distribution [Jaravel2021]; INSEE publishes CPIs by household
     category).
   - *Where?* Prices are about 7% higher in the Paris urban unit than in the
     rest of mainland France excluding Corsica (2022) [INSEE spatial price
     survey].
   - *PPP* (purchasing power parities) are needed only to compare countries,
     not France with itself over time.

## 1.3 Who is "a person"?

| Unit | Used by | Effect |
|---|---|---|
| Household | many surveys | Large households look richer |
| Consumption unit (OECD-modified scale: 1 / 0.5 per extra person 14+ / 0.3 per child) | INSEE *niveau de vie*, Eurostat | Accounts for economies of scale in a household |
| Adult (20+), resources split equally within couples | WID.world / DINA | Children not counted; comparable across countries and a century of data |

Numbers change with the unit, so every figure in this project states it.

## 1.4 Combining income and wealth

The classic approach is Weisbrod & Hansen [WH1968]:

```
comprehensive resources = income − capital income + annuity(net wealth, remaining life expectancy)
```

Capital income must be removed first; otherwise wealth is counted twice (once
through the rents and dividends it yields, once through the annuity).

Broader welfare measures put a euro value on life expectancy, leisure and
inequality [JK2016; Fleurbaey & Gaulier 2009]. They matter for international
comparisons but go beyond what this project measures.

## 1.5 Percentiles, thresholds, shares

Three objects are easy to confuse:

| Object | Example | Use |
|---|---|---|
| **Threshold** (quantile) | "€233k pre-tax income puts you at P99" | Where does a given person stand? |
| **Group average** | "The top 1% earn €562k on average" | How rich is a group? |
| **Share** | "The top 1% receive 11.8% of all income" | How is the cake divided? |

Summary indicators compress the whole distribution into one number: Gini
coefficient, P90/P10 ratio, Palma ratio (top 10% share / bottom 40% share),
Theil and Atkinson indices, top shares. They hide *where* the change happens,
which is why this project shows layers instead.

## 1.6 Measuring the very top

Household surveys miss the rich: few of them, high non-response,
under-reporting. The top is estimated from:

- **Tax data** (quasi-exhaustive), published as tabulations by bracket, with
  the distribution between brackets reconstructed by **generalized Pareto
  interpolation** [BFP2022].
- **Capitalization**: wealth inferred from capital income (dividends ÷ yield),
  combined with **inheritance / estate tax** data and wealth tax records
  [GGP2021].
- **Rich lists** (Challenges, Forbes) to check or calibrate the extreme tail
  [Vermeulen2018; BTZ2019]. WID's France benchmark [GGP2021] used them only
  as a cross-check; WID's current vintage adds the gap to Forbes to its top
  group, for every year from 1988, when its model is lower [TN2025-01]. See
  [notes/rich-lists.md](notes/rich-lists.md).

A specific problem for billionaires: their income mostly stays inside the
holding companies they own (*retained earnings*), so it never appears in
*fiscal* income [IPP2023]. Distributional national accounts allocate retained
profits to shareholders in proportion to dividends, which partly fixes this;
following actual ownership chains, IPP's group totals for the very top are
1.7–2.7× WID's (our ratios from IPP's published means [BBGM2025]).

Order of magnitude for France (about 53 million adults in 2024):
the top 1% is about 530,000 adults, the top 0.01% about 5,300, the top 0.001%
about 530, and the top 0.0001% about 53, roughly the number of French
billionaires. Below 0.001% WID publishes nothing; rich lists and one
tax-data study (IPP, top 75 tax households in 2016 [IPP2023]) are the only
sources.

## 1.7 Following it over time

- **Deflate** everything to constant euros.
- **Shares vs levels**: shares show the split of the cake; real averages show
  whether each group's slice grew. Both are needed: a falling share can hide a
  rising level when the cake grows.
- **How each slice changed**: a layer's change in real holdings splits
  exactly into a *growth effect* (the pie grew) and a *share effect* (its
  slice got bigger or smaller). Layers are ranks, not the same people, so
  this is not a flow of euros from one group to another (see
  [03-method.md §3.5](03-method.md#35-how-each-slice-changed)).
- **Growth incidence curve** [RC2003]: real growth of each percentile between
  two years. Caveat: it compares *ranks*, not the *same people* (anonymous,
  not panel, growth).
- **Breaks and provisional years**: methods change; the most recent years are
  extrapolated. For France WID flags wealth after 2014 (asset mix held at
  2014) and income after 2018; its top wealth group is lifted to Forbes
  totals from 1988; post-tax income after 2018 applies fixed 2019 ratios.
- **Choice of start year**: comparisons from 1980, near the twentieth
  century's low point for top wealth shares, show a larger shift to the top
  than comparisons from 1900 or 1950. The page lets the reader pick.
