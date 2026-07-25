#!/usr/bin/env python3
"""python-csv-dataset-ingestion-lab — run_lab.py

Four deterministic stdlib csv cases, three methods each (inspect/execute/verify),
twelve rows total.
"""
import csv
import io
import json

CASES = [
    {
        "case_id": "quoted_comma_field_marker",
        "csv_text": 'id,text,label\n1,"hello, world",positive\n',
        "parser": "csv.reader",
        "restval": None,
        "restkey": None,
    },
    {
        "case_id": "multiline_text_field_marker",
        "csv_text": 'id,note\n2,"line one\nline two"\n',
        "parser": "csv.reader",
        "restval": None,
        "restkey": None,
    },
    {
        "case_id": "missing_column_dictreader_marker",
        "csv_text": 'a,b,c\nx,y\n',
        "parser": "csv.DictReader",
        "restval": "MISSING",
        "restkey": None,
    },
    {
        "case_id": "extra_column_dictreader_marker",
        "csv_text": 'a,b,c\n1,2,3,extra\n',
        "parser": "csv.DictReader",
        "restval": None,
        "restkey": "__extra__",
    },
]

# ---- inspect_inputs -------------------------------------------------

def inspect_quoted_comma(case):
    text = case["csv_text"]
    # expected header, one data row
    lines = text.strip("\n").split("\n")
    if lines != ["id,text,label", '1,"hello, world",positive']:
        return False, "header/data mismatch"
    # quoted field containing an embedded comma
    if '"hello, world"' not in text:
        return False, "quoted comma field not found"
    return True, "header ok, quoted comma field present"

def inspect_multiline(case):
    text = case["csv_text"]
    # expected header
    if not text.startswith("id,note\n"):
        return False, "header mismatch"
    # balanced quoting
    if text.count('"') % 2 != 0:
        return False, "unbalanced quotes"
    # exactly one newline inside the quoted field
    # csv_text = 'id,note\n2,"line one\nline two"\n'
    # split at first quote
    try:
        inner = text.split('"', 2)[1]
    except IndexError:
        return False, "no quoted field"
    if inner.count("\n") != 1:
        return False, f"expected 1 embedded newline, got {inner.count(chr(10))}"
    return True, "header ok, balanced quotes, 1 embedded newline"

def inspect_missing_column(case):
    text = case["csv_text"]
    # parse header / data with csv.reader for inspection only
    f = io.StringIO(text)
    rows = list(csv.reader(f))
    if len(rows) != 2:
        return False, f"expected 2 rows, got {len(rows)}"
    header, data = rows
    if header != ["a", "b", "c"]:
        return False, f"header mismatch: {header}"
    if data != ["x", "y"]:
        return False, f"data mismatch: {data}"
    # fixed restval
    if case.get("restval") != "MISSING":
        return False, "restval != MISSING"
    return True, "3 header fields, 2 data values, restval=MISSING"

def inspect_extra_column(case):
    text = case["csv_text"]
    f = io.StringIO(text)
    rows = list(csv.reader(f))
    if len(rows) != 2:
        return False, f"expected 2 rows, got {len(rows)}"
    header, data = rows
    if header != ["a", "b", "c"]:
        return False, f"header mismatch: {header}"
    if data != ["1", "2", "3", "extra"]:
        return False, f"data mismatch: {data}"
    if case.get("restkey") != "__extra__":
        return False, "restkey != __extra__"
    return True, "3 header fields, 4 data values, restkey=__extra__"

INSPECTORS = {
    "quoted_comma_field_marker": inspect_quoted_comma,
    "multiline_text_field_marker": inspect_multiline,
    "missing_column_dictreader_marker": inspect_missing_column,
    "extra_column_dictreader_marker": inspect_extra_column,
}

# ---- execute_parse --------------------------------------------------

def execute_quoted_comma(case):
    try:
        f = io.StringIO(case["csv_text"])
        rows = list(csv.reader(f))
    except Exception as e:
        return False, f"parse error: {e}"
    # confirm parsing returns expected header and one data row
    if len(rows) != 2:
        return False, f"expected 2 rows, got {len(rows)}"
    header, data = rows
    if header != ["id", "text", "label"]:
        return False, f"unexpected header: {header}"
    if len(data) != 3:
        return False, f"expected 3 columns, got {len(data)}"
    return True, rows

def execute_multiline(case):
    try:
        f = io.StringIO(case["csv_text"])
        rows = list(csv.reader(f))
    except Exception as e:
        return False, f"parse error: {e}"
    # confirm parsing returns exactly two logical rows
    if len(rows) != 2:
        return False, f"expected 2 logical rows, got {len(rows)}"
    return True, rows

def execute_missing_column(case):
    try:
        f = io.StringIO(case["csv_text"])
        reader = csv.DictReader(f, restval=case["restval"])
        fieldnames = reader.fieldnames
        rows = list(reader)
    except Exception as e:
        return False, f"parse error: {e}"
    # confirm DictReader reports expected field names and one parsed dict
    if fieldnames != ["a", "b", "c"]:
        return False, f"unexpected fieldnames: {fieldnames}"
    if len(rows) != 1:
        return False, f"expected 1 row, got {len(rows)}"
    if not isinstance(rows[0], dict):
        return False, "row is not a dict"
    return True, {"fieldnames": fieldnames, "rows": rows}

