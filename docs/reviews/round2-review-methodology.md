# Second-round referee report: methodology and results of "Show Me Your Pie" (working paper v0.4)

Reviewer brief: second-round review, from the standpoint of distributional national accounts (DINA), top incomes and wealth, and Pareto tails. It asks whether the round-1 findings ([review-methodology.md](review-methodology.md)) are resolved, and scrutinises what is new in v0.4. Date: 2026-10-16. Like round 1, this is an AI reviewer agent (Claude), not an outside expert.

How numbers were obtained:

- **[json]**: computed from `site/data/france.json` as committed. The test suite passes (23 tests), and `pipeline/paper_numbers.py` regenerates `paper/numbers.json` identically.
- **[raw]**: computed from `data/raw/WID_data_FR.csv` or the other raw files.
- **[csv]**: computed from `data/manual/*.csv`.
- Money is in constant 2025 euros unless marked otherwise.
- Every number below was recomputed by me. None is copied from the project's documents.

---

## 0. Verdict

**Major revision. Do not publish until the five items in §5.1 are fixed.**

Most of round 1 has been dealt with seriously:

- The "transfer" vocabulary is gone, replaced by an exact two-factor Shapley split.
- All scenarios are selectable, families are converted at 1.8 adults per member, and a downward scenario exists.
- The default start is 1990.
- Quality flags are shaded for every year.
- The IPP comparison is in euros, and the housing metric uses cash income and financing costs.
- Every number in the paper can be regenerated from the data.

The new material, however, introduces fresh problems.

- **The abstract's "the bottom and middle are robust across sources" is contradicted by the project's own data.**
  - WID gives the middle 40% about 5 points less wealth than the ECB / Banque de France accounts, every year from 2009 to 2024.
- **The lower ("ECB / BdF") scenario is the project's own construction, not a published estimate.**
  - It moves the bottom 50% away from the source it claims to follow.
  - In the recent years it breaks the lower-bound logic the paper uses to justify the one-sided rich-list rule.
- **The page's "share of total growth" metric is broken whenever the total falls or barely changes.** This happens for every start year from 2020 to the 2024 end year.
- **The 2024 income headline (20.3% → 31.5%) carries no 2024 information.**
  - WID's 2024 pre-tax distribution is a copy of 2023.
  - Post-tax 2024 applies 2019 ratios.
  - The two shares rank different people.
- **The hero statement "the richest 0.001% held as much as the poorest 51.9%" is arithmetically right, but it is a point estimate of exactly the number the paper says must be read as a range.**
  - Across the paper's own scenarios it runs from 48.3% to 53.9%.
  - Under the lower scenario the statement reverses: the richest 0.001% would hold less than the poorest half.

---

## 1. Round-1 findings: are they resolved?

