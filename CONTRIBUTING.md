# Reviewing and contributing

This project is meant to be checked. Treat it like a working paper under open
review.

## How to review

1. Read the [working paper](paper/paper.md) and the
   [method](docs/03-method.md). Every number in the paper has a key in
   [paper/numbers.md](paper/numbers.md).
2. Rebuild everything (README, "Run it") and run the tests.
3. Open an issue with the **Review comment** template. Say where, what,
   your evidence, and a suggested fix. Rate the severity.
4. Earlier reviews and how each finding was handled are in
   [docs/reviews/](docs/reviews/). Please check there first.

## Ground rules for changes

- Every hand-entered value needs a source URL and, for quoted figures, the
  short quote it comes from (`data/manual/*.csv`).
- Do not commit raw downloads or data whose terms forbid redistribution
  (see [DATA_LICENSES.md](DATA_LICENSES.md)).
- Any change to a number quoted in the paper must regenerate
  `paper/numbers.json` (`python3 -I pipeline/paper_numbers.py site/data/france.json paper/numbers.json`)
  and keep the test suite green.
- Prefer showing a disagreement between sources over choosing one silently.
- Keep the page in plain language; put technical detail in `docs/`.
