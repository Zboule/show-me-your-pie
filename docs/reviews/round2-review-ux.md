# Round 2 review: public page, UX, clarity, data-vis and accessibility

Review date: 2026-10-16. Scope: `site/index.html` (v0.4) rendered with `site/data/france.json`.
Two readers at once: **(a)** a curious French citizen with no economics background, and
**(b)** an accessibility and data-visualisation specialist. Nothing outside this file was modified.

**How it was checked.**
- Pages were rendered in headless Chrome at 1280 px (light and dark), at 500 px, and at 375 px (in an iframe). Deep links `#ptinc`, `#diinc` and `#hweal~no_cut` were dumped to the DOM to read the generated sentences.
- Contrast was computed from the CSS tokens (WCAG 2.x formula). Colour-blind confusions were estimated by simulating deuteranopia and protanopia (Machado 2009) and measuring the CIELAB distance between colours.
- The keyboard, tooltip, screen-reader and live-region findings come from **reading the source**. Headless Chrome cannot show them, so they were not observed live.
- Screenshots are in the session scratchpad `<scratch>/ux/`, not in the repository. Files: `full_light.png` and `full_dark.png` (1280 px), `mobile.png` (500 px), `phone_a.png` (375 px), `hero_top.png`, `gic.png`. 1000 px slices are `L00.png`–`L12.png` (light) and `d00.png`–`d12.png` (dark); 1400 px mobile slices are `m00.png`–`m14.png`. Below, "L01" means `L01.png` in that folder, and so on.

---

## Summary verdict

**The hero looks good: dark band, gradient title, ribbon chart and Play button. Its headline is mostly right, but a lay reader still cannot decode it.**

- The ribbon chart has no colour key. Three of its seven pie segments are unlabelled, and one label is wrong. The headline sentence ("530 people held as much as the poorest 27.5 million") rests on a 2024 figure that WID itself projects from 2014 tax data. Nothing in the hero says so.
- Below the hero the page becomes a working paper. Chapters 02 (sensitivity chart), 04, 05, 06 and 07 are written for economists. The register jumps from "Picture France's wealth as one pie" to "refitting the distribution after the Forbes top-up" and "DINA-style".
- The glossary has 12 entries, but only one word on the whole page (`adults`) has a tooltip.
- **The page is in English for a French audience.** It uses US number formatting (`€21,100`, `€9.7 tn`). For persona (a) this is the single largest barrier, and it decides whether "anyone" can read it at all.
- **Neutrality is better than average.** The page states uncertainty ranges, gives the ECB counter-estimate, includes a "What this page does not say" box, and says the bottom half's wealth still rose.
- **But the uncertainty is easy to miss.** The strongest counter-evidence is lower on the page than the most quotable claims: the same team revised the top 0.001% from 0.90% to 3.4% for the same year, and every year after 2014 is extrapolated. In two places the wording goes beyond the evidence: the chapter 06 title, and the hero equivalence with no caveat.
- **Accessibility is weak where it matters most:**
  - Values appear only on mouse hover.
  - Only 2 of about 20 charts have a data table.
  - The light-mode muted text and three series colours fail contrast.
  - The colour palette means different things in different chapters.
  - The Play animation ignores reduced motion and floods the screen-reader live region.

Verdict: **ship-blocking for "understandable by anyone", not for correctness.** Most fixes are wording and CSS. Moving charts into an expert layer is a half-day of restructuring.

---

## Findings ranked by impact

Each finding gives where, the problem, evidence, and a fix (with wording where it helps).
Impact: H = high, M = medium, L = low. Effort: S = small (under 1 hour), M = medium (a few hours), L = large.

### 1. Page language and number format do not fit a French audience (H impact / L effort)
- **Where:** `<html lang="en">`, all copy, and `nf()`, which uses `Intl.NumberFormat("en-US")`.
- **Problem:** Persona (a) is a French citizen. The page is in English, with US separators (`€21,100`, `26.5 million`), English abbreviations (`€9.7 tn`, `€817 bn`, `€799 M`, `pts`) and one stray French term (*niveau de vie*) that is not explained. Even French readers who read English stumble on "tn" and "bn".
- **Fix:** This is a decision for the owner, but it is the biggest lever.
  - Ship a French version (`index.html` in French, `en/` in English), or at least a FR/EN toggle driven by a string table. The page already builds every sentence in JS, so a dictionary of about 150 strings is enough.
  - Format numbers with `fr-FR`, giving `21 100 €`, `9 700 milliards €` and `817 milliards €`.
  - Wording note for French: "le gâteau" is the natural metaphor ("le partage du gâteau"). A title such as **"Montre-moi ta part du gâteau"** keeps the joke.

### 2. The hero ribbon chart has no colour key and wrong or missing labels (H / S)
- **Where:** `renderHero()`.
- **Problem:**
  - Only "Poorest 50%" and "Next 40%" are named on the population bar. The pie bar shows `35.3%`, `32.2%`, `14.3%`, `5.7%`, an **unlabelled dark-green segment**, and `5.6%`. A reader cannot tell that the gold 14.3% is "the richest 1% to 0.1%".
  - The bracket text says "Richest 10% (the last five slices are almost invisible here)". This is wrong: the first of those five, the green "Top 10% to 1%", is clearly visible (`hero_top.png`). Only the four slices inside the top 1% are invisible.
  - Below about 640 px the bottom-50% label `4.8%` disappears, because the segment is narrower than 42 px (`mobile.png`, `phone_a.png`). That is the most important number in the picture.
  - The `rest` and `restFrom` variables are computed but never drawn, so the grouped label was intended but never shipped.