| # | Round-1 finding | Claimed fix (response.md) | Verdict | Evidence |
|---|---|---|---|---|
| C1 | Δshare × end-year total presented as euros "moved / lost / each" | Exact growth/share Shapley split; share of total growth; T(B) and T(E) valuations shown; vocabulary removed | **Partly** | The decomposition is correct. I reproduce growth €667bn and share effect −€403bn for the bottom 50% (1990–2024), and +€406bn share effect for the top 0.001% [json]. "Moved", "lost" and "each" are gone. Flow language remains: "7.7% **went to** the richest 0.001%" (abstract), "**received** 7.7%" (§5.2), "The top 0.001% **got** X% of that growth" (page). The price/volume split (round-1 fix 5) is still open. The paper's results section does not say that most of the €9.7tn is revaluation; only §3.5 of the method doc and the §7 limits say so. |
| C2 | Scenarios one-directional; 1 adult per family; neutral scenario hidden; DWA evidence not a scenario | 1.8 adults per member; `ggp_central` exposed; `dwa_lower` added; W_n vs list shown each year; one-sided rule justified | **Partly** | Units and exposure are fixed, and W_n / RL_adj are exported and tabulated. No gross-to-net or valuation haircut on Challenges (round-1 fix 5). `dwa_lower` is a problem in itself (§2.2). The one-sided rule is defensible by an order-statistic argument, but only if list valuations are net and correct (§2.3). |
| C3 | Forbes calibration from 1988; pre-1988 bases mix methods | Default 1990; 1988 marked; warning; jumps corrected; uncorrected series "open" | **Partly (acceptable as a stated limit)** | Correct as far as public data allow. The default 1990–2024 window still contains the 2013→14 Forbes coverage step (+1.00 pt). Removing that step alone lowers the top 0.001%'s "share of the rise" from 7.7% to 6.2% [json]. The paper should say this next to the 7.7%. |
| M1 | Top-bin threshold inconsistency over-read; α from p99.999 | "Thin" withdrawn; α from the chain p99.99→p99.998; jump shown; coherence test | **Holds** | Reproduced: €799M against €136M projected (×5.9), α_chain 1.90 [json]. The coherence test reports zero violations, but by construction it cannot detect this kind of threshold jump. The paper (§5.3 item 4) says the jump "most likely comes from refitting after the Forbes top-up". The same jump exists before calibration (×1.45 in 1980, ×1.75 in 1990 [json]), and the method doc says so. The paper should say so too, or drop "most likely". |
| M2 | IPP comparison mixes denominators; "4×" | Euros; dividend-imputed column; 2.7 / 1.7 / 1.13 / 0.87 | **Holds, with two caveats** | Reproduced exactly [json, csv]. (a) "Top 1% as a whole not understated" holds only for the 2025 "comprehensive" measure. IPP's own Note 92 (rev.) economic income gives 1.10× WID at the top 1% and 7.1× at the top 0.001% (219.4/198.8 and 64.95/9.19 €bn). The paper should say why Note 92 is set aside. (b) IPP's top 0.001% is 378 *foyers*. If most are couples, that is roughly 600–750 adults against WID's 507, which biases every IPP/WID ratio upward. The paper says "groups differ" but does not sign the bias. |
| M3 | Public-spending allocation misstated; 2019+ mechanical | Rules described; Fisher-Post & Gethin cited; 2019+ fixed ratios stated | **Partly** | The method doc and limits are now right. But the abstract, §5.2 and the page tile present 2024 post-tax and pre-tax shares as if observed (§2.5). Health is described two ways: "close to lump-sum" (paper, page) and "by a usage profile" (method §3.10). Pick one and source it. |
| M4 | Century series treated as one method; artifacts | Quality shading; breaks table; artifacts named | **Holds** | Shading is by `data_quality` for every year, and the breaks table is correct [raw]. Add 2010 to the named odd years: the bottom 50% goes 5.35 → 4.74 → 5.04% over 2009–11, and WID's top 10% jumps +1.7 pts in 2010 [json]. |
| M5 | Housing metric pre-tax, inconsistent, no financing | ERFS cash income per consumption unit; ECB rate annuity; files aligned | **Holds, with residual issues** | Paper, method §3.9, prices-housing.md and page now agree: 19 / 41 years, 155% / 236%, 8 / 13 years, 60% / 75% all reproduce [json]. Residual issues are in §2.6. |
| M6 | Page text contradicted controls | Method text rewritten | **Holds** | Method item "The very top" now describes the selector. |
| m1, m2 | CPI step at 1950; raw end years under smoothing | Fixed | **Holds** | `cpiFactor` holds the 1950 ratio; `smooth` uses two years at the ends. |
| m6 | Scenario mixing in growth tables | Note | **Partly** | `scenarioNote` lists the changed years. The decomposition still silently combines a WID start year with a scenario end year (§2.1). |
| m8 | DWA total exceeds WID despite narrower concept | Stated | **Open (acceptable as a limit)** | – |
| m10 | Tests check arithmetic only | 23 tests incl. coherence, oracle, paper numbers | **Mostly** | The paper-number test only checks that each generated string occurs *somewhere* in paper.md. A value such as "8" matches inside "8.9%". It does not check that numbers typed in the paper come from the data. "The test suite fails if the paper and the data disagree" (paper, last line) overstates it. |
| Round-1 §4.10 | Uncertainty range should include the vintage revision | Vintage table shown separately | **Partly** | The headline range "4.8% to 6.5%" excludes the largest source of uncertainty the paper documents: 0.9% vs 3.4% for 2014, by the same team. |

---

## 2. What is new since round 1

### 2.1 The growth/share decomposition and "share of total growth captured"

**The split is correct.** ΔW_L = s̄·ΔT + Δs·T̄ is the standard two-factor Shapley decomposition. It is exact and order-free (reproduced for all seven layers, 1990–2024 [json]).

**"Share of total growth captured" = ΔW_L / ΔT is ill-defined whenever ΔT ≤ 0 or ΔT is small relative to T.** This is not hypothetical: WID's real wealth total falls in the end years.

| Start → 2024 (wealth) | ΔT | Top 0.001% "captured" | Middle 40% "captured" | Bottom 50% "captured" |
|---|---|---|---|---|
| 2020 → 2024 | +€136bn | **234%** | **−53%** | −7% |
| 2021 → 2024 | −€720bn | **−11%** (it gained) | 39% (it lost €279bn) | 5% |
| 2022 → 2024 | −€890bn | **−8%** (it gained) | 39% (it lost €351bn) | 5% |
| 2023 → 2024 | −€212bn | **−24%** (it gained) | 46% (it lost €98bn) | 6% |

[json]: T = €14.52tn (2020), €15.38tn (2021), €15.55tn (2022), €14.87tn (2023), €14.66tn (2024).

