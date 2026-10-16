# Rich-list sources (rebuilt 2026-10-16)

Responds to `docs/reviews/review-sources.md` §4 and README checklist items 2–3.

## What was replaced

- **`forbes_france_billionaires.csv`**: all 26 rows (2001–2026) held counts and totals that we had summed from Forbes's list API (`forbes.com/forbesapi`). Forbes's terms forbid scraping and storing that data, so every row was deleted. Only counts and totals stated in articles remain; new column `total_eur_bn` holds euro totals, never converted.
- **`challenges_500.csv`**: 29 of 31 totals came only from the Observatoire des inégalités (IdO) table 2646, which is "© tous droits réservés". IdO links and figures, and articles relaying that table, were removed. Figures now come from press articles (mostly AFP) or Challenges' archived pages.
- **Both files** have a new `quote` column. It holds, per URL and in `source_url` order, the exact phrase with the figure (≤ 25 words); fragments are joined with " … ". A script matched every quote against the raw page.

## Coverage

**Forbes** (counts and totals belong to the edition, i.e. the year of publication). Counts exist for 2017–2025.

| Currency | Years |
|---|---|
| USD totals | 2017, 2021, 2022 |
| EUR totals | 2017 (AFP's "environ"), 2020, 2021, 2024 |

Nothing exists for 2001–2016 or 2026.

**Challenges**: 1996 and 1998–2026. 1997 is left out because no source gives a figure for it.

| Status | Years |
|---|---|
| Euro totals | 2004, 2006, 2007, 2009, 2010, 2012–2014, 2016–2020, 2022–2026 |
| Franc totals (notes only) | 1996, 1999–2001 |
| No total | 1998, 2002, 2003, 2005, 2008, 2011, 2015, 2021 |

2006 and 2022 totals are retrospective (later articles); 2012 rests on a blog repost of Challenges' article.

## Rules

- Nothing is derived (no sums, percentage changes, franc conversion or table rows).
- "près de"/"un peu plus de" figures are kept, qualifier in the quote; milestone wording ("cap des", "autour de") leaves the cell empty.
- Conflicts: the figure at publication, else an exact figure stated in a later article (flagged retrospective); alternatives in the note.

## Conflicts

- **Challenges totals**
  - 2014: 390 vs 394 (the 394 is from IdO only).
  - 2016: 456; the following year's "+117" would imply 454.
  - 2018: 650 vs 670 (the 670 is from IdO only).
  - 2019 and 2020: AFP gives 700 and 730; challenges.fr now shows 711 and 731.
  - 2025: 1 128, later restated as 1 129, and 1 279 in Lyon Capitale.
- **Challenges thresholds:** 59 vs 60 (2008), 39 vs 40 (2009), 80 vs 82 (2015).
- **Forbes counts**
  - 2017: Forbes France gives 38 and 39.
  - 2018: Forbes France says "39", but its table runs to #40.
  - 2023: 43, or 42 as implied by a 2024 article.
  - 2021: the total was restated in 2022 as 512,2 Md$.

## Access

Values come only from hosts whose robots.txt allows Claude agents, or from web.archive.org captures. Disallowing hosts include challenges.fr, forbes.fr, franceinfo, Le Monde, Le Figaro, Les Echos, Libération, La Libre, Le Temps and The Local; pages fetched from them early in the research were discarded. Figures seen only there are notes, not values.

## Licensing rationale

A published total is a fact; each row cites the article stating it, with a short quotation for attribution. No API was used, and no copyrighted compilation is reproduced.

## Effect on the build

`build_data.py` keeps rows with a count or a total. The dataset was rebuilt from these files; the rich-list scenarios now start in 2004, with missing years interpolated (see docs/03-method.md §3.7).


Weaker sources, kept with a note: the 2012 Challenges total rests on a blog repost of Challenges' own article, and the 2025 entry threshold on a newsletter.
