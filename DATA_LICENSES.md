# Data sources, licences and attribution

Every figure on the page and in the paper is our own calculation from the
sources below, **not endorsed by any producer**. Raw downloads are not
redistributed (`data/raw/` is ignored by git); `pipeline/fetch.py` downloads
them from the producers. The built dataset `site/data/france.json` contains
derived series and short quoted figures with their sources.

| Producer and data | Terms | Attribution |
|---|---|---|
| World Inequality Database (WID.world), France bulk data | No database licence published; cited as customary for derived statistics. WID reports are CC BY-NC-SA 4.0. | "Source: WID.world, France, vintage of 15 Oct 2026 (ETag recorded in `meta.wid_vintage`); Garbinti, Goupille-Lebret & Piketty (2018, 2021); Fisher-Post & Gethin (2023); WIL Technical Note 2025/01." |
| INSEE (income survey ERFS, wealth survey, distributed national accounts, price indices, national accounts, spatial price survey) | Licence Ouverte / Open Licence 2.0 | « Source : Insee », with the date of last update recorded in the build. |
| ECB Data Portal: distributional wealth accounts (DWA), MFI interest rates (MIR) | ESCB reuse policy | "Source: ECB statistics." Derived series (group sums, top-5% scenario, annual means of quarterly or monthly values) are our own calculations. |
| DGFiP / Etalab, Statistiques DVF | Licence Ouverte 2.0 and DVF conditions of use | "Source: DGFiP, DVF; Etalab, Statistiques DVF." Only département aggregates are used. |
| DGFiP *Analyses* n° 8; France Stratégie *Note d'analyse* n° 102 | Licence Ouverte 2.0 | Cited where quoted. |
| DREES *Études et Résultats* n° 1055 | Quoted figures with citation | Cited where quoted. |
| IPP Note 92 (2023) and Bach, Bozio, Guillouzouic & Malgouyres (2025) | All rights reserved; we quote a small number of published figures (21 rows) with page references | Cited in `data/manual/ipp_top_income.csv`. |
| Challenges "500 plus grandes fortunes de France" | Press figures quoted from published articles, one source per row | Cited in `data/manual/challenges_500.csv`. |
| Forbes World's Billionaires (French billionaires) | Figures quoted from published articles only (no API or scraped data) | Cited in `data/manual/forbes_france_billionaires.csv`. |

Earlier, unpublished versions of this project used a Paris Notaires price
table, an Observatoire des inégalités table and data obtained from Forbes's
API. Those tables are not in this repository because their terms do not
allow redistribution. The round-1 review reports in `docs/reviews/`, kept as
written for transparency, quote some figures from them; no result depends on
them.

## The project's own compilations

The hand-compiled tables in `data/manual/` and the built dataset
`site/data/france.json` are our compilation, released under CC BY 4.0
(credit "Show Me Your Pie contributors"). The facts they quote remain
attributed to their producers above.

## Fonts

The page uses Bricolage Grotesque and Newsreader, self-hosted in
`site/fonts/` under the SIL Open Font License 1.1 (licence texts alongside),
so visitors' browsers make no request to third-party font servers.
