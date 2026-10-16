# Reviews

This folder holds every review of the project and the responses, so readers
can judge how the results were checked.

## Who reviewed, and how

Each review was carried out by a **separate AI reviewer agent (Claude,
Anthropic)**, started with a single adversarial brief ("be as critical as
possible; only claim what you can support"), with access to the repository
and the web but not to the other reviewers' conclusions. The numbers
reviewers recomputed figures with their own code from the raw files, without
reusing the project's pipeline. **These are not peer reviews by outside
human experts.** The analysis itself was also built with Claude, so author
and reviewers share a model and may share blind spots; that is the main
reason human review is invited. Human review is welcome: open an issue with the *Review
comment* template ([CONTRIBUTING.md](../../CONTRIBUTING.md)).

## Round 1 (on version 0.2)

| Review | Brief | Report |
|---|---|---|
| Methodology | Referee in inequality measurement | [review-methodology.md](review-methodology.md) |
| Numbers | Recompute every number from raw inputs | [review-numbers.md](review-numbers.md) |
| Code | Reproducibility, correctness, tests | [review-code.md](review-code.md) |
| Sources | Citations, claims, framing, licensing | [review-sources.md](review-sources.md) |

Response and changes: [response.md](response.md) (version 0.3).

## Round 2 (on versions 0.4)

| Review | Brief | Report |
|---|---|---|
| Code | Clean-room rebuild, mutation testing, front end | [round2-review-code.md](round2-review-code.md) |
| Plain language and accessibility | Non-specialist reader and accessibility expert | [round2-review-ux.md](round2-review-ux.md) |
| Methodology | Second referee round, new methods | [round2-review-methodology.md](round2-review-methodology.md) |
| Numbers | Independent recomputation of the paper and the app | [round2-review-numbers.md](round2-review-numbers.md) |
| Sources | Provenance, licensing, citations, framing | [round2-review-sources.md](round2-review-sources.md) |

Response and changes: [round2-response.md](round2-response.md).

Reports are kept as written; where a later change made a statement in a
report obsolete, the response says so. Local file paths in reports are
redacted.
