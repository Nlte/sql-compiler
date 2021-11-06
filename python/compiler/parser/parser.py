from .tokenizer import Tokenizer

__all__ = ("Parser",)


class Parser:
    """Recursive decent parser.
    """

    def __init__(self,):
        self._string = ""
        self._lookahead = None
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
                :Literal
        ;
        """
        return {
            "type": "Program",
            "body": self.Literal()
        }

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
        return {
            "type": "NumericLiteral",
            "value": int(token["value"])
        }

    def StringLiteral(self):
        """StringLiteral
                : STRING
                ;
        """
        token = self._eat("STRING")
        return {
            "type": "StringLiteral",
            "value": str(token["value"])
        }
