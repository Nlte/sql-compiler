from .tokenizer import Tokenizer
from .astfactory import DefaultFactory


__all__ = ("Parser",)


class Parser:
    """Recursive decent parser for SQL."""

    def __init__(self):
        self._string = ""
        self._tokenizer = Tokenizer()
        self._lookerhead = None
        self._factory = DefaultFactory()

    def parse(self, string: str):
        self._string = string
        self._tokenizer.init(string)
        self._lookahead = self._tokenizer.next_token()
        return self.StatementList()

    def StatementList(self, stop_lookahead = None):
        """
        StatementList
        | Statement
        : StatementList Statement
        ;
        """
        first_statement = self.Statement()
        if first_statement is None:
            return self._factory.StatementList([])
        statement_list = [first_statement]
        while (self._lookahead is not None) and (
            self._lookahead["type"] != stop_lookahead
        ):
            statement_list.append(self.Statement())
        return self._factory.StatementList(statement_list)

    def Statement(self):
        """
        Statement
            : SelectStatement
            ;
        """
        if self._lookahead is None:
            return None
        if self._lookahead["type"] == "SELECT":
            return self.SelectStatement()
        raise SyntaxError()

    def SelectStatement(self):
        """
        SelectStatement
        SELECT
        FROM
        [ WHERE ]
        [ GROUP BY ]
        """
        pass








