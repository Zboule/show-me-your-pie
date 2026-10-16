# Referee report: methodology and results of "Show Me Your Pie" (v0.1)

Reviewer brief: a deliberately harsh review of the methodology and results, written from the standpoint of distributional national accounts (DINA), top-income and wealth measurement. Date: 2026-10-16.

How numbers were obtained. Unless stated otherwise:

- **[json]** means computed from `site/data/france.json` (build dated 2026-10-16).
- **[raw]** means computed from `data/raw/WID_data_FR.csv` or `WID_metadata_FR.csv`.
- **[csv]** means computed from `data/manual/*.csv`.
- **[src]** means quoted from an external source, cited inline.
- Money is in constant 2025 euros unless marked "nominal".

---

## 0. Summary verdict

The engineering is careful. The documentation is unusually candid, and the bottom and middle of the distribution are handled sensibly. But on its two headline claims, the project does not yet meet the author's own standard of "no bias".

**1. The "transfer" framing is not a measurement of transfers.**

- Δshare × end-year total is a share-gap valuation. For wealth it is driven largely by:
  - asset revaluation;
  - the year chosen to value it in;
  - since 1988, very likely a mechanical rich-list calibration inside WID.
- The page turns that number into "moved", "changed layer", "lost" and "€1.3bn each".
- Example: the bottom 50% is shown as having "lost" €529bn of wealth since 1980. Over the same period its real wealth per adult rose about 61% [json].

**2. The top-tail machinery is one-directional.**

- Every alternative the reader can select *raises* the top. The neutral scenario built on GGP's own parameters is computed and then hidden.
- The rule "never lower WID" is hard-coded and enforced by a unit test.
- Evidence that WID may *overstate* the top is set aside rather than turned into a scenario: the ECB/Banque de France DWA put the top 5% 6–7 points lower.
- Evidence that WID *understates* the top becomes a selectable scenario: Challenges, and IPP.
- The scenarios also assume 1 adult per family, which is below GGP's own floor of about 1.8 equal-split adults per family member and implausible as an average across 500 families.

**3. Several cross-source conclusions printed on the page do not survive an apples-to-apples check:**

- the IPP "WID matches taxable income / comprehensive income is 4×" claim;
- the claim that WID allocates public spending "in proportion to income";
- the "Forbes sits inside WID's top 0.001%" reading.

**4. The WID series is treated as more homogeneous than it is.** Inside 1900–2024 there are:

- method breaks: Forbes calibration probably from 1988, a fixed-portfolio extrapolation after 2014, and post-tax income from a different research programme;
- visible artifacts in the top bin: sawtooth years, and a duplicated year.

None of these is flagged on the page except the trailing extrapolation.

**Recommendation: major revision.** The project should not be published with the current wording of the hero tiles, the transfer section, the "very top" section, the IPP section and the cross-check notes.

---

## 1. Critical findings

### C1. The "transfer" metric is labelled as a flow of euros between groups; it is a valuation-year-dependent share gap

**What.** The measure is transfer_L = (s_L(E) − s_L(B)) × T(E). The page renders it as:

- "Moved to the top 0.001%" (site/index.html:580);
- "€X … changed layer" (site/index.html:639);
- "€… each" per member;
- bars coloured gain/loss under the aria-label "Euros gained or lost by each layer".

**Evidence** (wealth, 1980 → 2024) [json]:

| Layer | Δshare × T(2024) | Real growth of avg per adult, %/yr | Real wealth per adult 1980 → 2024 |
|---|---|---|---|
| Bottom 50% | −€529bn ("lost") | +1.09% | €16.6k → €26.8k (+61%) |
| Middle 40% | −€692bn ("lost") | +2.08% | ≈ ×2.5 |
| Top 0.001% | +€701bn (€1.32bn "each") | +7.0% | €78.7M → €1,544M |

**Decomposition the page should show.** A layer's change in holdings splits as ΔW_L = s_L(B)·ΔT + Δs_L·T(E). That is a growth effect plus a distribution effect.

