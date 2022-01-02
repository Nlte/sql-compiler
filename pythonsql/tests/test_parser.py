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
