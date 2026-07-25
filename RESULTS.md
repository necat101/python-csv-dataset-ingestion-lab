case_id                             method             result detail
----------------------------------------------------------------------------------------------------
quoted_comma_field_marker           inspect_inputs     PASS   header ok, quoted comma field present
quoted_comma_field_marker           execute_parse      PASS   parsed list
quoted_comma_field_marker           verify_relation    PASS   2 rows, 3 cols, quoted comma preserved
multiline_text_field_marker         inspect_inputs     PASS   header ok, balanced quotes, 1 embedded newline
multiline_text_field_marker         execute_parse      PASS   parsed list
multiline_text_field_marker         verify_relation    PASS   2 logical rows, embedded newline preserved
missing_column_dictreader_marker    inspect_inputs     PASS   3 header fields, 2 data values, restval=MISSING
missing_column_dictreader_marker    execute_parse      PASS   parsed dict
missing_column_dictreader_marker    verify_relation    PASS   missing field received "MISSING"
extra_column_dictreader_marker      inspect_inputs     PASS   3 header fields, 4 data values, restkey=__extra__
extra_column_dictreader_marker      execute_parse      PASS   parsed dict
extra_column_dictreader_marker      verify_relation    PASS   extra value collected under "__extra__"

12/12 rows passed