- With a falling total, a layer that *gained* shows a negative "share of growth", and layers that lost show positive shares. The column then reads as a share of the loss, with the sign reversed for the top.
- `renderChange` guards the summary sentence with `dT > 0`, but the table column uses `dT ? pct(net/dT) : "n/a"`. For 2020→2024 the page therefore prints "The top 0.001% got **234%** of that growth". For 2021–2023 starts the table shows the reversed-sign values above.
- The same happens for any user-chosen window across 1913–1945 or 2007–2009.
- **Fix:** show the metric only when ΔT > 0 *and* ΔT is a material fraction of T (e.g. |ΔT|/T̄ > 10%). Otherwise print "n/a (total fell or barely moved)". Define the domain in §3.5.

**For wealth, the metric is mostly a revaluation exposure, not a receipt.**

- The wealth/income ratio rose from 3.26 (1990) to 5.81 (2024) [json: T_wealth / T_ptinc].
- The literature attributes most of such rises to relative asset prices. I have not decomposed this here.
- More importantly, WID France holds each group's 2014 asset mix fixed after 2014. This is quoted from WIL TN 2021/16 for the extension to 2020. For 2021–2024 in this vintage, the only statement is the project's method §3.11 and the quality flag 0. If, as the method doc states, the 2014 mix is held fixed through 2024, every share change after 2014 is mainly one of:
  - asset-class totals moving against fixed 2014 portfolios; or
  - the Forbes top-up.
- After 2014 the "share effect" therefore largely reflects relative asset prices and the calibration, not saving, mobility or behaviour. The paper lists the extrapolation as a limit but never draws this consequence for §5.2.
- **Fix:** add one sentence to §5.2 and the abstract saying so, and replace "went to / received / got" with "accrued to" or "of the increase in value, x% is in the slice …".

**Sensitivity of the headline 7.7% / 2.7%** (1990 → 2024; scenario applied to the end year only, as the page does) [json]:

| End-year assumption | Top 0.001% | Bottom 50% | Middle 40% |
|---|---|---|---|
| WID as published | 7.7% | 2.7% | 32.6% |
| `dwa_lower` | 6.5% | 3.7% | 39.6% |
| `ggp_low` | 9.0% | 2.7% | 32.1% |
| `no_cut` | 11.5% | 2.5% | 31.1% |
| WID without the 2013→14 jump | 6.2% | – | – |

- Scenarios exist only from 2004 or 2009. Every decomposition with an earlier start therefore compares a WID base with a scenario end year. That mixes methods, which the paper criticises WID for at 1988.
- The page should either refuse scenario decompositions whose start precedes the scenario's coverage, or print this caveat in the table.

**Minor.** §5.2 states two different counterfactuals in consecutive sentences:

- "had it kept its 1990 share … €866bn" is s_B·ΔT, a Laspeyres valuation;
- the Shapley growth effect, €667bn, uses s̄.

Using the start-share counterfactual in the paper reintroduces the valuation-year dependence the Shapley split was meant to remove. Pick one, or state both.

### 2.2 The ECB / Banque de France "dwa_lower" scenario

**What it does** (`build_data.py:285–297`):

- It sets WID's top-5% share to the DWA household top-5% share.
- It multiplies every g-percentile above P95 by one factor f_top: 0.856 in 2024, range 0.83–0.88 over 2009–2024.
- It multiplies everything below P95 by f_rest: 1.130 in 2024 [json].

**(a) The 4.8% is not anyone's estimate.**

- DWA publish nothing above the top 5% (docs/notes/dwa.md §1; Banque de France: "ne permettent pas … d'aller plus finement que le top 5 %").
- The top 0.001% value under `dwa_lower` therefore comes entirely from the uniform-scaling assumption.
- Where the 6.84-point 2024 gap is placed decides the answer:

| Where the top-5% gap is removed (2024) | Top 0.001% share |
|---|---|
| Entirely within p95–p99 | 5.6% (unchanged) |
| Uniformly above p95 (the scenario) | 4.8% |
| Entirely within the top 0.1% (13.34% → 6.50%) | ≈ 2.7% (€398bn), **infeasible** |

- The last row is ruled out by Forbes. WID's own calibration keeps the top g-percentile at or above the Forbes total (€631bn in 2024, 53 French citizens), which is a floor of 631 / 14,657 ≈ 4.3% of wealth [json, csv].
- At the DWA top-5% level, the feasible range for the top 0.001% is therefore roughly 4.3–5.6%. The uniform 4.8% sits near the Forbes floor. It is one point in that interval, chosen by assumption.
- The paper and abstract call the range "alternative estimates … under published assumptions". For the lower end that is not accurate.
- The scenario should be labelled "WID rescaled to the DWA top-5% share (uniform above P95; our assumption)", and the abstract wording changed.