- **Fix:**
  - Under the pie bar, add a one-line key with the same chips as chapter 01: "■ Poorest 50% ■ Next 40% ■ Top 10–1% ■ Top 1–0.1% ■ Top 0.1–0.01% ■ Top 0.01–0.001% ■ Top 0.001%".
  - Better: label every segment with a leader line, as the 0.001% already has.
  - Always show the bottom-50% value: put it outside the bar with a leader when it does not fit.
  - Correct the bracket: "Richest 10%: the top 1% inside it is too thin to see here".
  - Draw the grouped label "Top 1% (4 thin slices): 27.6%" when slices are too narrow.

### 3. The headline year 2024 is a WID projection, and the hero does not say so (H / S)
- **Where:**
  - The hero caption.
  - All five finding cards.
  - Chapter 09 Limits: "an extrapolation after 2014".
  - Every chart, which shades 2015–2024 as lower quality.
- **Problem:** The most quotable numbers (5.6%, 530 people, 27.5 million) are for a year WID estimates by extending 2014 tax data. A citizen will take it as measured. A specialist will see the shading and wonder why the hero is silent.
- **Fix:** Append to the caption: "2024 is an estimate: WID extends 2014 tax data and will revise it." Add "(estimate)" next to the large year in the timeline whenever `year >= extrapolated_from`. Also consider a toggle (or a default) that shows **2014** as the latest measured year in the hero.

### 4. The hero equivalence sentence needs context and an uncertainty range (H / S)
- **Where:** The hero caption: "The richest 0.001%, about 530 people, held 5.6%: as much as the poorest 51.9% of adults put together (27.5 million people)."
- **Problem:** The sentence is arithmetically right, but it is the most emotive framing available.
  - It depends on the least certain number on the page. The cards give 4.8%–6.5%; the no-cut scenario reaches 8.1%; the same team's 2016 paper had 0.90% for 2014.
  - It also depends on the fact that a large part of the poorest half owns almost nothing, or owes more than it owns. Neither point appears in the sentence.
- **Fix (suggested wording):** "...held 5.6%, about as much as the poorest half of adults put together, many of whom own little beyond everyday savings, or owe more than they own. Estimates for the very top range from 4.8% to 6.5% (chapter 05)." Keep the "27.5 million" count in the tooltip or the chart, not in the sentence.

### 5. Strong counter-evidence is buried below the claims (H / S)
- **Where:**
  - The chapter 05 vintage card ("Same year, two estimates by the same team").
  - The cc-notes in chapter 07.
  - The "What this page does not say" callout in chapter 09.
- **Problem:**
  - The page's most honest facts are far below the fold. The same researchers' 2016 paper put the top 0.001% at **0.90%** for 2014; WID today says **3.4%** for that year, almost four times higher. The ECB / Banque de France accounts put the top 5% 6–8 points lower.
  - The "does not say" box ("does not follow the same people", "does not say anyone took money from anyone") is in chapter 09, after most readers have stopped.
  - Card 1's range "4.8% to 6.5%" silently leaves out the 8.1% no-cut scenario, so the range is narrower than the page's own scenarios.
- **Fix:**
  - Move the "What this page does not say" box up, directly under the finding cards, and shorten it to three bullets.
  - Add a sixth finding card, **"How sure are we?"**, with value **"Top: ×4 apart"** and text: "For the same year, 2014, the same team first estimated the richest 0.001% at 0.9% of wealth, now 3.4%. Estimates of the very top still differ a lot; estimates of the poorest half agree across sources."
  - On card 1, write "4.8% to 6.5% (8.1% under the most extreme assumption)".

### 6. One tooltip on the whole page, and jargon everywhere (H / M)
- **Where:**
  - `grep 'class="term"'` finds exactly one, on "adults".
  - The glossary lists 12 terms, but leaves out most of the terms that actually appear (see the **Jargon audit** below).
- **Problem:**
  - A reader meets WID, ECB / BdF, INSEE, IPP, DVF, "extrapolated", "Forbes calibration", "share effect", "logarithmic scale", "P99.9", "DINA-style", "imputed rent", "retained profits" and "non-resident cut" with no help on the spot.
  - The tooltip is CSS `::after` content taken from `data-def`. Screen readers announce only the word. Escape does not dismiss it (WCAG 1.4.13). It does not open on tap for touch users unless they happen to focus it.
- **Fix:**
  - Wrap the first use of each term in every chapter with a `<button class="term" aria-describedby="def-x">`, and give it a real popover: the `popover` attribute, or a small JS component that closes on Escape and outside click.
  - Generate the tooltip and the glossary entry from one dictionary.
  - Spell out every acronym on first use per chapter: "the World Inequality Database (WID)", "INSEE, France's statistics office", "the European Central Bank and Banque de France (ECB / BdF)".

### 7. Too many expert charts on the main path; add an "expert" layer (H / M)
- **Where:**
  - Chapter 02, "Does the start year change the answer?"
  - Chapter 04 (growth incidence curve).
  - Chapter 05: the summary paragraph, the top-bin note and the band chart.
  - Chapter 06 (IPP table).
  - Chapter 07 (six cross-check panels).
  - Chapter 08: the asset-mix chart.