| Layer | Growth effect | Distribution effect (page's "transfer") | Net change |
|---|---|---|---|
| Bottom 50% | +€920bn | −€529bn | +€391bn (€318bn → €709bn) |
| Top 0.001% | +€87bn | +€701bn | +€788bn |

**Valuation year.** The real total rose 3.9× (€3.77tn → €14.66tn) [json], so the euro figure depends mostly on which year's total is used:

| Valued at | Top 0.001% "transfer" |
|---|---|
| T(1980) | ≈ €180bn |
| Midpoint total | ≈ €440bn |
| T(2024), the page's choice | €701bn |

Much of T's growth is plausibly asset revaluation, housing in particular [literature, not decomposed here]. If so, for wealth the euro amount is largely a price effect applied to a share change.

**The "changed layer" total.** The headline "€1,540bn … changed layer" equals ½·Σ|Δs|·T(E). That is a dissimilarity (Hoover-type) index of two share vectors, scaled by T. Nothing "changed layer".

**Anonymity.** Layers are anonymous and their sizes change: 382 adults in the top 0.001% in 1980, 530 in 2024 [json]. So "€1.32bn for each of its 530 members" divides a share gap by people, most of whom were not in the group in 1980. docs/03-method.md:95 admits "This is a counterfactual on shares, not a claim that euros were taken". The page wording contradicts that caveat.

**Why it matters.** This is the project's signature number, and the wording invites a zero-sum reading: the rich took €X from the bottom. The data do not support that reading. In wealth, the bottom half's absolute position improved, and the top's gain is mostly revaluation plus calibration (see C3).

**Fix.**

1. Rename the measure "share-gap valuation" or "euros at constant shares". Drop "moved", "changed layer", "gained/lost" and "each".
2. Show the two-term decomposition per layer: growth effect and distribution effect.
3. Show the T(B) to T(E) range, or use the midpoint (Shapley) valuation.
4. Add "share of aggregate real growth captured" per layer. For wealth 1980–2024 [json]: bottom 50% 3.6%, middle 40% 33.6%, top 0.001% 7.2%. For pre-tax income: bottom 50% 18.1%, top 0.001% 1.3%. This number can be read correctly by a lay reader.
5. For wealth, separate price effects from volume/saving effects, at least for the top 1% using WID's asset composition (GGP 2021 do exactly this). Until then, say on the page that wealth "transfers" mostly reflect relative asset-price changes.

### C2. The rich-list scenario tooling can only raise the top, and its most-advertised settings fall below the literature's unit floor

**Neutral scenario hidden.** The only alternatives offered are `concentrated` and `upper` (site/index.html:150–154). `spread`, with GGP's central parameters (10 members per family, 20% non-resident), is computed by `pipeline/top_tail.py` but cannot be selected. It changes 0 years: WID's richest ~5,000 adults always hold more than 80% of the Challenges total [json, `scenarios.corrected_years.spread = []`].

**Never lower WID.**

- `scenario_shares` returns None whenever RL_adj ≤ W_n (pipeline/top_tail.py:76–77).
- The rule is stated at docs/03-method.md:197 and enforced by `test_scenarios_never_lower_the_top`.
- The scenario series is therefore max(WID, RL). The maximum of two noisy estimates is biased upward relative to either one.

**Unit error in k.** GGP's appendix H, as transcribed in `data/manual/ggp_richlist_comparison.csv`, uses 1/10/15 *members* per family and 80% of members married, with married members "split into two adults". Under WID's equal-split unit, one member is therefore about 1.8 adults on average. A single unmarried billionaire is exactly one adult, so k = 1 is not impossible for one family. As an average over 500 families, many of them multi-member dynasties (e.g. the Hermès heirs), it is implausible, and it is below GGP's own floor of about 1.8. docs/03-method.md:206 claims these are "the values Garbinti, Goupille-Lebret & Piketty use"; they are not.

**Sensitivity**, re-running `top_tail.scenario_shares` with other k values [json + raw]:

| Adults per family | Non-resident cut | Years corrected | Top 0.001% share 2024 |
|---|---|---|---|
| 1 (page "concentrated") | 20% | 16 | 6.95% |
| 1.8 (GGP minimum) | 20% | 9 | 6.46% |
| 1.8 | 0% | 21 | 8.07% |
| 4 adults (below DWA's ≈ 7) | 20% | 3 | 5.84% |
| 7.2 (DWA default: 4 households × ~1.8) | 20% | 0 | 5.58% (= WID) |
| 7.2 | 0% | 8 (2017–2024) | n/a |
| 10 (GGP central) | 20% | 0 | 5.58% (= WID) |

**Concept mismatches left unadjusted.** Challenges is gross professional wealth of families, at July market prices, including non-residents. WID is net personal wealth per equal-split adult. The direction of the gross/net and listed-valuation effects is upward for Challenges, and no liquidity discount is applied.

**Asymmetric treatment of evidence.** On the page:

- Challenges (top higher than WID) becomes a selectable scenario.
- DWA (top 5% 5.8–7.6 points lower than WID every year 2009–2024, docs/notes/dwa.md:197–201) and HVP (top 1% about 11 points lower) remain annotations. No "WID too high" scenario exists.

**Why it matters.** The author's goal is "no bias … without underestimating the very top". As built, the tool cannot express the possibility that the top is *overstated*, and its default alternatives sit above the published literature's most extreme parameter set.

**Fix.**

1. Expose all scenarios, including `spread`, and make the default comparison GGP-consistent: members × 1.8 equal-split adults.
2. Allow downward corrections (symmetric rule), or at least show W_n / RL_adj each year so the reader sees when the list is below WID.
3. Add a "DWA-consistent" lower scenario for the top 5%, or state explicitly why none is offered.
4. Label k = 1, c = 0 as "outside the parameter range of the literature", not "upper bound".
5. Apply a gross-to-net and valuation haircut range: Forbes/DWA practice, and DWA's "valuation differences from ESA 2010".

### C3. WID's Forbes calibration very likely starts in 1988, not 2014, so the default 1980 → 2024 comparison crosses a method break inside WID itself

**WID's note.** WIL Technical Note 2025/01 (Bajard et al. 2025, pp. 4–5, downloaded and read) [src]:

- "We harmonize historical billionaire sources published by Forbes between 1988 and 2024."
- "In cases where WID billionaire wealth is lower than Forbes, we add to the 127th g-percentile … the difference."
- "The same amount is subtracted proportionately to each group of the bottom 99.999%."
- "From this modified distribution, we compute new shares and bracket averages after fitting them through gpinter again."
- Figure 2 covers France, 1980–2024.
- The note says "our raw uncorrected estimates for countries like France … significantly underestimate billionaire wealth".

**WID's top 0.001% wealth share, with jumps** [json]:

| Years | Share | Note |
|---|---|---|
| 1987 → 1988 → 1989 | 0.74 → 1.17 → 1.45 | first Forbes year |
| 1998 → 1999 | 2.26 → 3.44 | +1.18 pts |
| 2013 → 2014 | 2.39 → 3.39 | +1.00 pt; a data_quality = 4 ("observed") year |
| 2020 → 2021 | 3.44 → 4.78 | +1.34 pts |

**What the project says.**

- The page hero (site/index.html:137), the method text (docs/03-method.md:102–109) and docs/01-concepts.md:141–143 present the Forbes lift as a post-2014 feature.
- docs/03-method.md:106–109 says the "two largest one-year jumps" are 2013–14 and 2020–21. That is false: 1998–99 (+1.18) exceeds 2013–14 (+1.00).

**After 2014, almost all of the top's rise is the top g-percentile.** Over 2014–2024 [json]:

| Layer | Share 2014 → 2024 |
|---|---|
| p99.99–p99.999 | 2.05 → 2.03 |
| p99.9–p99.99 | 5.79 → 5.73 |
| p99–p99.9 | 14.56 → 14.34 |
| Top 0.001% | 3.39 → 5.58 |

The layers just below hold similar, business-heavy portfolios and are flat. So the +2.19 points (≈ €321bn of the €701bn tile) are best read as the Forbes top-up, not asset prices.

**Why it matters.**

- The tile "Top 0.001% · 0.8% → 5.6%" compares an uncalibrated 1980 base with a Forbes-calibrated 2024 end year.
- The project warns about exactly this problem for its own scenarios ("comparisons with earlier start years under a scenario mix two methods", docs/03-method.md:209). It applies the warning to its own add-on but not to WID.
- The calibration also mechanically lowers every other layer, including the bottom 50%, in proportion.

**Fix.**

1. Obtain WID's uncorrected France series (from the authors, or by digitising Figure 3 of the technical note) and show both.
2. Flag 1988–2024 as "rich-list calibrated" wherever the top 0.001% wealth share is used.
3. Never put a pre-1988 base year against a post-1988 end year for the top 0.001% without a printed caveat.
4. Correct docs/03-method.md:106–109.

---

## 2. Major findings

### M1. The top g-percentile is internally inconsistent, and the project draws a substantive conclusion from the inconsistency

**The jump in thresholds.** The p99.999 threshold is far above what the bins below imply [raw]:

| Year | Threshold p99.998 | Threshold p99.999 | Avg of p99.998–p99.999 | Ratio threshold(p99.999) / avg of bin below |
|---|---|---|---|---|
| 1980 | €22.1M | €50.4M | €26.6M | 1.9× |
| 2000 | €86.8M | €286M | €104M | 2.75× |
| 2024 | €94.5M | €799M | €112M | 7.1× |

- The jump is therefore present in every year, not only since the 2025 update.
- The chain of thresholds below p99.998 is smooth. From p99.99 to p99.998 (a factor 5 in rank), the threshold rises €40.5M → €94.5M, a local Pareto α ≈ 1.9.
- Continuing at that α to p99.999 gives about €137M, not €799M. The step €94.5M → €799M implies a local α ≈ 0.32, below 1, which is impossible for a distribution with a finite mean.

**Forbes fits inside the bin only with a large haircut** (secondary argument; the threshold chain above does not depend on Forbes).

- In 2024 the top bin holds €817bn for 530 adults. Forbes French billionaires sum to €630bn for 53 people (project's own sum of `finalWorth`).
- If all of it sat in the bin, the other 477 members would average €394M, half the €799M entry threshold. The minimum consistent with the threshold is €630bn + 477 × €0.799bn ≈ €1,010bn [json + csv].
- The gap between that implied minimum and the published total grows over time [json + csv]:

| Years | Gap |
|---|---|
| 2014 | about 0.5% |
| 2015–2017, 2020 | about 9–10% |
| 2019, 2021 | about 13% |
| 2022–2024 | 20–24% |

- Gaps of about 10% could be closed by citizens living abroad (7–10 a year) and the early-March Forbes valuation date. For 2022–2024 the haircut needed is large. Count spouses under equal split (53 × 1.8 ≈ 95 WID adults); the remaining 435 adults need at least €348bn; so Forbes wealth inside the bin can be at most about €469bn, roughly 25% below the Forbes total.
- Calling the 2022–2024 figures "inconsistent unless about a quarter of Forbes wealth is outside French residents' equal-split holdings" is defensible. Calling the earlier years impossible is not.

**Pareto inside the bin contradicts the same data.** `top_tail.py` derives α ≈ 2.07 from b = avg/threshold (2024). Under that Pareto, the top 53 of 530 hold 0.1^(1 − 1/α) ≈ 30% of the bin, about €250bn, against Forbes's €630bn.

**The project's reading.** docs/03-method.md:212–221 concludes that "the fortunes between roughly €100M and €800M are thin in WID". The data support this reading no more than the opposite one: that the p99.999 threshold, refit by gpinter after the Forbes top-up (as the note itself describes), is an artifact.

External counts weakly favour the smooth chain below the threshold:

- Zucman's estimate cited in Assemblée report n°930 is about 1,800 foyers above €100M (docs/notes/rich-lists.md:69). That is at most about 3,600 adults with more than €50M each.
- WID puts about 3,700 adults above €46.5M (threshold at p99.993) in 2024.

**Why it matters.**

- The threshold is printed as evidence of a gap, and it feeds the within-bin Pareto α in `top_tail.py:55–56`.
- Quantitatively the α choice barely moves W_n when n = 500 of 530. With f = 0.94, f^(1−1/α) is 0.968 at the α ≈ 2.07 used in the code and 0.971 at the α ≈ 1.9 implied by the threshold chain. Even an extreme α ≈ 1.1 gives only about 0.995. The scenario numbers are therefore not badly off for this reason.
- The interpretive claim on the page, however, is not supported.

**Fix.**

1. Withdraw the "thin €100M–€800M" inference, or present both readings.
2. Do not use `thwealj992 p99.999` to derive α. Estimate α from the threshold chain p99.99…p99.998 instead, or from Challenges/Forbes rank-size.
3. Add a test that t_j ≤ a_j ≤ t_{j+1} for every g-percentile, and print the violations on the page.
4. Replace "Forbes sits inside WID's top 0.001%" (docs/03-method.md:161; site/index.html:734) with "WID's top-bin total exceeds the Forbes total; its threshold is inconsistent with that".

### M2. The IPP comparison is not apples-to-apples: the share "match" is a denominator coincidence, and the "4×" is overstated

**The claim.** site/index.html:785 says "WID's shares match IPP's taxable income almost exactly … top 0.001% … about 4 times WID's". docs/03-method.md:288 says "1.3× to 4× larger".

**Evidence in euros, 2016, nominal** [csv + json]:

| Group | WID pre-tax (adults) | IPP taxable (foyers) | IPP dividend-imputed | IPP comprehensive, 2025 paper | IPP comprehensive, Note 92 rev. |
|---|---|---|---|---|---|
| Top 1% | €199bn | €100bn | €162bn | €172bn | €219bn |
| Top 0.1% | €68bn | €34bn | €61bn | €77bn | €128bn |
| Top 0.01% | €24.6bn | €12.9bn | €22.6bn | €41.1bn | €88.9bn |
| Top 0.001% | €9.2bn | €4.66bn | €8.1bn | €24.5bn | €65.0bn |

- **Denominators differ by about 2×.** WID's denominator is national income, €1,913bn nominal. IPP's is total fiscal income of foyers (€999bn) or comprehensive income (€1,245bn). In euros, WID is about **2× IPP taxable income in every top group**. The equal shares are a coincidence of numerator and denominator both being about twice as large. They are not evidence that WID "is" taxable income.
- **The euro gap is smaller than the share gap.** At the top 0.001% the euro ratio, IPP comprehensive (2025) / WID, is **2.7×**, not 4×. It is 1.7× at the top 0.01% and 1.13× at the top 0.1%. At the **top 1%, WID exceeds the 2025 paper's comprehensive income** (€199bn vs €172bn); Note 92's economic income (€219bn) is above WID.
- **The comparison that isolates the method.** WID's top 0.001% (€9.2bn) is close to IPP's *dividend-imputed* variant (€8.1bn). That variant allocates retained earnings in proportion to dividends received, the DINA-style approach. It is in `ipp_top_income.csv` but not shown on the page. The real disagreement is therefore about the allocation rule for retained earnings (in proportion to distributed dividends vs ownership through holding chains), not about "taxable vs comprehensive income". Whether WID France uses a dividend-proportional rule should be confirmed in GGP (2018), Appendix; I have not verified it.
- **Groups differ.** IPP's top 0.001% is 378 foyers ranked by each IPP concept. WID's is 507 adults (2016) ranked by equal-split pre-tax income. A married foyer counts as 2 WID adults.
- **The two IPP measures differ by 2.6×.** Note 92 (rev.) measures *economic* income ranked by economic income: top 0.001% share 5.1%. The 2025 paper measures *comprehensive* income: 2.0%. I have not established whether this is a revision or a definitional difference; the page treats it as a revision ("IPP's own estimates moved between versions"). Either way, "the size is uncertain, but the direction is not" holds only above the top 0.1%.

**Fix.**

1. Present euros per group, not shares over different totals; or rescale IPP to national income.
2. Add the dividend-imputed column.
3. Say "WID's top 0.01% and 0.001% income are 1.7× and 2.7× below IPP's ownership-based allocation, and WID is close to IPP's dividend-proportional allocation".
4. Note that at the top 1%, WID is above IPP's 2025 comprehensive measure.

### M3. Post-tax national income: the page misstates how WID allocates public spending, and ignores that 2019+ post-tax is mechanical

**What WID's own metadata says.** The source and method fields for `sdiincj992` (data/raw/WID_metadata_FR.csv) [raw]:

- The source is Fisher-Post & Gethin (2023), *Government Redistribution and Development*, WID WP 2023/17, not GGP/Bozio et al.
- The method field says: "Education is distributed proportionally to posttax disposable income. 2019-2022 series are estimated by applying the 2019 ratio of pretax to posttax income by generalized percentile."

**What Fisher-Post & Gethin (2023, §2.3) say** [src, PDF read]:

- "Data on the distributional incidence of healthcare come from Gethin (2023), who mostly relies on series from the CEQ database."
- "All other government expenditure is distributed proportionally to posttax disposable income."

Health is therefore allocated on an incidence profile, **not** in proportion to income.

**What the project says.**

- The page note (site/index.html:812): "WID shares public spending out in proportion to income, which understates what public services bring to the bottom half."
- docs/03-method.md:287 and docs/notes/insee.md:66 and :214–216 attribute proportional allocation of health and education to Bozio et al. (WID WP 2018/10). That is not the source of this vintage.
- docs/notes/insee.md:132 argues that in-kind transfers "should matter little" for the ERFS comparison because the allocation is neutral. That premise is wrong for health.

**The page assigns the 38% vs 32% bottom-50% gap entirely to the allocation rule.** It omits what docs/notes/insee.md:218–219 itself lists:

- the CND does not re-rank people by extended income, which mechanically raises bottom and lowers top concentration shares;
- the unit differs (UC-weighted persons vs equal-split adults).

The normative "understates" is not established. According to a search summary of its abstract (paper not read in full here), Riedel & Stichnoth (2024, *International Tax and Public Finance*) find that proportional allocation of education is rejected empirically and lump-sum fits better. That supports the *direction* for education, but this is a claim about one component, not about "public spending".

**2019–2024 post-tax series are pre-tax × fixed 2019 ratios.** The metadata says "2019–2022"; 2023–2024 is inferred from the same `data_quality` flag (4), which covers 2019–2024.

- Every post-tax "transfer" ending after 2018 therefore contains no information on taxes or benefits after 2019 (e.g. COVID-era transfers).
- The page's post-tax view shows bottom 50% "+€80bn" for 1980–2024 [json].

**Fix.**

1. Quote WID's metadata and the Fisher-Post & Gethin rules.
2. Rewrite the cross-check note to list all three reasons, with the no-re-ranking effect first.
3. Flag post-tax 2019–2024 as "pre-tax × 2019 ratio", not merely "extrapolated".
4. Correct insee.md.

### M4. The century-long series is treated as one methodology; quality flags and visible artifacts are ignored except at the end

**What the docs claim.** docs/02-data-france.md:36 says "one methodology from 1900 to 2024". In fact [raw `data_quality`, metadata]:

**Wealth:**

- 1800–1969: quality 2 (estate multiplier). The metadata also says "Before 1980, series is constructed based on the trend observed in the fiscal income data".
- 1970–2014: quality 4 (mixed capitalisation).
- 2015–2024: quality **0**, the fixed-2014-portfolio extrapolation.
- Plus the Forbes calibration, probably from 1988 (C3).

**Pre-tax income:**

- 1900–1969: quality 3, with 1901–1909 and 1911–1914 missing.
- 1971–74 and 1976–78: quality 3 between quality-5 years.
- 2019–2024: quality 4.

**Post-tax income:** a separate project (Fisher-Post & Gethin), from 1980 only.

**Artifacts in the top 0.001% wealth share** [json]:

| Year | Share | Neighbouring years |
|---|---|---|
| 1970 | 0.41% | 1969 0.81, 1971 0.83 |
| 1975 | 0.24% | 1974 0.84, 1976 0.83; bin avg/threshold 1.04, implied α = 24 |
| 1984 | 0.38% | 1983 0.51, 1985 0.52 |

The full share vector of 1961 is **identical** to 1963 (all seven layers).

**Why it matters.**

- The start year is user-selectable, and the transfer is a two-point difference. Picking 1984 instead of 1980 halves the base: the tile ratio goes from 7× (0.80 → 5.58) to 15× (0.38 → 5.58).
- The sensitivity chart will show these spikes as if they were economics.
- The grey band marks only the trailing extrapolation.

**Fix.**

1. Shade by WID `data_quality` for all years, not just the trailing run.
2. Mark Forbes-calibrated years and 1961/1963.
3. Default to multi-year averages for base years: smoothing should be the default and should include end years (see m2).
4. Withdraw "one methodology".

### M5. The housing affordability metric is mis-specified and reported inconsistently across files

**Inconsistent definitions.**

- The page uses *pre-tax* national income (site/index.html:742, `D.concepts.ptinc`), giving the bottom 50% 34.7 years for 70 m² in Paris in 2024 [json].
- docs/notes/prices-housing.md:159–177 uses *post-tax* `diinc` and DVF back-cast Paris prices: 23.4 years.
- docs/03-method.md:228–235 (§3.8) says post-tax and an index.
- docs/03-method.md:268–274 (§3.8c) says pre-tax.
- The page's method item 7 (site/index.html:260) says "income after tax".

**The pre-tax income is not cash.** The justification "Pre-tax income is used because it is cash" (docs/03-method.md:272–273) is wrong. Pre-tax national income includes:

- imputed rents of owner-occupiers;
- retained corporate earnings allocated to owners;
- social contributions and taxes not yet paid.

Mortgages are paid from disposable cash income.

**The denominator is not a buyer.** The bottom-50% average per adult includes many adults with near-zero individual income (P10 of `ptinc` = €6.2k, 2024 [json]). The "average bottom-50% adult" is not a plausible buyer.

**No financing costs.**

- Interest rates are ignored. French mortgage rates fell from roughly 7–8% (mid-1990s) to roughly 1% (2021), then rose [recall/literature, not verified here]. A price-to-income ratio that doubled is not a doubled payment burden.
- Price-to-income without the user cost or an annuity payment is not "affordability".

**Back-cast prices.** The rest-of-France level is a 2025 DVF mean back-cast with an index. The notes concede it is biased upward by at least 4.7% (docs/notes/prices-housing.md:185–187), and it is shown without that caveat on the page.

**Fix.**

1. Use disposable cash income per household or per consumption unit (e.g. ERFS deciles), or `diinc` minus in-kind items.
2. Add an annuity-payment version using the Banque de France mortgage rate series.
3. Use medians or deciles rather than layer means.
4. Make all four documents agree.

### M6. The "very top" section's internal text contradicts the page's own controls

**Contradictions.**

- Method item 6 (site/index.html:259) says "We do not adjust further; instead the page sets WID next to the Challenges and Forbes rich lists".
- The choices table (docs/03-method.md:36) says rich lists are "shown beside WID, not merged".
- Yet the filter bar offers rich-list scenarios that replace WID's top in every chart.

**Asymmetric scope.** Scenarios exist only from 1996, so they can only raise recent years. The page warns about this (scenarioNote), but the asymmetry adds to C2 and C3.

**Fix.** Make the text match the controls, and add the scenario's year coverage to every chart touched.

---

## 3. Minor findings

**m1. The CPI option creates an artificial step in 1950.**

- `priceFactor` returns 1 for y < 1950 (site/index.html:331).
- The spliced CPI exists for 1949 and gives a factor of 1.064 [json]. Every real series under "Consumer prices" therefore jumps by about 6.4% between 1949 and 1950.
- Fix: either apply the CPI to all years where it exists, or rescale so the factor is continuous at 1950.

**m2. Smoothing leaves the end year raw.**

- "First and last years are not averaged" (site/index.html:598; docs/03-method.md:243). The default end year, 2024, is the most volatile year: market-cap-driven Forbes calibration.
- Fix: use a one-sided or asymmetric window at the ends, or forbid the last year as an endpoint under smoothing.

**m3. The billionaire tile mixes units.** It divides Forbes *citizens* (including 7–10 living abroad, with family wealth folded in) by the household wealth of *residents* ("~4.3%"). The Forbes totals are the project's own sums of `finalWorth`, not figures stated by Forbes (CSV notes), and 2001–2009 are lower bounds.

**m4. Units and ranks across sections.**

- Housing layers are ranked by pre-tax income; the composition chart is ranked by wealth; tiles use wealth ranks.
- The page states that ranks differ (method limits), but sections are juxtaposed as if they described the same people.
- Equal-split adults also means a married billionaire is two "people" in "the richest 530 adults".

**m5. Population and age composition.**

- Adults 20+ rose from 26.8M (1900) and 38.2M (1980) to 53.0M (2024) [json], with strong ageing.
- Wealth shares of fixed percentiles move with age structure, independently of any "transfer".
- At minimum, state this; better, show within-age-group shares for 1970–2014, where WID has the microdata basis.

**m6. Real-growth table uses per-layer CAGR from layer averages that include the scenario.** In `renderTransfers`, `cagr` uses `C()` layers. With a scenario on, the "real growth" of the top 0.001% from a pre-1996 base mixes methods without a note in the table.

**m7. The Challenges / WID top 0.01% ratio has unaligned dates.** The ratio (0.43 → 1.11, docs/03-method.md:153–159) compares July market valuations of gross professional assets with annual WID net wealth. Luxury-stock swings within a year are ±20–30%. Show a band, not a point.

**m8. The DWA total-wealth check is not well defined.** WID's total exceeds DWA's by 0.7–4.5% although DWA's concept is about 10% narrower (docs/notes/dwa.md:245–250). The notes concede the source is unknown. This undermines the "bottom 50% agrees" reading less than it seems, but it should be resolved before claiming agreement on levels.

**m9. GIC "top 0.001% grew x% a year".** This uses calibrated WID top g-percentiles across the 1988 break (C3) with no flag.

**m10. Tests check arithmetic, not economics.** There are 14 passing tests and none checks:

- threshold/average coherence (M1);
- monotonic g-percentile averages vs thresholds;
- that documentation numbers match the build (several docs tables are hand-copied).

---

## 4. What a referee would require before publication

1. **Reframe transfers** (C1):
   - growth vs distribution decomposition per layer;
   - midpoint or both-year valuation;
   - "share of growth captured";
   - for wealth, a price/volume split for the top 1%.
   - Remove "moved/changed layer/lost/each".
2. **Identify WID's calibration** (C3): the uncorrected France series, or Figure 3 of WIL TN 2025/01 digitised. Mark calibrated years 1988–2024, and show the top 0.001% with and without.
3. **Symmetric top-tail scenarios** (C2):
   - GGP-consistent units (members × 1.8);
   - all scenarios selectable, including the neutral one;
   - downward corrections allowed;
   - a DWA-consistent lower scenario;
   - per-year W_n vs RL_adj table.
4. **Fix the top-bin interpretation** (M1). Withdraw "thin €100M–€800M", stop deriving α from `thwealj992 p99.999`, and add coherence tests.
5. **Redo the IPP comparison in euros** (M2), with the dividend-imputed column and the group-size caveat.
6. **Correct the post-tax allocation description** (M3) from WID metadata and Fisher-Post & Gethin, and flag 2019+ as mechanical.
7. **Quality shading by `data_quality`** for all years (M4). Use multi-year base averages by default, with smoothing that covers endpoints.
8. **Housing** (M5): disposable cash income, financing cost, one definition across all files.
9. **Reconcile every docs table with the build.** The "two largest jumps" claim and the housing tables are already out of sync.
10. **Uncertainty.** Show at least the range across sources and vintages for the top 1%, 0.1% and 0.001%. The project already has GGP 2016 (0.9% in 2014) vs the current vintage (3.4%) (docs/03-method.md:289), a 3.8× vintage revision. That range is the honest headline for the top 0.001%.

---

## 5. What is done well

- Layers that partition the population are the right object for "who holds what". Shares sum to 1 every year and this is asserted in the build.
- The pipeline is fully reproducible: standard library only, input hashes recorded, one source URL per hand-entered row, and superseded versions kept (IPP Note 92 old/revised).
- Unusually honest documentation. The start-year caveat, the anonymity caveat on the GIC and the DWA/HVP disagreements are all written down. Many of the problems above are flagged *somewhere* in the docs; the failure is that the page's wording does not carry the caveats.
- The start-year sensitivity chart is exactly the right robustness device.
- The cross-checks are well chosen and carefully parsed:
  - DWA with frozen-household caveats;
  - ERFS series split at breaks instead of spliced;
  - HVP net-wealth bounds derived correctly (ranking by gross can only lower top net shares);
  - the CND unit-count reconstruction checked against the published total.
- Rich-list data are well documented: valuation dates, family vs individual, citizenship vs residence, Forbes pre-2010 incompleteness. The WIL TN 2025/01 calibration was correctly identified from the WID metadata.
- The level chart on a log scale and the growth incidence curve are present. The tools to tell a non-zero-sum story already exist on the page; they should lead, not follow, the "transfer" bars.

---

### Sources consulted

- Bajard, Bauluz, Brassac, Chancel, Martínez-Toledano, Piketty, Sodano (2025), "Global wealth inequality on WID.world: Estimates and imputations", WIL Technical Note 2025/01, §3.3, pp. 4–7. https://wid.world/document/global-wealth-inequality-on-wid-world-estimates-and-imputations-world-inequality-lab-technical-note-2025-01/
- Fisher-Post, M. and Gethin, A. (2023), "Government Redistribution and Development: Global Estimates of Tax-and-Transfer Progressivity, 1980–2019", WID WP 2023/17, §2.3. http://wid.world/document/government-redistribution-and-development-global-estimates-of-tax-and-transfer-progressivity-1980-2019-wid-world-working-paper-2023-17/
- WID metadata for `sdiincj992`, `sptincj992`, `shwealj992` in `data/raw/WID_metadata_FR.csv` (source and method fields).
- Riedel, L. and Stichnoth, H. (2024), "Government expenditure in the DINA framework: allocation methods and consequences for post-tax income inequality", *International Tax and Public Finance* (search-result summary of the abstract only; not read). https://link.springer.com/article/10.1007/s10797-024-09832-1
- Project files: `data/manual/ipp_top_income.csv` (IPP Note 92 revised; Bach, Bozio, Guillouzouic & Malgouyres 2025, RFBerlin DP 70/25) and `data/manual/ggp_richlist_comparison.csv` (GGP 2016 appendix H parameters).
