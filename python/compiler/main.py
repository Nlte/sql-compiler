from compiler.parser import Parser
import re

from pprint import pprint


# p = Parser(ast_mode="sexpression")
p = Parser(ast_mode="default")
pprint(p.parse("1 + 2 + 3;"))

# pattern = re.compile('"([^"]*)"')
# match = pattern.match('"abcd"')
# print(match.group(1))
# print(len(match.groups()))
