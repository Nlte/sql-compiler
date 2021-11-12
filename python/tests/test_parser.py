import unittest

from compiler.parser import Parser


class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

    def test_program_return_empty_program(self):
        prog = """
        """
        ret = self.parser.parse(prog)
        assert ret == {"type": "Program", "body": ""}

    def test_numeric_literal(self):
        prog = """
        1234
        """
        ret = self.parser.parse(prog)
        assert ret == {"type": "Program",
                       "body": {"type": "NumericLiteral", "value": 1234}}

