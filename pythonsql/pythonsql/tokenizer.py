import re

from typing import List, Tuple, Any


TokenizerTraits = [
    # Whitespaces --------------------------------------------------------------
    (r"^\s+", "NULL_TOKEN"),
    # Comment ------------------------------------------------------------------
    (r"^\/\/.*", "NULL_TOKEN"),
    (r"^\/*[\s\S]*?\*\/", "NULL_TOKEN"),
    # Numbers and strings ------------------------------------------------------
    (r"^\d+", "NUMBER"),
    (r"^\"([^\"]*)\"", "STRING"),
    (r"^'([^']*)'", "STRING"),
    # Delimiters, Special symbols ----------------------------------------------
    (r"^,", ","),
    (r"^\{", "{"),
    (r"^\}", "}"),
    (r"^\(", "("),
    (r"^\)", ")"),
    # Keywords -----------------------------------------------------------------
    # SELECT
    (r"^(?i:select)", "SELECT"),
    # FROM
    (r"^(?i:from)", "FROM"),
    # WHERE
    (r"^(?i:where)", "WHERE"),
    # GROUP BY
    (r"^(?i:group by)", "GROUPBY"),
    # LIMIT
    (r"^(?i:limit)", "LIMIT"),
    # JOIN
    (r"^(?i:join)", "JOIN"),
    # INNER JOIN
    (r"^(?i:inner join)", "INNER JOIN"),
    # LEFT JOIN
    (r"^(?i:left join)", "LEFT JOIN"),
    # Identifiers --------------------------------------------------------------
    (r"^\w+", "IDENTIFIER"),
]


class Tokenizer:

    # TODO parameterize this depending on the syntax (MySQL, PSQL etc.)
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
            if token_type == "NULL_TOKEN":
                return self.next_token()
            return {
                "type": token_type,
                "value": token_value
            }

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