**(b) It moves the bottom 50% away from DWA.**

- Scaling all of the bottom 95% by f_rest raises the bottom 50% from 4.84% to 5.47% in 2024. DWA's published value is 5.00% [json].
- The paper's own claim that WID and DWA agree on the bottom half (−0.6 to +0.4 pts) is thus violated *by the scenario that claims to follow DWA*.
- A DWA-consistent scenario should match the published DWA bottom-50, top-10 and top-5 shares jointly. All three are available.

**(c) It is inconsistent with the paper's own rule that a rich list is a lower bound.**

The paper justifies the one-sided rich-list rule by saying a list is a lower bound on what the richest n adults hold. Applying that logic to `dwa_lower` [json, csv]:

- **At 900 adults (1 member per family, 1.8 adults):** `dwa_lower` puts the richest 900 below Challenges × 0.8 in 12 of the 13 list years from 2009 on (all but 2014). In 2024 it is €735bn against €994bn.
- **At DWA's own family split:** DWA's default is 4 households per family (docs/notes/dwa.md §4). At 1.66 adults per household that is about 3,300 adults.

| Year | dwa_lower, top 3,320 | top 4,000 | top 5,000 | Challenges × 0.8 |
|---|---|---|---|---|
| 2019 | €645bn | €673bn | €710bn | €652bn |
| 2020 | €626bn | €655bn | €694bn | €660bn |
| 2022 | €821bn | €851bn | €890bn | €869bn |
| 2023 | €840bn | €869bn | €907bn | €967bn |
| 2024 | €879bn | €907bn | €945bn | €994bn |

- In 2023–2024 the scenario falls below the Challenges list even at 5,000 adults.
- Either the list is not a lower bound (and then the one-sided rule loses its justification), or `dwa_lower` is infeasible in recent years.
- The only escape is that DWA's own "valuation differences from ESA 2010" adjustment cuts Challenges by more than about 12%. The project does not know whether it does.
- This must be stated next to the scenario.
- Against Forbes the scenario is feasible:
  - 2024: €700bn for the top 0.001% vs €631bn for 53 French citizens.
  - 2022: €630bn vs €566bn.
  - 2021: €637bn vs €503bn.

**(d) The two "directions" are not independent.**

- DWA's French top tail is a Pareto fit on the HFCS plus, probably, the Challenges list (WP 2687 Table 1; dwa.md §6).
- The rich-list scenarios use the same list.
- The "range in both directions" is therefore largely one list under different family-size and valuation assumptions. The upper end (`ggp_low`, 6.5%) assumes 1 member per family; the lower end implicitly assumes large families. These are mutually exclusive premises.
- That is legitimate for an envelope, but it is not two independent sources bracketing WID. The paper's §1 principle 3 ("uncertainty in both directions") should say so.

**(e) Households vs adults.**

- The scenario applies a household share (1.66 adults per household in 2024) to an equal-split adult distribution without adjustment.
- docs/notes/dwa.md correctly declines to sign the bias. The paper mentions "households vs adults" only in the method doc.
- Acceptable as a limit, but it belongs in the paper's §4 and §7.

### 2.3 Rich-list scenarios from article-quoted Challenges totals (2004+)

- **Data.**
  - 16 years with a quoted euro total (2004, 2006–07, 2009–10, 2012–14, 2016–20, 2022–24 in the build). The 2012 total is from a blog repost and 2013 is flagged "CONFLICT".
  - The ±3% statement is fair.
  - Gaps in 2005, 2008, 2011, 2015 and 2021 revert to WID in `C()`, so scenario series zig-zag. For example, `no_cut` goes 5.22% (2020) → 4.78% (2021, WID) → 6.59% (2022) [json].
  - "8 years corrected (2016–2024)" reads as contiguous, but 2021 is not corrected.
  - **Fix:** interpolate the list total in log terms for missing years, or mark scenario gaps on every chart.
- **Members × 1.8 adults.**
  - Correct conversion of GGP's "80% married, equal split".
  - The paper's `ggp_low` (1 member) is the extreme of GGP's 1/10/15 range. For an average over 500 "families" that include multi-heir dynasties (the 2025 No. 1 entry is "the numerous members of the Hermès inheriting families", per `challenges_500.csv`), 1 member is not plausible.
  - Calling 6.5% the top of a range "under published assumptions" is formally correct, but GGP's own conclusion was that the corrected list (10–15 members) is consistent with their benchmark. The paper should say this.
