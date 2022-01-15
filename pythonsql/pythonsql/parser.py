import logging
from .tokenizer import Tokenizer
from .astfactory import DefaultFactory


__all__ = ("Parser",)


LOG = logging.getLogger(__name__)


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
        LOG.debug("Begining parsing")
        return self.StatementList()

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

    def StatementList(self, stop_lookahead = None):
        """
        StatementList
        | Statement
        : StatementList Statement
        ;
        """
        LOG.debug("in StatementList")
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
        LOG.debug("in Statement")
        if self._lookahead is None:
            return None
        if self._lookahead["type"] == "SELECT":
            LOG.debug("Statement is SELECT statement")
            return self.SelectStatement()
        raise SyntaxError()

    def SelectStatement(self):
        """
        SelectStatement
        SELECT ExpressionList
        FROM Projection
        [ WHERE ]
        [ GROUP BY ]
        """
        LOG.debug("in SelectStatement")
        self._eat("SELECT")
        columns = self.ExpressionList(stop_lookahead="FROM")
        from_ = None
        self._eat("FROM")
        from_ = self.ProjectionList((None, "WHERE", "GROUPBY", "LIMIT"))
        if from_ is None:
            raise SyntaxError()
        return self._factory.SelectStatement(columns, from_)

    def ExpressionList(self, stop_lookahead):
        """
        ExpressionList
        : Expression
        | ExpressionList ',' Expression
        ;
        """
        LOG.debug("in ExpressionList")
        expression_list = [self.Expression()]
        while (self._lookahead is not None) and (self._lookahead["type"] != stop_lookahead):
            self._eat(",")
            expression_list.append(self.Expression())
        LOG.debug("return ExpressionList with #%d elements", len(expression_list))
        return expression_list

    def Expression(self):
        """
        Expression
        : Identifier
        | StringLiteral
        | NumberLiteral
        ;
        """
        LOG.debug("in Expression")
        if self._lookahead is None:
            raise SyntaxError()
        if self._lookahead["type"] == "IDENTIFIER":
            return self.Identifier()
        elif self._lookahead["type"] == "STRING":
            return self.StringLiteral()
        elif self._lookahead["type"] == "NUMBER":
            return self.NumericLiteral()
        raise SyntaxError()

    def Identifier(self):
        LOG.debug("in Identifier")
        name = self._eat("IDENTIFIER")["value"]
        node = self._factory.Identifier(name)
        LOG.debug("returning node %s", node)
        return node

    def StringLiteral(self):
        LOG.debug("in StringLiteral")
        value = self._eat("STRING")["value"]
        node = self._factory.StringLiteral(value)
        LOG.debug("returning node %s", node)
        return node

    def NumericLiteral(self):
        value = self._eat("NUMBER")["value"]
        node = self._factory.NumericLiteral(value)
        LOG.debug("returning node %s", node)
        return node

    def ProjectionList(self, stop_lookaheads=()):
        """
        ProjectionList
        : Projection
        | ProjectionList JOIN Projection
        """
        LOG.debug("in ProjectionList")
        projection_list = [self.Projection()]
        return projection_list

    def Projection(self):
        """
        Projection
        : Table
        | '(' SelectStatement ')'
        """
        LOG.debug("in Projection")
        if self._lookahead["type"] == "IDENTIFIER":
            return self.Table()
        raise SyntaxError()

    def Table(self):
        LOG.debug("in Table")
        name = self._eat("IDENTIFIER")["value"]
        node = self._factory.Table(name)
        LOG.debug("returning node %s", node)
        return node
