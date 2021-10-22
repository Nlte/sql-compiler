import unittest

from antlrsandbox.func import add_two


class TestFunction(unittest.TestCase):

    def test_add_two(self):
        res = add_two(2)
        assert isinstance(res, int)
        assert res == 4
