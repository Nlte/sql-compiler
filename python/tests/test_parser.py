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
                    "expression": {"type": "NumericLiteral", "value": 1234},
                }
            ],
        }

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
                    "expression": {"type": "StringLiteral", "value": "abcd"},
                }
            ],
        }

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
                    "expression": {"type": "StringLiteral", "value": "abcd"},
                }
            ],
        }

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
                            "expression": {"type": "NumericLiteral", "value": 1234},
                        },
                        {
                            "type": "ExpressionStatement",
                            "expression": {"type": "StringLiteral", "value": "abcd"},
                        },
                    ],
                }
            ],
        }

    def test_block_empty(self):
        prog = """
        {
        }
        """
        ret = self.parser.parse(prog)
        assert ret == {
            "type": "Program",
            "body": [{"type": "BlockStatement", "body": []}],
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
                            "expression": {"type": "NumericLiteral", "value": 1234},
                        },
                        {
                            "type": "BlockStatement",
                            "body": [
                                {
                                    "type": "ExpressionStatement",
                                    "expression": {
                                        "type": "StringLiteral",
                                        "value": "abcd",
                                    },
                                },
                            ],
                        },
                    ],
                }
            ],
        }

    def test_binary_expression_sum(self):
        prog = """
        2 + 2;
        """
        ret = self.parser.parse(prog)
        assert ret == {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "BinaryExpression",
                        "operator": "+",
                        "left": {"type": "NumericLiteral", "value": 2},
                        "right": {"type": "NumericLiteral", "value": 2},
                    },
                }
            ],
        }

    def test_binary_expression_sum_left_association(self):
        # left to right arithmetics
        prog = """
        1 + 2 - 3;
        """
        ret = self.parser.parse(prog)
        assert ret == {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "BinaryExpression",
                        "operator": "-",
                        "left": {
                            "type": "BinaryExpression",
                            "operator": "+",
                            "left": {"type": "NumericLiteral", "value": 1},
                            "right": {"type": "NumericLiteral", "value": 2},
                        },
                        "right": {"type": "NumericLiteral", "value": 3},
                    },
                }
            ],
        }

    def test_binary_expression_multiplication(self):
        prog = """
        2 * 2;
        """
        ret = self.parser.parse(prog)
        assert ret == {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "BinaryExpression",
                        "operator": "*",
                        "left": {"type": "NumericLiteral", "value": 2},
                        "right": {"type": "NumericLiteral", "value": 2},
                    },
                }
            ],
        }

    def test_binary_expression_multiplication_left_association(self):
        prog = """
        2 * 2 * 3;
        """
        ret = self.parser.parse(prog)
        assert ret == {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "BinaryExpression",
                        "operator": "*",
                        "left": {
                            "type": "BinaryExpression",
                            "operator": "*",
                            "left": {"type": "NumericLiteral", "value": 2},
                            "right": {"type": "NumericLiteral", "value": 2},
                        },
                        "right": {"type": "NumericLiteral", "value": 3},
                    },
                }
            ],
        }

    def test_binary_expression_multiplication_precedence(self):
        prog = """
        2 + 2 * 3;
        """
        ret = self.parser.parse(prog)
        assert ret == {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "BinaryExpression",
                        "operator": "+",
                        "left": {
                            "type": "NumericLiteral",
                            "value": 2
                        },
                        "right": {
                            "type": "BinaryExpression",
                            "operator": "*",
                            "left": {"type": "NumericLiteral", "value": 2},
                            "right": {"type": "NumericLiteral", "value": 3}
                        },
                    },
                }
            ],
        }

    def test_primary_expression_parenthesis_literal(self):
        prog = """
        (2);
        """
        ret = self.parser.parse(prog)
        assert ret == {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "NumericLiteral",
                        "value": 2
                    }
                }
            ]
        }

    def test_primary_expression_parenthesis_expression(self):
        prog = """
        (2 + 2);
        """
        ret = self.parser.parse(prog)
        assert ret == {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "BinaryExpression",
                        "operator": "+",
                        "left": {"type": "NumericLiteral", "value": 2},
                        "right": {"type": "NumericLiteral", "value": 2}
                    }
                }
            ]
        }

    def test_binary_expression_parenthesis_precedence(self):
        prog = """
        (2 + 2) * 3;
        """
        ret = self.parser.parse(prog)
        assert ret == {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "BinaryExpression",
                        "operator": "*",
                        "left": {
                            "type": "BinaryExpression",
                            "operator": "+",
                            "left": {"type": "NumericLiteral", "value": 2},
                            "right": {"type": "NumericLiteral", "value": 2}
                        },
                        "right": {
                            "type": "NumericLiteral",
                            "value": 3
                        }
                    }
                }
            ]
        }

    def test_assignment(self):
        prog = """
        x = 2;
        """
        ret = self.parser.parse(prog)
        assert ret == {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "AssignmentExpression",
                        "operator": "=",
                        "left": {
                            "type": "Identifier",
                            "name": "x"
                        },
                        "right": {
                            "type": "NumericLiteral",
                            "value": 2
                        }
                    }
                }
            ]
        }

    def test_assignment_chained(self):
        prog = """
        x = y = 2;
        """
        ret = self.parser.parse(prog)
        assert ret == {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "AssignmentExpression",
                        "operator": "=",
                        "left": {
                            "type": "Identifier",
                            "name": "x"
                        },
                        "right": {
                            "type": "AssignmentExpression",
                            "operator": "=",
                            "left": {
                                "type": "Identifier",
                                "name": "y"
                            },
                            "right": {
                                "type": "NumericLiteral",
                                "value": 2
                            }
                        }
                    }
                }
            ]
        }

    def test_assignment_invalid_lhs(self):
        prog = """
        2 = 2;
        """
        with self.assertRaises(SyntaxError):
            self.parser.parse(prog)

    def test_variable_declaration(self):
        prog = """
        let x = 2;
        """
        ret = self.parser.parse(prog)
        assert ret == {
            "type": "Program",
            "body": [
                {
                    "type": "VariableStatement",
                    "declarations": [
                        {
                            "type": "VariableDeclaration",
                            "id": {
                                "type": "Identifier",
                                "name": "x"
                            },
                            "init": {
                                "type": "NumericLiteral",
                                "value": 2
                            }
                        }
                    ]
                }
            ]
        }


    def test_variable_declarations(self):
        prog = """
        let x, y = 2;
        """
        ret = self.parser.parse(prog)
        assert ret == {
            "type": "Program",
            "body": [
                {
                    "type": "VariableStatement",
                    "declarations": [
                        {
                            "type": "VariableDeclaration",
                            "id": {
                                "type": "Identifier",
                                "name": "x"
                            },
                            "init": {
                                "type": "NumericLiteral",
                                "value": 2
                            }
                        },
                        {
                            "type": "VariableDeclaration",
                            "id": {
                                "type": "Identifier",
                                "name": "y"
                            },
                            "init": {
                                "type": "NumericLiteral",
                                "value": 2
                            }
                        }
                    ]
                }
            ]
        }

    def test_variable_empty_declarations(self):
        prog = """
        let x, y;
        """
        ret = self.parser.parse(prog)
        assert ret == {
            "type": "Program",
            "body": [
                {
                    "type": "VariableStatement",
                    "declarations": [
                        {
                            "type": "VariableDeclaration",
                            "id": {
                                "type": "Identifier",
                                "name": "x"
                            },
                            "init": "null"
                        },
                        {
                            "type": "VariableDeclaration",
                            "id": {
                                "type": "Identifier",
                                "name": "y"
                            },
                            "init": "null"
                        }
                    ]
                }
            ]
        }