- **The one-sided rule.**
  - It is defensible by an order statistic: the true top-n adults hold at least what any n adults hold. That is a better justification than the current wording, and should replace it.
  - It is a lower bound only if the list's valuations are *net, resident, and not inflated*. rich-lists.md itself says gross valuation, family grouping and market pricing push Challenges *up*, and no haircut is applied.
  - So `ggp_low` is "a floor conditional on 1 member per family and accurate net valuation", not an upper estimate.
  - The abstract's "range from 4.8% to 6.5%" invites reading 6.5% as an upper limit. Under the paper's own logic there is no upper limit from the list.
- **For transparency, report the symmetric reading once.**
  - Under central assumptions (9,000 adults) the list is *below* WID every year: €994bn vs €1,235bn in 2024 [json].
  - Read as a point estimate rather than a floor, it would put the top 0.001% at about 4.5% (5.58% × 994/1,235).
  - The page already shows W_n against RL; the paper does not.
- **Within-bin assumption.**
  - §4 says the scenarios need "no assumption about the shape inside that bin". In fact W_900 splits the p99.998–p99.999 g-percentile uniformly (370 of 530 adults).
  - This slightly understates W_n and so slightly favours correction. The magnitude is negligible (≈ €2bn), but the sentence is wrong as written.

### 2.4 Hero: "the richest 0.001% held as much as the poorest 51.9% of adults"

**The computation is correct.**

- My independent recomputation from the 127 g-percentiles gives 51.87% [json].
- `PieCore.poorestHolding` and `paper_numbers.py` both add negative bins to the running total before testing, which is the right treatment.
- In WID 2024 only p0–p1 is negative (average −€421). Flooring it at zero changes the result in the fourth decimal.
- The cumulative share of the poorest 20% is 0.16%, of the poorest 30% 0.60%, and of the poorest 50% 4.84%.

**Fairness.** Three issues.

1. **It is a point estimate of the least certain number in the paper.** Because the Lorenz curve near p50 adds only about 0.29 pts of wealth per percentile, the result moves a lot with the top share:

   | 2024 assumption | Top 0.001% share | "Poorest X% hold as much" |
   |---|---|---|
   | `dwa_lower` | 4.77% | **48.3%** |
   | WID | 5.58% | 51.9% |
   | `ggp_low` | 6.45% | 53.9% |
   | `no_cut` | 8.07% | 57.4% |

   Under the lower scenario the claim reverses: the richest 0.001% hold *less* than the poorest half. §5.3 concludes "we report the very top as a range, not a point". §5.2 then states 51.9% unhedged.

2. **It is not stable over time for reasons the paper itself flags.** It was 14.8% (1980), 23.4% (1990), 45.4% (2014) and 51.9% (2024) [json]. The rise crosses the 1988 calibration and the 2014 Forbes coverage step.

3. **The page caption is half wrong.** It adds "many of whom own very little or owe more than they own". "Own very little" is right. "Owe more than they own" applies to about 1% of adults in WID's g-percentiles.

**Fix:**

- In the paper, state the 48–54% range alongside 51.9%, or drop the sentence from §5.2.
- On the page, append the scenario range to the caption as `heroRange` already does for the share.
- Drop "owe more than they own" or quantify it.

### 2.5 "Share of income before tax 20.3% → after taxes and public services 31.5%" for the poorest half

**Units are comparable.**

- Both series are shares of national income.
- Pre-tax and post-tax totals are identical in every year checked (e.g. €2,521bn in 2024) [json].
- The ratio is a legitimate DINA statistic.

**But three things are not said.**

1. **2024 carries no 2024 information.**
   - WID's 2024 pre-tax distribution is a copy of 2023: all seven layer shares are identical to six decimals, and `sptincj992 p0p50` is 0.203 in both years [raw].
   - Post-tax 2019–2024 is pre-tax × fixed 2019 ratios (WID metadata).
   - Oddly, post-tax 2024 (31.54%) differs from post-tax 2023 (31.60%) although pre-tax is identical. That is unexplained by the stated method and worth a note.
   - The last year with independent information is 2018: pre-tax 20.3%, post-tax 31.9% [json].
   - **Fix:** quote 2018, or label 2024 "extrapolated" wherever it appears. That covers the abstract, §5.1's "0.88% of pre-tax income in 2024", §5.2 and the page tile.
2. **Different people.** Pre-tax shares rank adults by pre-tax income, post-tax by post-tax income. "Raise the poorest half's share" suggests one group lifted. It compares two differently ranked bottom halves, and re-ranking alone pushes the post-tax bottom share up relative to a fixed-rank measure. Say so.
3. **What "benefits" means here.**
   - Pre-tax income already includes pensions and unemployment insurance. The 20.3 → 31.5 step excludes the largest French transfer.
   - It includes collective expenditure (defence, police, etc.) attributed in proportion to disposable income.
   - Spell this out in §5.2, not only in §2.
4. **Comparison year.** §5.2 compares WID 2024 (31.5%) with INSEE's distributed accounts 2019 (38%). The like-for-like WID 2019 value is 32.1% [json]. Use it.