- **Problem:** The owner's goal is "very fancy and understandable by anyone", with science in the repo. These blocks are correct and valuable, but they are written for referees. The chapter 05 summary alone holds 11 euro figures, 3 group definitions and 2 assumptions in 6 lines.
- **Fix:** Keep each chapter's **title, one plain sentence and one chart**. Put the rest inside a `<details class="expert">For experts: …</details>`. Suggested split:

  | Chapter | Keep on main path | Move to "For experts" |
  |---|---|---|
  | 01 | Stacked chart (with direct labels) | Small multiples (or keep them collapsed) |
  | 02 | Bar chart + 1 sentence | Sensitivity-to-start-year chart, numbers table |
  | 03 | Log chart, re-explained (see finding 13) | none |
  | 04 | Replace with 3 bars: "poorest half / average / richest 0.001% grew x% a year" | The 127-rank curve |
  | 05 | Plain summary + "WID vs rich lists" chart | Scenario band chart, top-bin threshold note, vintage table (but surface the vintage fact in the hero, finding 5) |
  | 06 | One sentence + simple 2-bar chart for top 0.001% (WID 9.2 vs IPP ownership 24.5 bn) | Full IPP table |
  | 07 | One chart: top 10% wealth share, WID vs ECB vs INSEE | Other five panels and cc-notes |
  | 08 | Years-of-income Paris + rest of France | Repayment charts, asset mix, CPI-by-income note |

### 8. Chapter titles and controls do not match what the charts show (M / S)
- **Where:**
  - The rail entry "Real wealth per person" and the chapter 03 title "Everyone's slice, in euros".
  - The control bar's `aria-label`: "Settings for every chart below".
  - `renderTop`, `renderCrosscheck` and `renderHousing`, which are called only on load and resize.
- **Problem:**
  - Choosing "Income before tax" switches the chapter 03 chart to income, but the rail still says "Real wealth per person".
  - Chapters 05–08 ignore the Pie, From and To controls, yet the bar claims to scope "every chart below". After changing the scenario, the hero still says 5.6% while chapter 01 says 8.1% (deep link `#hweal~no_cut`).
  - In chapter 02 on income, the summary says "The bottom half's real **holdings** went up by €184 bn". Income is not holdings.
- **Fix:**
  - Make the chapter 03 rail and title follow the selected pie ("Real income per adult" or "Real wealth per adult").
  - Change the bar's label to "Settings for chapters 01–04", and put a small "Wealth only, fixed period" chip on chapters 05–08.
  - Under a scenario, add one line to the hero caption: "Hero shows WID as published."
  - Use "yearly income" instead of "holdings" when `concept !== "hweal"`.

### 9. The two income pies show identical totals and growth, which will look like a bug (M / S)
- **Where:** Chapter 02 and chapter 04 under `#ptinc` and `#diinc`. Both read "rose by €998 bn" and "+0.82% a year".
- **Problem:** A lay reader expects income *after* tax to be smaller. By construction the two have the same total: taxes come back as benefits and public services. This is never said.
- **Fix:**
  - Hero chip tooltip, and one line under chapter 02: "Both income pies have the same size: taxes are counted as coming back to people as benefits and public services. Only the cut changes."
  - Rename the chip **"After taxes, benefits and public services"** (this is also clearer than "After tax & services").

### 10. Light-mode contrast failures (M / S)
Computed from the tokens:

