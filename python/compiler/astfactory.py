class Factory:

    def Program(self, body):
        raise NotImplementedError()

    def ExpressionStatement(self, expr):
        raise NotImplementedError()

    def BlockStatement(self, body):
        raise NotImplementedError()

    def NumericLiteral(self, value):
        raise NotImplementedError()

    def StringLiteral(self, value):
        raise NotImplementedError()

    def BinaryExpression(self, left, operator, right):
        raise NotImplementedError()

    def AssignmentExpression(self, left, operator, right):
        raise NotImplementedError()

    def Identifier(self, name):
        raise NotImplementedError()


class DefaultFactory:

    def Program(self, body):
        return {
            "type": "Program",
            "body": body
        }

    def ExpressionStatement(self, expr):
        return {
            "type": "ExpressionStatement",
            "expression": expr
        }

    def BlockStatement(self, body):
        return {
            "type": "BlockStatement",
            "body": body
        }

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

    def BinaryExpression(self, left, operator, right):
        return {
            "type": "BinaryExpression",
            "operator": operator,
            "left": left,
            "right": right
        }

    def AssignmentExpression(self, left, operator, right):
        return {
            "type": "AssignmentExpression",
            "operator": operator,
            "left": left,
            "right": right
        }

    def Identifier(self, name):
        return {
            "type": "Identifier",
            "name": name
        }


class SExpressionFactory:

    def Program(self, body):
        return ['begin', body]

    def ExpressionStatement(self, expr):
        return expr

    def BlockStatement(self, block):
        return ["begin", block]

    def NumericLiteral(self, value):
        return value

    def StringLiteral(self, value):
        return value

    def BinaryExpression(self, left, operator, right):
        return [operator, left, right]

    def AssignmentExpression(self, left, operator, right):
        return [operator, left, right]

    def Identifier(self, name):
        return name
