import re

from typing import List, Tuple, Any


TokenizerTraits = [
    # Whitespaces
    (r"^\s+", "NULL"),
    # Comment
    (r"^\/\/.*", "NULL"),
    (r"^\/*[\s\S]*?\*\/", "NULL"),
    # Numbers
    (r"^\d+", "NUMBER"),
    # Strings
    (r"^\"([^\"]*)\"", "STRING"),
    (r"^'([^']*)'", "STRING"),
    # Delimiters, Special symbols
    (r"^;", ";"),
    (r"^\{", "{"),
    (r"^\}", "}"),
    (r"^\(", "("),
    (r"^\)", ")"),
    # Keywords
    (r"^let", "LET"),
    # Identifiers
    (r"^\w+", "IDENTIFIER"),
    # Asignments operators: =, +=, -=, *=, /=
    (r"^=", "SIMPLE_ASSIGNMENT"),
    (r"^[\+\-\*\/]=", "COMPLEX_ASSIGNMENT"),
    # Math operators
    (r"^[+\-]", "ADDITIVE_OPERATOR"),
    (r"^[\*\\]", "MULTIPLICATIVE_OPERATOR"),
]


class Tokenizer:

    QUOTES = "\"\'"

    def __init__(self, traits: List[Tuple] = None):
        self._traits = traits if traits is not None else TokenizerTraits

    def init(self, string: str):
        self._string = string
        self._cursor = 0

    def next_token(self):
        if not self.has_next_token():
            return None
        string = self._string[self._cursor:]
        for elem in self._traits:
            token_value = self._match(elem[0], string)
            token_type = elem[1]
            if token_value is None:
                continue
            if token_type == "NULL":
                return self.next_token()
            return {
                "type": token_type,
                "value": token_value
            }
        raise ValueError("Unexpected token: %s" % string)

    def _match(self, regex: str, string: str) -> Any:
        pattern = re.compile(regex)
        match = pattern.match(string)
        value = None
        if match is not None:
            if len(match.groups()) > 0:
                value = match.group(1)
            else: 
                value = match.group()
            self._cursor += match.span()[-1]
        return value

    def has_next_token(self):
        return self._cursor < len(self._string)

    def is_eof(self):
        return self._cursor >= len(self._string)