### 2.6 Housing (ERFS per consumption unit; DVF back-cast)

- **Reproduced:** 18.9 / 41.1 years (Paris, 1996 / 2023), 155% / 236% repayment (2000 / 2023), 7.8 / 13.0 years and 60% / 75% outside Île-de-France [json]. The four documents now agree.
- **Single person, 70 m².**
  - The denominator is income per consumption unit: a person living alone.
  - A two-adult household in the bottom half has 1.5 CU or more, so its burden is a third lower or less. A couple with two children has 2.1 CU, so its burden is less than half.
  - The page says this; the paper's "for one person in the poorer half" does not explain it.
  - The headline 236% is for a single low-income person buying a family-sized flat in Paris. That is a stylised upper case, not a typical household.
- **National incomes against Paris prices.** The incomes are national ERFS tenths, not Paris residents. State it.
- **Trend shape.** The 2000 → 2023 contrast hides that the Paris repayment share peaked at 271–272% in 2011–12 and was 208–236% from 2014 to 2023 [json].
  - Years of income peaked at 48 in 2020–21 and fell to 41 in 2023 as prices fell about 10% from 2021 to 2025.
  - Neither endpoint is cherry-picked; 1996 is the first ERFS year, and also the trough of Paris prices (€2,528/m² vs €3,225 in 1992).
  - But the paper should say most of the rise in the repayment burden happened by 2008–2012.
- **The DVF back-cast is reasonable and honestly caveated.**
  - A 2025 mean is carried back with a constant-quality index, which yields constant-2025-composition prices.
  - DVF is 1.9–4.7% above Notaires in Paris.
- **ECB MIR 2000–2002 observations are flagged `E` (estimated)** in the raw file [raw]. The series is stated as "2000–" without that flag.
- **ERFS is spliced at breaks** (2010, 2012, 2020) by keeping the newer method. The project explicitly refuses to splice ERFS in the cross-check charts. Use the same rule, or justify the difference. The level effect here is small: 2009 → 2010 bottom half €13,587 → €13,575.
- **"Prices by income decile rose at similar rates … so housing, not general inflation, is where purchasing power diverged" is not supported.**
  - The CPI excludes house purchase prices, so equal CPI growth by decile says nothing about housing.
  - The ERFS incomes of the bottom half and the middle 40% grew almost identically over 1996–2023 (×1.924 and ×1.914; top 10% ×2.144) [json]. The housing burden therefore rose about equally for both groups.
  - What diverged is incomes against prices, and owners against non-owners. Neither is measured here.
  - **Fix:** rephrase as "housing prices rose far faster than incomes in every group".
- **Pre-committed spending, 13.4% → 30.3% (1959–2025):** reproduced. It is a national-accounts concept including imputed rents. The last year is provisional national accounts.

---

## 3. The paper as a scientific document

### 3.1 Claims not supported, or contradicted, by the project's own data

1. **"The bottom and middle of the distribution are robust across sources"** (abstract; method §3.10 "Reading").

   | Middle 40% wealth share | WID | DWA | Gap |
   |---|---|---|---|
   | 2009 | 38.0% | 44.0% | −6.0 |
   | 2014 | 36.3% | 41.5% | −5.2 |
   | 2024 | 35.3% | 40.6% | −5.3 |
   | Range 2009–2024 | | | −4.7 to −6.8 every year |

   [json]
   - That is the same size as the top-5% gap. docs/notes/dwa.md says "the middle 40% mirrors that gap"; the paper does not.
   - For the bottom 50% the *levels* agree. The *trend* does not: over 2009–2014 WID falls from 5.35% to 4.99% while DWA rises from 4.99% to 5.60%.
   - The defensible claim is: "levels agree for the bottom 50%; the middle 40% and the top 5% differ by 5–7 points in opposite directions; trends since 2009 agree in direction for the top 10% and the middle 40%."
   - This matters for the headline. The middle 40%'s 32.6% share of the rise, and its −5.2-point share change since 1990, rest on WID's allocation between the middle and the top, which is exactly where DWA disagrees.
2. **"The paper reports ranges rather than single numbers there"** (abstract), yet two of the four quantitative sentences in the abstract are point values for the very top: 7.7%, and implicitly 51.9% (§5.2). Their ranges are 6.5–9.0% (or 6.2% without the 2014 step) and 48–54%.
3. **"Alternative estimates … under published assumptions"** for 4.8%: see §2.2(a).
4. **Robustness, start year** (§6). "The poorest half's share fell from every start year between 1966 and 2009, and rose from starts before 1966" is inaccurate in both directions [json].
   - It fell from 1961 and 1963.
   - It fell from every start year 2011–2023; only 2010, an odd WID year, is an exception.
   - The middle 40% fell from 1971–1997 *and* 2002–2023; it rose only from 1998–2001.
   - `paper_numbers.fell_range` reports the longest run only, which truncates the result. Report the full sets.
