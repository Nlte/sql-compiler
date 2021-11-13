import unittest

from compiler.parser import Parser


class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

    def test_init_unkown_ast_mode(self):
        with self.assertRaises(ValueError):
            Parser(ast_mode="unkown")

    def test_program_return_empty_program(self):
        prog = """
        """
        ret = self.parser.parse(prog)
        assert ret == {"type": "Program", "body": ""}

    def test_numeric_literal(self):
        prog = """
        1234;
        """
        ret = self.parser.parse(prog)
        assert ret == {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "value": {"type": "NumericLiteral", "value": 1234}
                }
            ]}

    def test_string_literal_double_quotes(self):
        prog = """
        "abcd";
        """
        ret = self.parser.parse(prog)
        assert ret == {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "value": {"type": "StringLiteral", "value": "abcd"}
                }
            ]}

    def test_string_literal_single_quotes(self):
        prog = """
        'abcd';
        """
        ret = self.parser.parse(prog)
        assert ret == {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "value": {"type": "StringLiteral", "value": "abcd"}
                }
            ]}


    def test_block(self):
        prog = """
        {
            1234;
            "abcd";
        }
        """
        ret = self.parser.parse(prog)
        assert ret == {
            "type": "Program",
            "body": [
                {
                    "type": "BlockStatement",
                    "body": [
                        {
                            "type": "ExpressionStatement",
                            "value": {"type": "NumericLiteral", "value": 1234}
                        },
                        {
                            "type": "ExpressionStatement",
                            "value": {"type": "StringLiteral", "value": "abcd"}
                        }
                    ]
                }
            ]
        }

    def test_block_empty(self):
        prog = """
        {
        }
        """
        ret = self.parser.parse(prog)
        assert ret == {
            "type": "Program",
            "body": [
                {
                    "type": "BlockStatement",
                    "body": [
                    ]
                }
            ]
        }


    def test_nested_blocks(self):
        prog = """
        {
            1234;
            {
                "abcd";
            }

        }
        """
        ret = self.parser.parse(prog)
        assert ret == {
            "type": "Program",
            "body": [
                {
                    "type": "BlockStatement",
                    "body": [
                        {
                            "type": "ExpressionStatement",
                            "value": {"type": "NumericLiteral", "value": 1234}
                        },
                        {
                            "type": "BlockStatement",
                            "body": [
                                {
                                    "type": "ExpressionStatement",
                                    "value": {"type": "StringLiteral", "value": "abcd"}
                                },
                            ]
                        }
                    ]
                }
            ]
        }
        
