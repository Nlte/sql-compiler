from compiler.parser import Parser
import re

from pprint import pprint


p = Parser(ast_mode="sexpression")
pprint(p.parse("""
432;
"abcd";
"""))

# pattern = re.compile('"([^"]*)"')
# match = pattern.match('"abcd"')
# print(match.group(1))
# print(len(match.groups()))
