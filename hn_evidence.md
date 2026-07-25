# HN evidence — python-csv-dataset-ingestion-lab

HN thread: https://news.ycombinator.com/item?id=22038317
Retrieved via: `hackernews get-item --id 22038317`

## Linked article claims

- CleverCSV is a drop-in replacement for Python's CSV module (github.com/alan-turing-institute/CleverCSV).

## Named Hacker News commenter claims

- **gregmac** (#22040336): Excel "absolutely butchers" CSV files — strips leading zeros, converts big numbers to scientific notation, interprets non-date values as dates, doesn't preserve quotes, uses regional separators (semicolon in some locales).
- **Twirrim** (#22041068): Unescaped comma in a text field caused a CSV line to have more columns than expected, shifting all subsequent fields by one. Some consumers crashed, others silently ingested misaligned data.
- **th0ma5** (#22042189): CSV problems include lack of standards, character encodings, lack of compression, inefficient read/write, problems handling multiline freeform text. "Ultimately the structure is inband with the data, which is what makes all problems probable."
- **fake-name** (#22042799): Python's csv module is slow.
- **gjjvdburg** — author of CleverCSV (#22043891): CleverCSV was written to improve automated dialect detection accuracy. Modified the C parser (increased look-ahead to two characters). Parsing is ~10–20% faster than builtin csv.
- **donarb** (#22039366): Pandas uses the Python csv module under the hood; most of `read_csv` is converting CSV data into dataframes.
- **manor** (#22044666): Suggested TSV solves CSV problems — "fields that contain tabs are not allowable in this encoding."
- **dmd** (#22044743), replying to manor: "What problem is solved, exactly? How do you parse the messy CSV file you've been handed, in order to convert it to TSV?"

## Current Python documentation

- `csv.reader` — RFC 4180 compatible, handles quoted fields, embedded delimiters, and newlines inside quoted fields.
- `csv.DictReader` — `restval` fills missing fields; `restkey` collects extra fields into a list.

## Local observations

- `csv.reader` correctly keeps a quoted embedded comma inside a single field (3 columns, not 4).
- `csv.reader` correctly treats an embedded newline inside quotes as field content, not as a record separator (2 logical rows, not 3).
- `csv.DictReader(restval="MISSING")` fills a missing third column with `"MISSING"`.
- `csv.DictReader(restkey="__extra__")` collects one extra value as `["extra"]`.
- A naive `str.split(",")` would split on the quoted comma and would split multiline fields at the embedded newline — not tested in the 12-row lab, noted here only as context.

## Non-claims and limitations

This lab does NOT:
- detect arbitrary CSV dialects,
- validate schemas,
- repair malformed files,
- prove performance,
- handle every spreadsheet export,
- demonstrate superiority over CleverCSV, pandas, or other parsers.

It tests four specific stdlib parsing relations on fixed inline strings: quoted delimiter handling, multiline quoted field handling, missing-column `restval`, and extra-column `restkey`.
