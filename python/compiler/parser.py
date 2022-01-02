from typing import Callable

from .tokenizer import Tokenizer
from .astfactory import DefaultFactory, SExpressionFactory

__all__ = ("Parser",)


class Parser:
    """Recursive decent parser."""

    def __init__(self, ast_mode: str = "default"):
        self._string = ""
        self._lookahead = None
        self._factory = None
        if ast_mode == "default":
            self._factory = DefaultFactory()
        elif ast_mode == "sexpression":
            self._factory = SExpressionFactory()
        else:
            raise ValueError("unkown ast mode")
        self._tokenizer = Tokenizer()

    def parse(self, string: str):
        """Parse a string into an AST."""
        self._string = string
        self._tokenizer.init(string)
        self._lookahead = self._tokenizer.next_token()
        return self.Program()

    def _eat(self, token_type: str):
        token = self._lookahead
        if token is None:
            raise SyntaxError(f"unexpected end of input, expected {token_type}")
        if token["type"] != token_type:
            raise SyntaxError(
                f"unexpected token {token['type']}, expected {token_type}"
            )
        self._lookahead = self._tokenizer.next_token()
        return token

    def Program(self):
        """Main entrypoint.
        Program
            : StatementList
            ;
        """
        if self._lookahead is None:
            return self._factory.Program("")
        return self._factory.Program(self.StatementList())

    def StatementList(self, stop_lookahead=None):
        """
        StatementList
            : Statement
            | StatementList Statement
            ;
        """
        statement_list = [self.Statement()]
        while (self._lookahead is not None) and (
            self._lookahead["type"] != stop_lookahead
        ):
            statement_list.append(self.Statement())
        return statement_list

    def Statement(self):
        """
        Statement
            : ExpressionStatement
            | BlockStatement
            ;
        """
        if self._lookahead["type"] == "{":
            return self.BlockStatement()
        return self.ExpressionStatement()

    def BlockStatement(self):
        """
        BlockStatement
            : '{' OptStatementList '}'
            ;
        """
        self._eat("{")
        body = (
            self.StatementList(stop_lookahead="}")
            if self._lookahead["type"] != "}"
            else []
        )
        self._eat("}")
        return self._factory.BlockStatement(body)

    def ExpressionStatement(self):
        """
        ExpressionStatement
            : Expression ;
            ;
        """
        expression = self.Expression()
        self._eat(";")
        return self._factory.ExpressionStatement(expression)

    def Expression(self):
        """
        Expression:
            : AssignmentExpression
            ;
        """
        return self.AssignmentExpression()

    def AssignmentExpression(self):
        """
        AssignmentExpression
        : AdditiveExpression
        | LeftHandSideExpression AssignmentOperator AssignmentExpression
        ;
        """
        left = self.AdditiveExpression()
        if not Parser._isAssignmentOperator(self._lookahead["type"]):
            return left
        return self._factory.AssignmentExpression(
            Parser._checkValidAssignmentTarget(left),
            self.AssignmentOperator()["value"],
            self.AssignmentExpression(),
        )

    @staticmethod
    def _isAssignmentOperator(token_type):
        return (token_type == "SIMPLE_ASSIGNMENT") or (
            token_type == "COMPLEX_ASSIGNMENT"
        )

    @staticmethod
    def _checkValidAssignmentTarget(node):
        if node["type"] == "Identifier":
            return node
        raise SyntaxError("Invalid left hand side in assignment expression.")

    def AssignmentOperator(self):
        """
        AssingmentOperator
        : SIMPLE_ASSIGNMENT
        | COMPLEX_ASSIGNMENT
        ;
        """
        if self._lookahead["type"] == "SIMPLE_ASSIGNMENT":
            return self._eat("SIMPLE_ASSIGNMENT")
        return self._eat("COMPLEX_ASSIGNMENT")

    def LeftHandSideExpression(self):
        """
        LeftHandSideExpression
        : Identifier
        ;
        """
        return self.Identifier()

    def Identifier(self):
        name = self._eat("IDENTIFIER")["value"]
        return self._factory.Identifier(name)

    def AdditiveExpression(self):
        """
        AdditiveExpression
            : MultiplicativeExpression
            | AdditiveExpression ADDITIVE_OPERATOR MultiplicativeExpression
            ;
        """
        return self._BinaryExpression(
            self.MultiplicativeExpression, "ADDITIVE_OPERATOR"
        )

    def MultiplicativeExpression(self):
        """
        MultiplicativeExpression
            : PrimaryExpression
            | MultiplicativeExpression MULTIPLICATIVE_OPERATOR PrimaryExpression
            ;
        """
        return self._BinaryExpression(self.PrimaryExpression, "MULTIPLICATIVE_OPERATOR")

    def _BinaryExpression(self, builder_name: Callable, operator_token: str):
        """Generic binary expression"""
        left = builder_name()
        while self._lookahead["type"] == operator_token:
            operator = self._eat(operator_token)
            right = builder_name()
            left = self._factory.BinaryExpression(left, operator["value"], right)
        return left

    def PrimaryExpression(self):
        """
        PrimaryExpression
        : Literal
        | ParenthesizedExpression
        | LeftHandSideExpression
        ;
        """
        if Parser._isLiteral(self._lookahead["type"]):
            return self.Literal()
        if self._lookahead["type"] == "(":
            return self.ParenthesizedExpression()
        return self.LeftHandSideExpression()

    @staticmethod
    def _isLiteral(token_type):
        return (token_type == "NUMBER") or (token_type == "STRING")

    def ParenthesizedExpression(self):
        """
        ParenthesizedExpression
        : '(' Expression ')'
        ;
        """
        self._eat("(")
        expr = self.Expression()
        self._eat(")")
        return expr

    def Literal(self):
        """Literal
        : StringLiteral
        | NumericLiteral
        ;
        """
        if self._lookahead["type"] == "NUMBER":
            return self.NumericLiteral()
        if self._lookahead["type"] == "STRING":
            return self.StringLiteral()
        raise SyntaxError("Literal: unexpected literal token.")

    def NumericLiteral(self):
        """NumericLiteral
        : NUMBER
        ;
        """
        token = self._eat("NUMBER")
        return self._factory.NumericLiteral(int(token["value"]))

    def StringLiteral(self):
        """StringLiteral
        : STRING
        ;
        """
        token = self._eat("STRING")
        return self._factory.StringLiteral(str(token["value"]))
