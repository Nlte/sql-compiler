from .tokenizer import Tokenizer
from .ast import DefaultFactory, SExpressionFactory

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
        """Parse a string into an AST.
        """
        self._string = string
        self._tokenizer.init(string)
        self._lookahead = self._tokenizer.next_token()
        return self.Program()

    def _eat(self, token_type: str):
        token = self._lookahead
        if token is None:
            raise SyntaxError(f"unexpected end of input, expected {token_type}")
        if token["type"] != token_type:
            raise SyntaxError(f"unexpected token {token['type']}, expected {token_type}")
        self._lookahead = self._tokenizer.next_token()
        return token

    def Program(self):
        """Main entrypoint.
        Program
                :StatementList
        ;
        """
        if self._lookahead is None:
            return self._factory.Program("")
        return self._factory.Program(self.StatementList())

    def StatementList(self, stop_lookahead = None):
        """
        StatementList
            : Statement
            | StatementList Statement
            ;
        """
        statement_list = [self.Statement()]
        while (self._lookahead is not None) and (self._lookahead["type"] != stop_lookahead):
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
        body = self.StatementList(stop_lookahead='}') if self._lookahead["type"] != '}' else []
        self._eat("}")
        return self._factory.BlockStatement(body)

    def ExpressionStatement(self):
        """
        ExpressionStatement
            : Expression ;
            ;
        """
        expression = self.Expression()
        self._eat(';')
        return self._factory.ExpressionStatement(expression)

    def Expression(self):
        """
        Expression:
            : Literal
            ;
        """
        return self.Literal()

    def Literal(self):
        """Literal
                :StringLiteral
                :NumericLiteral
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
