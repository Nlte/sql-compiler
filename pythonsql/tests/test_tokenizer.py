import unittest

from pythonsql.tokenizer import Tokenizer


class TestTokenizer(unittest.TestCase):

    def setUp(self):
        self.tokenizer = Tokenizer()

    def test_whitespace(self):
        prog = """

        """
        self.tokenizer.init(prog)
        ret = self.tokenizer.next_token()
        assert ret is None

    def test_comment_single_line(self):
        prog = """

        // single comment
        """
        self.tokenizer.init(prog)
        ret = self.tokenizer.next_token()
        assert ret is None

    def test_comment_multiline(self):
        prog = """
        /*
        * Multiline comment
        */
        """
        self.tokenizer.init(prog)
        ret = self.tokenizer.next_token()
        assert ret is None

    def test_select(self):
        prog = """
        select
        """
        self.tokenizer.init(prog)
        ret = self.tokenizer.next_token()
        assert ret == {"type": "SELECT", "value": "select"}
        prog = """
        SELECT
        """
        self.tokenizer.init(prog)
        ret = self.tokenizer.next_token()
        assert ret == {"type": "SELECT", "value": "SELECT"}

    def test_from(self):
        prog = """
        from
        """
        self.tokenizer.init(prog)
        ret = self.tokenizer.next_token()
        assert ret == {"type": "FROM", "value": "from"}
        prog = """
        FROM
        """
        self.tokenizer.init(prog)
        ret = self.tokenizer.next_token()
        assert ret == {"type": "FROM", "value": "FROM"}

    def test_where(self):
        prog = """
        where
        """
        self.tokenizer.init(prog)
        ret = self.tokenizer.next_token()
        assert ret == {"type": "WHERE", "value": "where"}
        prog = """
        WHERE
        """
        self.tokenizer.init(prog)
        ret = self.tokenizer.next_token()
        assert ret == {"type": "WHERE", "value": "WHERE"}

    def test_groupby(self):
        prog = """
        group by
        """
        self.tokenizer.init(prog)
        ret = self.tokenizer.next_token()
        assert ret == {"type": "GROUPBY", "value": "group by"}
        prog = """
        GROUP BY
        """
        self.tokenizer.init(prog)
        ret = self.tokenizer.next_token()
        assert ret == {"type": "GROUPBY", "value": "GROUP BY"}
