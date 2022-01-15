from typing import List, Dict, Any


class Factory:

    def StatementList(self, statements: List["Statement"]) -> Dict[str, Any]:
        raise NotImplementedError()

    def Literal(self, value, dtype):
        raise NotImplementedError()

    def StringLiteral(self, value):
        return self.Literal(value, "string")

    def NumericLiteral(self, value):
        return self.Literal(value, "numeric")

    def SelectStatement(self, columns, from_, where=None, groupby=None):
        raise NotImplementedError()

    def From(self, table):
        raise NotImplementedError()

    def Where(self, expressions):
        raise NotImplementedError()

    def Expression(self):
        raise NotImplementedError()

    def BinaryExpression(self, lhs, operator, rhs):
        raise NotImplementedError()

    def Table(self, name):
        raise NotImplementedError()


class DefaultFactory:


    def NumericLiteral(self, value):
        raise NotImplementedError()

    def StringLiteral(self, value):
        raise NotImplementedError()

    def Identifier(self, name):
        raise NotImplementedError()

    def Expression(self):
        pass

    def BinaryExpression(self, lhs, operator, rhs):
        pass

    def StatementList(self, statements: List["Statement"]) -> Dict[str, Any]:
        return {"type": "StatementList", "statements": statements}

    def SelectStatement(self, columns, from_, where=None, groupby=None):
        return {
            "type": "SelectStatement",
            "columns": columns,
            "from": from_,
            "where": where,
            "groupby": groupby
        }

    def From(self, table):
        return {
            "type": "From",
            "table": table
        }

    def Column(self, expression, alias=None):
        pass

    def Where(self, expressions):
        pass

    def NumericLiteral(self, value):
        return {
            "type": "NumericLiteral",
            "value": value
        }

    def StringLiteral(self, value):
        return {
            "type": "StringLiteral",
            "value": value
        }

    def Identifier(self, name):
        return {
            "type": "Identifier",
            "name": name
        }

    def Table(self, name):
        return {
            "type": "Table",
            "name": name
        }