def execute_extra_column(case):
    try:
        f = io.StringIO(case["csv_text"])
        reader = csv.DictReader(f, restkey=case["restkey"])
        fieldnames = reader.fieldnames
        rows = list(reader)
    except Exception as e:
        return False, f"parse error: {e}"
    # confirm field names and one parsed dict
    if fieldnames != ["a", "b", "c"]:
        return False, f"unexpected fieldnames: {fieldnames}"
    if len(rows) != 1:
        return False, f"expected 1 row, got {len(rows)}"
    if not isinstance(rows[0], dict):
        return False, "row is not a dict"
    return True, {"fieldnames": fieldnames, "rows": rows}

EXECUTORS = {
    "quoted_comma_field_marker": execute_quoted_comma,
    "multiline_text_field_marker": execute_multiline,
    "missing_column_dictreader_marker": execute_missing_column,
    "extra_column_dictreader_marker": execute_extra_column,
}

# ---- verify_relation ------------------------------------------------

def verify_quoted_comma(case, rows):
    if len(rows) != 2:
        return False, f"expected 2 logical rows, got {len(rows)}"
    header, data = rows
    if header != ["id", "text", "label"]:
        return False, f"header mismatch: {header}"
    if len(data) != 3:
        return False, f"expected 3 columns, got {len(data)}"
    if data[1] != "hello, world":
        return False, f"quoted comma field mismatch: {data[1]!r}"
    return True, "2 rows, 3 cols, quoted comma preserved"

def verify_multiline(case, rows):
    if len(rows) != 2:
        return False, f"expected 2 logical rows, got {len(rows)} (embedded newline treated as record separator?)"
    header, data = rows
    if header != ["id", "note"]:
        return False, f"header mismatch: {header}"
    if len(data) != 2:
        return False, f"expected 2 columns, got {len(data)}"
    expected_note = "line one\nline two"
    if data[1] != expected_note:
        return False, f"embedded newline not preserved: {data[1]!r}"
    return True, "2 logical rows, embedded newline preserved"

def verify_missing_column(case, result):
    rows = result["rows"]
    if len(rows) != 1:
        return False, f"expected 1 row, got {len(rows)}"
    d = rows[0]
    expected = {"a": "x", "b": "y", "c": "MISSING"}
    if d != expected:
        return False, f"dict mismatch: {d} vs {expected}"
    return True, 'missing field received "MISSING"'

def verify_extra_column(case, result):
    rows = result["rows"]
    if len(rows) != 1:
        return False, f"expected 1 row, got {len(rows)}"
    d = rows[0]
    if "__extra__" not in d:
        return False, "restkey __extra__ missing"
    if d["__extra__"] != ["extra"]:
        return False, f"extra value mismatch: {d['__extra__']}"
    # check base keys
    if d["a"] != "1" or d["b"] != "2" or d["c"] != "3":
        return False, f"base columns mismatch: {d}"
    return True, 'extra value collected under "__extra__"'

VERIFIERS = {
    "quoted_comma_field_marker": verify_quoted_comma,
    "multiline_text_field_marker": verify_multiline,
    "missing_column_dictreader_marker": verify_missing_column,
    "extra_column_dictreader_marker": verify_extra_column,
}

# ---- lab driver -----------------------------------------------------

def run_one_case(case):
    case_id = case["case_id"]
    results = []

    # inspect_inputs
    ok, detail = INSPECTORS[case_id](case)
    results.append({
        "case_id": case_id,
        "method": "inspect_inputs",
        "pass": ok,
        "detail": detail,
    })
    if not ok:
        return results, None

    # execute_parse
    ok, parsed = EXECUTORS[case_id](case)
    results.append({
        "case_id": case_id,
        "method": "execute_parse",
        "pass": ok,
        "detail": f"parsed {type(parsed).__name__}" if ok else str(parsed),
    })
    # execute_parse should always succeed for these cases
    if not ok:
        return results, parsed

    # verify_relation
    ok, detail = VERIFIERS[case_id](case, parsed)
    results.append({
        "case_id": case_id,
        "method": "verify_relation",
        "pass": ok,
        "detail": detail,
    })
    return results, parsed

def run_lab():
    all_rows = []
    for case in CASES:
        rows, _ = run_one_case(case)
        all_rows.extend(rows)
    return all_rows

def render_results(rows):
    """Render the twelve-row results table. Returns the text."""
    lines = []
    lines.append(f"{'case_id':<35} {'method':<18} {'result':<6} detail")
    lines.append("-" * 100)
    for r in rows:
        status = "PASS" if r["pass"] else "FAIL"
        lines.append(f"{r['case_id']:<35} {r['method']:<18} {status:<6} {r['detail']}")
    lines.append("")
    passed = sum(1 for r in rows if r["pass"])
    lines.append(f"{passed}/{len(rows)} rows passed")
    lines.append("")
    return "\n".join(lines)

def main():
    rows = run_lab()
    output = render_results(rows)
    print(output, end="")

    # write observations.json
    with open("observations.json", "w") as f:
        json.dump(rows, f, indent=2)

    # write RESULTS.md from same rows
    with open("RESULTS.md", "w") as f:
        f.write(output)

    return rows

if __name__ == "__main__":
    main()