5. **"So housing, not general inflation, is where purchasing power diverged":** see §2.6.
6. **"WID therefore likely understates the income of the very top, not of the top 1% as a whole":** this depends on the IPP measure chosen (§1, M2).
7. **The top-bin jump "most likely comes from refitting after the Forbes top-up":** the jump predates the calibration (§1, M1).

### 3.2 Framing

The direction of the framing is now broadly balanced. The level chart, the "both statements are true at once" sentence and the vintage tile are good. Remaining issues:

- **Flow language for revaluation:** "went to", "received", "got" (abstract, §5.2, page).
- **Table 2 is incomplete.** It prints "–" for the top 1% in 1950, 1990 and 2014. The values exist: compute them or drop the column's empty cells.
- **Missing counter-evidence in the paper:**
  - the DWA middle-40% gap;
  - the symmetric reading of the central rich-list scenario (≈ 4.5%);
  - IPP Note 92's larger ratios;
  - the fact that WID's real wealth total *fell* in 2022–2024, all extrapolated years.
- **§8 and the page say a "second round on version 0.4" exists**, with reports in docs/reviews. response.md is still headed "version 0.2 → 0.3" and the method doc says "Version 0.3". Align the version labels.

### 3.3 Limitations section: what is missing

§7 is honest but incomplete. Add:

1. WID and DWA disagree by 5–7 points on the middle 40% as well as the top 5%.
2. DWA's French top tail and the rich-list scenarios likely share the Challenges list, so they are not independent.
3. Pre-tax and post-tax shares rank different people.
4. WID's 2024 pre-tax distribution is a copy of 2023; post-tax 2019–2024 uses 2019 ratios.
5. After 2014, wealth share changes are mechanical: fixed 2014 portfolios plus the Forbes top-up.
6. "Share of total growth" is undefined when the total falls or barely moves.
7. Scenarios cover 2004+ or 2009+ only; decompositions from earlier bases mix methods.
8. Challenges is gross, family-level and market-priced, with no haircut.
9. Housing: single-person consumption unit; national incomes against Paris prices; mortgage rates estimated before 2003.
10. No sampling or model uncertainty is available from WID; the "ranges" are assumption envelopes, not confidence intervals.

---

## 4. Numerical checks

| Item | Paper | Recomputed | Status |
|---|---|---|---|
| Top 0.001% wealth 1980 / 1990 / 2014 / 2024 | 0.80 / 1.4 / 3.4 / 5.6% | 0.80 / 1.44 / 3.39 / 5.58% | OK |
| Bottom 50% 1990 / 2024; avg | 8.9 / 4.8%; €21,100 / €26,800 | 8.94 / 4.84%; €21,066 / €26,775 | OK |
| ΔT 1990–2024 | €9.7tn | €9.687tn (4.970 → 14.657) | OK |
| Captured, top 0.001% / bottom 50% | 7.7 / 2.7% | 7.70 / 2.73% | OK, but see §2.1 |
| Bottom 50% net; at-start-share counterfactual | €265bn; €866bn | €265bn; €866bn | OK |
| Scenarios 2024: dwa / central / low / no cut | 4.8 / 5.6 / 6.5 / 8.1% | 4.77 / 5.58 / 6.45 / 8.07% | OK |
| Years corrected, low / no cut | 8 / 14 | 8 (2016–20, 2022–24) / 14 | OK; not contiguous |
| Top-bin threshold vs projected | €799M / €136M / 5.9 | €798.7M / €136.1M / 5.87 | OK |
| Poorest equivalent | 51.9% | 51.87% | OK; range 48.3–53.9% |
| Pre / post-tax bottom 50% 2024 | 20.3 / 31.5% | 20.30 / 31.54% | OK; 2024 pre-tax = 2023 copy |
| DWA top-5% gap; bottom-50% gap | 5.8–7.6; −0.6 to +0.4 | 5.87–7.59; −0.61 to +0.36 | OK |
| DWA middle-40% gap | not reported | −4.7 to −6.8 | **Missing** |
| IPP ratios | 0.87 / 1.13 / 1.7 / 2.7 | 0.866 / 1.131 / 1.669 / 2.664 | OK |
| Housing figures | 19 / 41; 155 / 236%; 8 / 13; 60 / 75% | same | OK |
| Challenges ÷ WID top 0.01% (method doc) | 0.49 → 1.11 | 0.495 → 1.114 | OK |
| CPI vs deflator 1980 | "about 6%" | 6.35% (level 6.8% higher) | OK |
| Smoothing: top 0.001% 2024 | 5.58 → 5.37% | 5.58 → 5.37% | OK |
| Start-year robustness | "fell 1966–2009; rose before 1966" | fell 1961, 1963, 1966–2009, 2011–2023 | **Inaccurate** (§3.1.4) |

