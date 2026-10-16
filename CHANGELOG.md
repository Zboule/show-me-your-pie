# Changelog

## 0.4.0 (2026-10-16) — first public release
- Redesigned page for non-specialists: hero chart (share of adults vs share of the pie, with a year slider), plain-language key findings, numbered chapters, glossary, expert settings folded away.
- Working paper (`paper/paper.md`) with every quoted number generated from the data and checked by the tests.
- Licensing clean-up: Forbes and Challenges series rebuilt from published articles; Notaires and Observatoire tables taken out of the repository (round-1 review reports, kept as written, still quote some of their figures); Paris prices from open DVF data; IPP table reduced to the figures used. Added LICENSE (MIT), LICENSE-DOCS (CC BY 4.0), DATA_LICENSES, CITATION.cff, CONTRIBUTING.
- Second review round (five AI reviewer agents: code, plain language and accessibility, methodology, numbers, sources) and response (`docs/reviews/round2-response.md`):
  - very top reported as ranges (Forbes floor to rich list); ECB-based scenario labelled illustrative; middle-40% disagreement with ECB / Banque de France shown;
  - 2018 used for the income headline (2019+ extrapolated by WID); growth-share ratio shown only when the total clearly rose;
  - page calculations moved to `site/core.js` and tested; stricter paper-number test; provenance test; DVF completeness and rate checks;
  - accessibility: ordered colour ramp, tables under every chart, term tooltips, expert sections, skip link, reduced motion; fonts self-hosted.

## 0.3.0 — response to the first review round
- Growth/share decomposition replaces "transfers"; scenarios in both directions; Forbes calibration from 1988 handled; IPP comparison in euros; housing on cash income with mortgage repayments; quality-flag shading; strict pipeline and non-tautological tests.

## 0.2.0
- Cross-checks with ECB / Banque de France, INSEE, IPP; rich-list scenarios; prices and housing; tests.

## 0.1.0
- First prototype on WID.world data.
