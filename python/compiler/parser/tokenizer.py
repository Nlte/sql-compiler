import re

from typing import List, Tuple, Any


TokenizerTraits = [
    ("^\d+", "NUMBER"),
    ("^\"[^\"]*\"", "STRING"),
    ("^'[^']*'", "STRING")
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
            print(elem)
            token_value = self._match(elem[0], string)
            if token_value is None:
                continue
            return {
                "type": elem[1],
                "value": token_value
            }

    def _match(self, regex: str, string: str) -> Any:
        pattern = re.compile(regex)
        match = pattern.match(string)
        value = None
        if match is not None:
            value = match.group()
            self._cursor += match.span()[-1]
        return value

    def has_next_token(self):
        return self._cursor < len(self._string)

    def is_eof(self):
        return self._cursor >= len(self._string)