No headline number is arithmetically wrong. The errors are about what the numbers are said to show.

---

## 5. What a journal referee would still require

### 5.1 Must fix before the repository is published

1. **Withdraw "the bottom and middle are robust across sources."**
   - It appears in the abstract and in method §3.10.
   - Report the WID–DWA middle-40% gap (−4.7 to −6.8 pts) in §5.3 and §7.
   - Restrict the agreement claim to bottom-50% levels.
2. **Fix the "share of total growth" metric on the page and in §3.5.**
   - Suppress it ("n/a") when ΔT ≤ 0 or ΔT is small relative to T.
   - Today the page prints "the top 0.001% got 234% of that growth" for 2020→2024.
3. **Relabel and qualify `dwa_lower`.**
   - It is the project's uniform-scaling assumption, not a published DWA estimate. Remove "under published assumptions" for the 4.8%. At the DWA top-5% level, anything between about 4.3% (the Forbes floor) and 5.6% is feasible.
   - State that it raises the bottom 50% above DWA's own value (5.47% vs 5.00%).
   - State that it falls below the Challenges list in 2023–2024 even at 5,000 adults, which contradicts the paper's lower-bound argument unless DWA haircuts the list.
   - Preferably rebuild it to match DWA's bottom-50, top-10 and top-5 shares jointly.
4. **Stop presenting very-top-dependent statistics as points in the abstract and §5.2.**
   - Give "poorest 51.9%" its range: 48–54%, reversing under the lower scenario.
   - Give the 7.7% its range: 6.5–9.0%, or 6.2% without the 2014 coverage step.
   - Replace "went to / received / got" with neutral wording.
   - Add one sentence saying the wealth rise is largely revaluation, and that post-2014 share changes are mechanical in WID.
5. **Label the 2024 income figures as extrapolated, or use 2018.**
   - 20.3% → 31.5%, and 0.88%.
   - Say that pre-tax and post-tax bottom halves are different people.
   - Compare WID 2019 (32.1%) with INSEE 2019 (38%).

### 5.2 Should fix (wording, errors that do not change the headline)

- Correct the start-year robustness sentence; report full sets, not the longest run.
- Rephrase the housing/CPI "purchasing power diverged" inference.
- State the single-person / national-income construction of the housing metric in the paper.
- Mention the 2011–12 peak of the repayment share.
- Flag ECB MIR 2000–02 as estimated.
- IPP:
  - say why Note 92 is set aside (it gives 1.10× at the top 1%);
  - sign the foyer-vs-adult bias.
- Top-bin jump: say it predates the calibration (×1.45 in 1980).
- Fix the scenario gaps (2021 etc.): interpolate, or mark them on charts.
- Restate the one-sided rule as an order-statistic bound conditional on net valuation. Report the symmetric reading of the central rich-list scenario once (≈ 4.5%).
- Fix §4's "no assumption about the shape inside that bin" (the p99.998–p99.999 bin is split uniformly).
- Complete Table 2.
- Health allocation: use one description, sourced.
- Hero caption: drop "owe more than they own" (≈ 1% of adults).
- Paper-number test: it checks presence only. Soften "the test suite fails if the paper and the data disagree".
- Align version labels (paper 0.4, response "0.2 → 0.3", method "0.3").

### 5.3 Acceptable as stated limitations

- No WID uncorrected (pre-Forbes) France series; the vintage comparison stands in.
- No price/volume decomposition of wealth changes (planned §3.13), *provided* the results section says the rise is mostly revaluation.
- Households vs adults in DWA; direction unsigned.
- Challenges ±3%; July valuation; 20% non-resident share held constant over 2004–2024.
- DWA–WID total-wealth discrepancy (round-1 m8).
- Equal-split adult unit; ageing; one national deflator.
- ERFS splices at method breaks (small here), if stated.
- DVF back-cast level bias of a few percent.

---

## 6. What is done well

- The Shapley split is exact and well explained. The page shows the start- and end-year valuations side by side.
- The scenario plumbing is transparent:
  - `rich_list_check` exports W_n and RL_adj every year;
  - the page table makes it visible when the list does *not* bind;
  - the neutral central scenario is selectable.
- All 66 paper numbers regenerate from the committed data. The DWA, IPP and housing reconciliations are carefully documented in the notes.
- docs/notes/dwa.md is a model of a cross-check note. It gives:
  - concept, unit and timing differences;
  - frozen-household caveats;
  - a refusal to sign effects it has not measured.

  Most of the must-fix items above amount to carrying that note's honesty into the abstract.