| Pair | Ratio | Needed | Status |
|---|---|---|---|
| `--muted #7b8597` on `--bg #f2f4f7` (eyebrow, `.ctl-label`, rail numbers) | 3.38 | 4.5 (12 px text) | **Fail** |
| `--muted` on `--surface #fff` (all chart tick labels at 11 px, `th`, `.range`) | 3.72 | 4.5 | **Fail** |
| `--muted` on `--surface-2` | 3.50 | 4.5 | **Fail** |
| `.neg` / `--loss #e34948` text on white | 3.95 | 4.5 | **Fail** |
| `.pos` / `--gain #2a78d6` text on white | 4.42 | 4.5 | **Fail (marginal)** |
| Line `--s4` gold #eda100 on white | 2.17 | 3 (graphics) | **Fail** |
| Line `--s5` pink #e87ba4 on white | 2.69 | 3 | **Fail** |
| Line `--s3` green #1baf7a on white | 2.82 | 3 | **Fail** |
| Growth bars `--growth #9aa3b2` on white | 2.54 | 3 | **Fail** |
| `--ink-2` on white / bg | 7.8 / 7.1 | 4.5 | Pass |
| `--accent-ink` on bg / white | 5.75 / 6.33 | 4.5 | Pass |
| Hero `--hero-ink-2` on hero bg / finding card | 8.9 / 8.3 | 4.5 | Pass |
| Hero label `#0b1322` on `--s7` (light theme #6250d6), the "5.6%" segment label | 3.22 | 4.5 | **Fail** |
| Hero label `#0b1322` on `--s1` (light theme #2a78d6), the "4.8%" segment label | 4.21 | 4.5 | **Fail** |
| `--s6` #008300 as a graphic on dark surface | 3.49 | 3 | Pass (barely; looks muddy) |

- **Dark mode passes everywhere tested.** `--muted #8590a3` on the dark surface is 5.35.
- **The "always dark" hero is not:** it reads `--s1…--s7` from the theme, so in light mode the dark hero is drawn with the light palette.
- **Fix:**
  - `--muted: #5f6979` (5.0:1 on #f2f4f7, 5.2:1 on #f7f8fa, 5.6:1 on white; checked).
  - Darken the light-mode series: `--s3: #0f8a5f` (4.4:1 on white), `--s4: #b37800` (3.8:1), `--s5: #c4517e` (4.4:1), `--growth: #7d8696` (3.7:1). Alternatively, draw the growth bars with a 1 px `--ink-2` outline.
  - Pin the dark series tokens inside `.hero { --s1: #3987e5; … --s7: #9085e9; }`.
  - Use `--ink` for `.pos` and `.neg` text and show the colour only as a small swatch.

### 11. The colour system is unordered and reused for different meanings (M / M)
- **Where:** `--s1…--s8` across all charts.
- **Problem:**
  - The seven slices are *ordered* (poorest → richest) but drawn in a rainbow (blue, orange, green, gold, pink, dark green, purple). Nothing tells the eye that pink is richer than gold.
  - **Two greens** (`--s3` and `--s6`) sit next to each other in the stack: contrast ratio 1.76 in light mode, 1.45 in dark mode.
  - The same hues change meaning between chapters:
    - Blue is the bottom 50% in chapter 01, "share went up" in chapter 02, WID in chapter 07, and "WID top 0.01%" in chapter 05.
    - Orange is the middle 40% in chapter 01, Challenges in chapter 05, and ECB in chapter 07.
    - Green is "Top 10%–1%" in chapter 01 and INSEE in chapter 07.
  - Colour-blind simulation:
    - Deuteranopia: blue vs purple ΔE ≈ 12, so the bottom 50% and the top 0.001% look alike in the levels chart; green vs pink ΔE ≈ 13.
    - Protanopia: orange vs dark green ΔE ≈ 11.
    - Normal vision: in the band chart, "Rich list, 1 member" (`--s2`) and "no non-resident cut" (`--s8`) differ by a contrast ratio of only 1.2 and ΔE ≈ 22. They look like the same red.
- **Fix:**
  - Give the seven slices a **sequential ramp**, for example from cool grey-blue (poorest) to deep violet or magenta (richest), with the top 0.001% the one saturated accent that matches the hero's "pie" gradient.
  - Keep a **separate, fixed palette for sources** (WID / ECB / INSEE / IPP / Challenges / Forbes), drawn as neutral greys plus one accent, with dashed or dotted strokes per source.
  - Draw scenario lines with dash patterns, not just hue.
  - Add direct end-of-line labels everywhere (the levels chart already has them) so no chart depends on colour alone.

### 12. Charts are mouse-only; most have no text or table alternative (M / M)
- **Where:**
  - `lineChart`, `stackChart`, `decompChart` and `renderHero`.
  - Every `<svg role="img">` has a generic label such as "Stacked shares of each population layer over time".
- **Problem (from the source):**
  - Values appear only on `pointermove` / `pointerdown`, so keyboard and screen-reader users get none.
  - Only chapter 02 and the chapter 05 rich-list chart have "Show the numbers".
  - The `aria-label`s carry no data and no conclusion.
  - The hero chart is `role="img"`. Its caption is `aria-live="polite"`, which is good, but see finding 14.
- **Fix:**
  - Add "Show the numbers" (a collapsible table) to every chart. A generic `tableFor(series)` helper would cover all `lineChart` calls.
  - Write a one-sentence takeaway into each `aria-label`, for example: "Stacked shares of wealth, 1900–2024. The bottom 50% rose from 1.6% in 1900 to 9.7% in 1988, then fell to 4.8% in 2024."
  - Make the plot area focusable (`tabindex=0`) and move the crosshair with ← and → keys, showing the same tooltip.

### 13. Chapter 03's log scale and chapter 04's rank axis are misread by non-specialists (M / S)
- **Problem:**
  - **Chapter 03:** The note leads with "logarithmic scale: equal vertical distances mean equal growth rates". Lay readers do not know what a log scale is, and will read "€10.0 bn" at the top as a value someone holds.
  - **Chapter 04:**
    - The x-axis spaces 127 ranks evenly, so the top 1% takes about 22% of the width with no visual break.
    - Ticks read `P10 P25 P50 … P99.9 P99.99 top`, and at 500 px they collide ("P99P99.9P99.99top", `mobile.png`).
    - The chart has **no legend**: the grey horizontal line ("average of everyone") is identified only in the tooltip.
    - The line rises steeply at the right edge, and a lay reader will over-read it.
- **Fix:**
  - **Chapter 03:**
    - Rephrase the note: "Each step up the scale is ten times more money. Lines that rise at the same slope grow at the same speed."
    - Label one line in plain words directly on the chart ("Poorest half: €26,800 per adult").
    - Format axis values as `10 000 €`, `1 million €` and `1 milliard €`.
  - **Chapter 04:**
    - Add a shaded band and the label "zoom: inside the richest 1%" over ranks 99–126.
    - Use readable ticks: "poorest 10%", "median", "richest 10%", "1%", "0.1%", "0.01%", "0.001%", and drop the alternate ticks below 640 px.
    - Add a legend: "— each rank · — average of everyone".
    - Better: on the main path, show the 3-bar version (finding 7).

### 14. The Play animation ignores reduced motion and floods the live region (M / S)
- **Where:** `bindHero()`, which runs `setInterval(…, 110)`; `#hero-caption` has `aria-live="polite"`.
- **Problem:**
  - The CSS `prefers-reduced-motion` rule only stops CSS animations and transitions. The JS timer still redraws about 9 times a second, through 125 years.
  - Each redraw rewrites the live caption, so a screen reader queues about 125 announcements.
  - Dragging the range input does the same.
- **Fix:**
  - When `matchMedia('(prefers-reduced-motion: reduce)').matches`, step every 600 ms or jump decade by decade.
  - Set `aria-live="off"` while playing or dragging, and announce only on pause or `change`.
  - Give the range input `aria-valuetext="1990: poorest half 8.9%, richest 0.001% 1.4%"`.

### 15. Chapter 06 title overstates; its key table is cut off (M / S)
- **Where:** The `#topincome` heading "Profits that never reach a tax return", and the IPP table.
- **Problem:**
  - "Never reach a tax return" reads as evasion. These are retained company profits, already taxed by corporate tax, and they may be distributed later.
  - The summary itself says WID is *close to* IPP under the standard method and that the gap is "indicative".
  - The two columns that carry the argument (dividend-imputed and ownership-chain) are off-screen at 1280 px. The header is truncated at "IPP retained profits allocated in proportion to d…". At 500 px only the WID column is visible, with no sign that the table scrolls.
- **Fix:**
  - Title: **"Company profits that stay inside firms"**. Summary sentence: "For the 500 richest adults, counting profits kept inside their companies could make their income up to about 2.7 times larger than WID's estimate; for the top 1% as a whole it makes little difference (one year, 2016)."
  - Shorten the column headers ("Taxable", "Profits shared like dividends", "Profits via ownership chains") and add a footnote.
  - Show the scroll affordance with a fade on the right edge.

### 16. Chapter 08 metrics need a plain-language anchor (M / S)
- **Problem:**
  - The Paris repayment chart goes up to about 270% of income (bottom 50%, 2012). Without explanation, a reader does not know that above 100% the repayment cannot be paid from one income at all.
  - The hero card "41 years of income for one person in the poorer half of incomes" switches from **wealth**-ranked groups (everywhere else) to **income**-ranked groups without saying so.
  - The card's years (1996 → 2023) differ from the rest of the hero (1990 → 2024).
  - "Income committed before any choice" includes **imputed rent for owners**. A reader will take 30% as a cash outflow.
  - The DREES figure dates from 2011.
- **Fix:**
  - Draw a dashed reference line at 100% labelled "= all of one person's income".
  - Card text: "For one person in the lower-income half (ranked by income, not wealth)…".
  - Precommit note: "…including what owners would pay if they rented their own home."
  - Mark the DREES number "(2011 survey)" in the sentence, as it is now, and add "(latest available)" if true.

### 17. Hero cards: phrasing, wrapping and missing subjects (M / S)
- **Where:** `#findings`.
- **Problem:**
  - Card 3 shows the value **"7.7% vs 2.7%"** with no subject; the reader must read the small text to learn who is who.
  - Card 4's value, "20.3% → 31.5%", wraps onto two lines at 1280 px (`full_light.png`, `L00`).
  - The card titles are uppercase 12 px muted text. Uppercase lowers readability, and in a 5-column grid they wrap to two lines.
- **Fix (wording):**
  - Card 3: title "Who got the extra wealth since 1990", value "530 people: 7.7%", subline "26.5 million people: 2.7% of the €9 700 bn rise".
  - Card 4: title "Taxes and public services", value "20% → 32%", text "Poorest half's share of income, before vs after taxes, benefits and public services such as health care and schools".
  - Use `white-space: nowrap` on `.v`, or drop to 1 decimal place.
  - Grid: switch to `minmax(220px,1fr)` with 3 + 2 rows on desktop.

### 18. Chapter 01: quality shading and the reference lines need a key (L / S)
- **Problem:**
  - The grey veil over 1900–1969 and 2015–2024 is explained only inside "How to read this chart". On the stacked colours it looks like a rendering glitch (`L01`).
  - The 1988 dashed line (stroke `--surface`) and the 1990 solid line sit 2 years apart and read as one thick double line.
  - The stack has no direct labels.
- **Fix:**
  - Add legend items "▒ less reliable years (WID's own flag)" and "┆ 1988: WID starts using Forbes billionaires".
  - Label the right edge of the stack directly ("Poorest 50% 4.8%", and so on).
  - When `from` is 1988–1992, draw only the dashed line.

### 19. Decomposition chart wastes half its width (L / S)
- **Where:** Chapter 02, `decompChart`.
- **Problem:** The scale is symmetric (`-ext … ext`), but only small negative bars exist. Row labels sit at x ≈ 475 px and bars start at about 833 px, so the left half of the card is empty (`L03`). The meaning of grey plus colour is in the legend, but readers need the net value as the bar itself.
- **Fix:**
  - Use an asymmetric domain (`min(0, minNeg) … max`) and left-align the labels next to the axis.
  - Consider a stacked bar: grey (growth) plus coloured (share), with a black tick for the net.

### 20. Robustness and polish (L / S)
- **Load failure:** The catch handler writes to `#tiles`, which does not exist. If `france.json` fails, the page shows nothing and throws a TypeError. Write the message into `#hero-caption` or a dedicated `role="alert"` element.
- **No loading state** while the 488 KB JSON arrives: the hero chart area and the cards are blank. Add a skeleton or a "Loading…" line.
- **No chapter navigation below 1000 px:** the rail is hidden. Add a compact "Jump to chapter" `<select>` in the control bar.
- **No skip link** to the main content.
- **Sources chapter:** "the four independent reviews" should say who reviewed. `review-numbers.md` cites Claude Code scratchpad paths, which indicates the reviews were run as AI-agent sessions. Say so ("four critical reviews run by separate AI agents, published in full"); "independent" alone suggests outside human experts.
- **Footer:** "data built 2026-10-16 from WID.world (prices of 2025)". Replace "prices of 2025" with "in 2025 euros".

---

## 1. First 30 seconds (hero)

**What works.**
- The title is memorable.
- The lede poses three clear questions ("Who gets which slice, how has that changed, and how sure can we be?").
- The ribbon picture is a good idea: population width above, share width below, ribbons between them.
- Play animates over a century. The poorest-half-vs-0.001% caption is easy to grasp.
- The first card already admits uncertainty ("the very top is the least certain number here").
- Card 2 gives the counter-fact ("Yet their average real wealth still rose").

**What fails for persona (a).**
1. "Pie", but no pie is shown. The lede asks the reader to *imagine* a pie, then shows two bars. This is fine, but the stage title "Share of the adults vs share of the pie" is awkward. Better: **"Each group's share of the people, and of the pie"**.
2. There is no colour key (finding 2). Three segments are unlabelled and the bracket text is wrong.
3. The caption sentence is the right message, but it lacks the 2024-is-an-estimate flag and the context of near-zero and negative wealth (findings 3 and 4).
4. The finding cards ask for too much decoding (finding 17). Card 3 ("7.7% vs 2.7%") is the hardest for a non-specialist.
5. The findings note under the cards is technical ("after it began adjusting its top group to Forbes in 1988"). Rewrite: "These numbers come from the World Inequality Database. Other official sources put the richest 5% somewhat lower; chapter 07 compares them."

**Fancier, and easier to understand: a "village of 100,000" idea.** One line under the chart would make the scale tangible:
"If France were a village of 100,000 adults, the richest one would own as much as the poorest 51,900 put together."

## 2. Jargon audit

| Where | Quoted text | Plain rewrite |
|---|---|---|
| Hero chip / control | "Income before tax" | "Income before taxes (wages, profits, pensions)" |
| Hero chip / control | "After tax & services" | "After taxes, benefits and public services" |
| Hero caption | "Top estimate adjusted to Forbes figures since 1988" | "Since 1988, WID raises its estimate of the richest so it is never below the Forbes billionaires list." |
| Findings note | "after it began adjusting its top group to Forbes in 1988" | as above |
| Findings note | "the ECB / Banque de France accounts" | "the European Central Bank and Banque de France's household wealth figures" |
| Findings note | "5.8–7.6 points lower" | "6 to 8 percentage points lower (in 2024, about 41% instead of 47%)" |
| Control bar | "Expert settings" → "The very top of wealth: WID as published / Lower: ECB / Banque de France level / Rich list, 1 member per family / no non-resident cut" | Fine to keep as expert. Add one hint line: "Change how the richest 530 people are estimated." |
| Control bar | "National income prices (WID)" / "Consumer prices (INSEE)" | "Adjust for inflation using: the price of everything produced (WID) / the price of what households buy (INSEE)" |
| Ch 01 howto | "years that the World Inequality Database itself flags as less reliable" | Good. Also state it in the legend. |
| Ch 02 legend | "Growth effect (at the average of the start and end shares)" | "If its share had not changed" |
| Ch 02 legend | "Share effect: share went up / down" | "Because its share grew / Because its share shrank" |
| Ch 02 | "total real net wealth rose by €9.7 tn" | "all household wealth, after inflation, grew by 9 700 billion euros" |
| Ch 02 | "real holdings" | "wealth after inflation" (and for income: "yearly income after inflation") |
| Ch 02 sensitivity | "The share effect up to your end year, for every possible start year" | Move to experts (finding 7). If kept: "Would the answer change if we started counting in another year? Each point is a different starting year." |
| Ch 03 | "constant 2025 euros, logarithmic scale: equal vertical distances mean equal growth rates" | "in today's euros. Each step up the scale is ten times more money." |
| Ch 03 | "layer" (also "slice (layer)" in the glossary) | Use "slice" or "group" only; drop "layer" from the visible text (tooltip and table header "Layer"). |
| Ch 04 | "percentile group", "P10 … P99.99", "growth incidence" (aria) | "rank", "poorest 10%", "richest 0.01%" |
| Ch 04 | "8 groups near zero are left out, since a growth rate from almost nothing is meaningless" | "The poorest few percent own almost nothing (under about €1,100 each on average; the poorest 1% owe more than they own), so a growth rate means nothing for them and they are left out." |
| Ch 05 | "WID's whole top 0.01%", "111.4%" | "Challenges' list now adds up to more than WID's richest 5,300 adults (its top 0.01%)." |
| Ch 05 | "Under published assumptions the list covers 9,000 adults (10 members per family) and, after the non-resident cut, €994 bn…" | Move to experts. |
| Ch 05 | "entry threshold … sits 5.9 times above what the thresholds just below it imply at the same slope … refitting the distribution after the Forbes top-up" | Move to experts. Plain version: "WID's very top group starts at an oddly high fortune, a sign it was adjusted to match Forbes; our alternatives smooth this out." |
| Ch 05 vintage | "2016 paper / WID today" | "First estimate (2016) / Revised estimate (today)" |
| Ch 06 | "retained profits", "tax households", "DINA-style", "ownership chains", "distributional national accounts usually do" | "profits companies keep instead of paying out", "foyers fiscaux", "shared in proportion to dividends", "followed through who owns which company" |
| Ch 07 | "persons per consumption unit", "INSEE ERFS", "ranked by their ordinary income (which mechanically raises the bottom's share)", "attributes education and collective spending by use" | Move all of cc-notes to experts. Keep: "Official sources agree on the poorest half; they disagree by several points on the richest." |
| Ch 07 | "INSEE wealth survey (gross)" | "INSEE survey (before debts)" |
| Ch 08 | "cash income after taxes and benefits (INSEE income survey) for one person living alone; a couple counts as 1.5 people" | "income after taxes and benefits, per person, as INSEE measures living standards" |
| Ch 08 | "DVF open data", "INSEE's price indices", "ECB" | "recorded sale prices (DVF, public data)" |
| Ch 08 | "Income committed before any choice" / "pre-committed" | "Bills you can't easily cut: rent, energy, phone, insurance, canteen" |
| Ch 08 | "gross assets" | "everything owned, before debts" |
| Ch 09 | "partition", "imputed rent", "Growth effect … split is exact", "extrapolation", *niveau de vie* | Fine for a method chapter, but each needs a tooltip. |

**Glossary gaps.** The glossary has none of these entries:
WID, INSEE, ECB / Banque de France, IPP, DVF, Challenges and Forbes as sources, real / constant euros (inflation-adjusted), percentage point, logarithmic scale, percentile / rank, retained profits, imputed rent, disposable income, tax household (foyer fiscal), non-resident cut, gross vs net assets, *niveau de vie*.

It does have "Distributional national accounts" and "Consumption unit". Those are expert terms the main path will no longer need once finding 7 is applied.

## 3. Chapter by chapter

| # | Title + summary understandable? | "How to read" sufficient? | Verdict |
|---|---|---|---|
| 01 Seven slices | Yes. Good summary sentence. | Good text, but the quality shading and the 1988 line should be in the legend. Two greens adjacent. | Keep. Add direct labels and a sequential palette. Small multiples could be collapsed. |
| 02 A bigger pie, cut differently | Title is excellent. The summary's last clause ("had it kept its 1990 share, they would have gone up by €866 bn") is the key insight, but it comes last. | The text is good and its "not money taken from one group" caveat is essential. Keep it visible, not collapsed. | Keep the bar chart; move the sensitivity chart to experts. Lead with: "The poorest half's wealth grew by €265 bn. If they had kept their 1990 share, it would have grown by €866 bn." |
| 03 Everyone's slice, in euros | Title is fine, but static under income. The log note is jargon. | It says "multiplies by ten at each step", which is good; put that in the visible note instead of "logarithmic". | Keep. Fix the wording and the title binding. |
| 04 Who grew fastest? | Title is good. The summary is OK. | "127 ranks … last 28 points are all inside the top 1%" is fine for experts; there is no legend. | Move the curve to experts; show 3 bars. |
| 05 530 people, several estimates | Title is good. The summary is unreadable for (a): 11 figures. | The callout "Why the top is hard" is the best plain text on the page. | Keep the callout and the rich-list chart; move the rest. Surface the vintage fact. |
| 06 Profits that never reach a tax return | Title overstates (finding 15). The intro is dense. | No chart; the table is cut off. | Simplify to a sentence and a 2-bar chart; move the table to experts. |
| 07 The same question, other producers | Title is vague. Better: **"Do official sources agree?"** The answer is buried in cc-notes. | No howto. Six panels with y-axes that don't start at zero (they exaggerate gaps). INSEE survey points are joined across multi-year gaps. | Keep one panel on the main path, plus the one-line answer. |
| 08 What a flat costs | Clear and concrete; the best lay hook after the hero. | No howto. Repayment over 100% unexplained. | Keep the years-of-income charts; move repayment, asset-mix and the CPI note to experts. |
| 09 Method and limits | Appropriately technical. The "does not say" box belongs higher up. | n/a | Keep; move the callout up. |
| 10 Glossary | Clear definitions. | n/a | Extend (see the jargon audit) and link it from the tooltips. |
| 11 Check everything | Good. | n/a | Qualify "independent" (finding 20). |

## 4. Balance and neutrality

**Good:**
- "Yet their average real wealth still rose".
- "this is not money taken from one group and given to another".
- "What this page does not say".
- Explicit scenarios in both directions.
- The ECB gap stated in the hero.
- The IPP finding quoted symmetrically ("the top 1% as a whole is not understated").
- Auten and Splinter cited.

**Pushes beyond the evidence, or reads that way:**
1. The hero equivalence sentence without caveats (finding 4).
2. 2024 presented as a measured year (finding 3).
3. "Profits that never reach a tax return" (finding 15).
4. The card 1 range leaves out the highest scenario without saying so (finding 5). This is a quiet narrowing in the *conservative* direction, but it should be stated.
5. The hero "Paris flat" card picks the most dramatic group (poorer half × Paris). Show the middle 40% and top 10% next to it (same data: 22 and 10 years in 2023) so it reads as information, not indignation.

**Counter-evidence that is not visible enough:**
- The 0.90% → 3.4% revision (finding 5).
- The fact that the bottom-50% share **agrees** across WID and ECB (−0.6 to +0.4 points), while the top disagrees. This is reassuring for the main message and honest about the top. Say it in the hero.
- Auten and Splinter is a US critique. If no French-specific critique exists, say so in chapter 09.
- Asset-price revaluation (house and share prices) as the main driver of wealth-share movements is mentioned only as "does not separate". One sentence in chapter 02 would help: "Much of this comes from house and share prices rising, which favours those who own them."

## 5. Visual design and the "fancy" factor

**Strengths:**
- The hero is genuinely attractive: a dark band with a radial glow and the gradient "pie". The ribbon chart is original.
- The type pairing (Bricolage Grotesque display, Newsreader prose, system UI) is distinctive.
- Cards, rail and sticky control bar are clean. Dark mode is well tuned.

**Weaknesses:**
- After the hero, the page becomes a long grid of uniform cards with thin lines. There are no annotations on the charts: no "World War I", "1945–75 rebuilding", "1988 Forbes" or "2008 crisis" labels on the 1900–2024 charts.
- Chapters 05–08 are walls of 12–13 px grey sans-serif text (`L09`, `L10`).
- Serif prose (Newsreader, 18 px) alternates with sans notes (13.5 px), so the eye keeps changing register.
- The light-theme stack is very saturated next to a pale UI.
- On mobile the seven small multiples are a 1,600 px scroll.

**Improvements ranked by impact ÷ effort:**
1. A legend and labels in the hero, and corrected bracket text (S).
2. Annotate the 1900–2024 charts with 3–4 historical events (S). This is the single cheapest way to look "fancy" and teach at the same time.
3. A sequential palette for the slices that matches the hero gradient, plus separate source styling (M).
4. Collapse the expert material and turn each chapter into title, sentence, chart (M). The page halves in length.
5. Big-number pull quotes per chapter, reusing the `.finding` style (S).
6. On mobile, show the small multiples as a horizontal scroll strip or a 2-column grid of sparklines (S).
7. Scrollytelling hero (L, optional): play years as the reader scrolls, with captions at 1914, 1945, 1980 and 2008.

**Dark and light behaviour.** The hero is dark in both themes, which is good, but it takes its series colours from the theme (finding 10). The rest of the page switches correctly.

**Mobile.**
- At 375–500 px the hero works.
- The `4.8%` label disappears.
- The chips wrap to two lines.
- The control bar becomes non-sticky, which is correct.
- The IPP table hides 3 of its 4 numeric columns.
- The chapter 04 ticks collide.
- There is no chapter navigation.

## 6. Accessibility

1. **Contrast:** see the table in finding 10. Light mode fails for muted text, three series colours, the growth bars and two hero labels. Dark mode passes everywhere tested.
2. **Keyboard (from the source):**
   - The buttons, selects, range input and `<details>` are native and reachable.
   - Escape closes Expert settings.
   - Focus outlines exist (`--accent` on the hero background ≈ 4.2:1, adequate).
   - **Chart values are not reachable by keyboard** (finding 12).
   - There is no skip link.
3. **ARIA:**
   - Chips use `aria-pressed` correctly; the range has `aria-label="Year"` but no `aria-valuetext`.
   - Every SVG is `role="img"` with a generic label.
   - The glossary tooltip is not exposed (finding 6).
   - The live caption floods during Play (finding 14).
   - The control bar's region label claims it scopes "every chart below" (finding 8).
4. **Colour-only encodings:**
   - Stack slices, line series in chapters 05, 07 and 08, the scenario band chart (two near-identical reds), and the up/down share bars (direction also helps there).
   - Fix: direct labels and dash patterns (finding 11).
5. **Reduced motion:** smooth scroll and CSS transitions are disabled correctly; the JS Play timer is not (finding 14).
6. **Table alternatives:** 2 of about 20 charts have one (finding 12).
7. **Language:** `lang="en"` on content meant for French readers, and *niveau de vie* is not marked `lang="fr"`.
8. **Text size:** chart ticks are 11 px and tooltips 12 px. Raise the ticks to 12 px with the darker muted colour.
9. **Error and loading states:** a failed load is silent (finding 20).

---

## Top 12 changes, in order

1. **Decide on French.** Build an FR version (or a toggle) with `fr-FR` number formatting ("9 700 milliards €"). Mark any remaining English or French terms with `lang`.
2. **Fix the hero chart.**
   - Add a colour key or label every segment.
   - Always show the bottom-50% value.
   - Correct the "last five slices" bracket.
   - Pin the dark series colours inside `.hero`.
3. **Flag 2024 as a WID estimate** extended from 2014 tax data, in the caption and next to the year. Optionally default the hero to 2014.
4. **Rewrite the hero caption** with context ("many of whom own little or owe more than they own") and the 4.8%–6.5% range. State that the range leaves out the 8.1% scenario.
5. **Move uncertainty up.**
   - Put the "What this page does not say" box under the cards.
   - Add a "How sure are we?" card using the 0.90% → 3.4% revision.
   - Add the line "sources agree on the poorest half, not on the richest".
6. **Add tooltips and expand the glossary.** Tooltips on the first use per chapter of every term in the jargon audit, built as accessible popovers from one dictionary that also feeds the glossary. Spell out every acronym on first use.
7. **Create a "For experts" layer.** Collapse the sensitivity chart, the 127-rank curve, the chapter 05 summary detail and top-bin note, the IPP table, five of the six cross-check panels and cc-notes, and the repayment and asset-mix charts. Each chapter becomes title, one sentence, one chart.
8. **Fix light-mode contrast.**
   - `--muted` to about #5f6979.
   - Darker `--s3`, `--s4`, `--s5` and `--growth`.
   - `.pos` and `.neg` text in `--ink`.
   - Ticks at 12 px.
9. **Rebuild the colour system.**
   - A sequential ramp for the seven slices.
   - A separate neutral palette with dash patterns for sources and scenarios.
   - Direct labels on every multi-series chart.
10. **Give every chart a table alternative and a meaningful aria-label.** Add "Show the numbers" everywhere, put the takeaway sentence in the `aria-label`, and add keyboard crosshair navigation.
11. **Make titles and controls tell the truth.**
    - The chapter 03 title follows the selected pie.
    - Change the control-bar label to "chapters 01–04".
    - Use "income", not "holdings", for the income pies.
    - Explain once that both income pies have the same total.
    - Retitle chapter 06 to "Company profits that stay inside firms".
    - Add the 100% reference line to the repayment charts.
12. **Polish and robustness.**
    - Respect reduced motion in Play, and silence the live region while playing.
    - Annotate historical events on the long charts.
    - Fix the `#tiles` error handler and add a loading state.
    - Add mobile chapter navigation and a skip link.
    - Qualify "independent reviews".
