# python-csv-dataset-ingestion-lab

A tiny deterministic correctness lab for CSV parsing in ML dataset ingestion pipelines. Python stdlib only.

HN thread: https://news.ycombinator.com/item?id=22038317 — "CleverCSV: A Drop-In Replacement for Python's CSV Module"

## What

Four cases, three methods each, twelve rows total:

| case | what it checks |
|---|---|
| `quoted_comma_field_marker` | quoted text field containing a comma stays one field, no column shift |
| `multiline_text_field_marker` | quoted field with embedded newline: 2 logical rows, newline preserved in field |
| `missing_column_dictreader_marker` | `csv.DictReader(restval="MISSING")` fills missing column |
| `extra_column_dictreader_marker` | `csv.DictReader(restkey="__extra__")` collects extra value as `["extra"]` |

Methods (applied to every case):

1. `inspect_inputs` — check case-specific preconditions on the inline CSV string
2. `execute_parse` — parse through `io.StringIO` + `csv.reader` / `csv.DictReader`
3. `verify_relation` — verify the expected parsing relation holds

All CSV inputs are fixed inline strings. No downloads, no external datasets, no randomness.

## Run

```
python3 run_lab.py
python3 -m unittest test_lab -v
```

Produces `observations.json` and `RESULTS.md` (12 rows).

## Scope / Non-claims

This lab does **not** detect arbitrary CSV dialects, validate schemas, repair malformed files, prove performance, handle every spreadsheet export, or demonstrate superiority over CleverCSV, pandas, or other parsers.

A naive `str.split(",")` would fail on quoted commas and multiline fields — noted as context, not tested in the 12-row matrix.

See `hn_evidence.md` for attributed claims from the HN thread, Python docs, and local observations.
