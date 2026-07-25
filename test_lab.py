#!/usr/bin/env python3
"""python-csv-dataset-ingestion-lab — test_lab.py"""
import unittest
import run_lab

class TestLab(unittest.TestCase):

    def test_quoted_comma_remains_one_field(self):
        case = run_lab.CASES[0]
        rows, _ = run_lab.run_one_case(case)
        # verify_relation is rows[2]
        self.assertTrue(rows[2]["pass"])
        # independent parse check
        import io, csv
        f = io.StringIO(case["csv_text"])
        parsed = list(csv.reader(f))
        self.assertEqual(parsed[1][1], "hello, world")

    def test_quoted_comma_two_rows_three_cols(self):
        case = run_lab.CASES[0]
        import io, csv
        f = io.StringIO(case["csv_text"])
        parsed = list(csv.reader(f))
        self.assertEqual(len(parsed), 2)
        self.assertEqual(len(parsed[1]), 3)

    def test_multiline_two_logical_rows_not_three(self):
        case = run_lab.CASES[1]
        import io, csv
        f = io.StringIO(case["csv_text"])
        parsed = list(csv.reader(f))
        self.assertEqual(len(parsed), 2)

    def test_multiline_embedded_newline_preserved(self):
        case = run_lab.CASES[1]
        import io, csv
        f = io.StringIO(case["csv_text"])
        parsed = list(csv.reader(f))
        self.assertEqual(parsed[1][1], "line one\nline two")

    def test_missing_field_receives_missing_marker(self):
        case = run_lab.CASES[2]
        import io, csv
        f = io.StringIO(case["csv_text"])
        reader = csv.DictReader(f, restval=case["restval"])
        rows = list(reader)
        self.assertEqual(rows[0]["c"], "MISSING")

    def test_missing_column_dict_keys_and_values(self):
        case = run_lab.CASES[2]
        import io, csv
        f = io.StringIO(case["csv_text"])
        reader = csv.DictReader(f, restval=case["restval"])
        rows = list(reader)
        expected = {"a": "x", "b": "y", "c": "MISSING"}
        self.assertEqual(rows[0], expected)

    def test_extra_value_collected_as_list_extra(self):
        case = run_lab.CASES[3]
        import io, csv
        f = io.StringIO(case["csv_text"])
        reader = csv.DictReader(f, restkey=case["restkey"])
        rows = list(reader)
        self.assertEqual(rows[0]["__extra__"], ["extra"])

    def test_extra_column_dict_uses_key_extra_extra(self):
        case = run_lab.CASES[3]
        import io, csv
        f = io.StringIO(case["csv_text"])
        reader = csv.DictReader(f, restkey=case["restkey"])
        rows = list(reader)
        self.assertIn("__extra__", rows[0])

    # corruption tests — call production input-check helpers
    def test_corrupt_quoted_comma_rejected(self):
        case = dict(run_lab.CASES[0])
        case["csv_text"] = 'id,text,label\n1,hello world,positive\n'  # comma removed, quotes removed
        ok, _ = run_lab.inspect_quoted_comma(case)
        self.assertFalse(ok)

    def test_corrupt_multiline_rejected(self):
        case = dict(run_lab.CASES[1])
        case["csv_text"] = 'id,note\n2,line one line two\n'  # no quotes, no embedded newline
        ok, _ = run_lab.inspect_multiline(case)
        self.assertFalse(ok)

    def test_corrupt_missing_column_rejected(self):
        case = dict(run_lab.CASES[2])
        case["restval"] = "WRONG"
        ok, _ = run_lab.inspect_missing_column(case)
        self.assertFalse(ok)

    def test_corrupt_extra_column_rejected(self):
        case = dict(run_lab.CASES[3])
        case["restkey"] = "wrong"
        ok, _ = run_lab.inspect_extra_column(case)
        self.assertFalse(ok)

    def test_twelve_rows_deterministic_unique_ordered(self):
        rows = run_lab.run_lab()
        self.assertEqual(len(rows), 12)
        expected = [
            ("quoted_comma_field_marker", "inspect_inputs"),
            ("quoted_comma_field_marker", "execute_parse"),
            ("quoted_comma_field_marker", "verify_relation"),
            ("multiline_text_field_marker", "inspect_inputs"),
            ("multiline_text_field_marker", "execute_parse"),
            ("multiline_text_field_marker", "verify_relation"),
            ("missing_column_dictreader_marker", "inspect_inputs"),
            ("missing_column_dictreader_marker", "execute_parse"),
            ("missing_column_dictreader_marker", "verify_relation"),
            ("extra_column_dictreader_marker", "inspect_inputs"),
            ("extra_column_dictreader_marker", "execute_parse"),
            ("extra_column_dictreader_marker", "verify_relation"),
        ]
        actual = [(r["case_id"], r["method"]) for r in rows]
        self.assertEqual(actual, expected)
        # uniqueness
        self.assertEqual(len(set(actual)), 12)
        # deterministic — run twice
        rows2 = run_lab.run_lab()
        self.assertEqual(rows, rows2)

if __name__ == "__main__":
    unittest.main(verbosity=2)
