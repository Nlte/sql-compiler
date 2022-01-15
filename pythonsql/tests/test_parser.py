import unittest

from pythonsql.parser import Parser


class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_empty_program_returns_empty_statement_list(self):
        prog = """
        """
        ret = self.parser.parse(prog)
        assert ret == {"type": "StatementList", "statements": []}

    def test_comment_program_returns_empty_statement_list(self):
        prog = """
        /* Comment */
        """
        ret = self.parser.parse(prog)
        assert ret == {"type": "StatementList", "statements": []}

    def test_select_statement_missing_columns(self):
        prog = """
        SELECT
        """
        with self.assertRaises(SyntaxError):
            ret = self.parser.parse(prog)

    def test_select_statement_missing_from(self):
        prog = """
        SELECT col1
        """
        with self.assertRaises(SyntaxError):
            ret = self.parser.parse(prog)

    def test_select_statement_single_column(self):
        prog = """
        SELECT col1
        FROM table1
        """
        ret = self.parser.parse(prog)
        assert ret == {
            "type": "StatementList",
            "statements": [
                {
                    "type": "SelectStatement",
                    "columns": [{"type": "Identifier", "name": "col1"}],
                    "from": [{"type": "Table", "name": "table1"}],
                    "where": None,
                    "groupby": None,
                }
            ],
        }

    def test_select_statement_multiple_columns(self):
        prog = """
        SELECT col1, col2
        FROM table1
        """
        ret = self.parser.parse(prog)
        assert ret == {
            "type": "StatementList",
            "statements": [
                {
                    "type": "SelectStatement",
                    "columns": [
                        {"type": "Identifier", "name": "col1"},
                        {"type": "Identifier", "name": "col2"}
                    ],
                    "from": [{"type": "Table", "name": "table1"}],
                    "where": None,
                    "groupby": None,
                }
            ],
        }

    def test_select_statement_string_literal_column(self):
            prog = """
            SELECT col1, "abcd"
            FROM table1
            """
            ret = self.parser.parse(prog)
            assert ret == {
                "type": "StatementList",
                "statements": [
                    {
                        "type": "SelectStatement",
                        "columns": [
                            {"type": "Identifier", "name": "col1"},
                            {"type": "StringLiteral", "value": "abcd"}
                        ],
                        "from": [{"type": "Table", "name": "table1"}],
                        "where": None,
                        "groupby": None,
                    }
                ],
            }

    def test_select_statement_numeric_column(self):
            prog = """
            SELECT col1, 123
            FROM table1
            """
            ret = self.parser.parse(prog)
            assert ret == {
                "type": "StatementList",
                "statements": [
                    {
                        "type": "SelectStatement",
                        "columns": [
                            {"type": "Identifier", "name": "col1"},
                            {"type": "NumericLiteral", "value": "123"}
                        ],
                        "from": [{"type": "Table", "name": "table1"}],
                        "where": None,
                        "groupby": None,
                    }
                ],
            }
