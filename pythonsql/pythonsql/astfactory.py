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


class DefaultFactory:

    def StatementList(self, statements: List["Statement"]) -> Dict[str, Any]:
        return {"type": "StatementList", "statements": statements}
