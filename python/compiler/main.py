from compiler.parser.parser import Parser
import re


p = Parser()
print(p.parse("'abcd'"))

# pattern = re.compile('"[^"]*"')
# match = pattern.match('"abcd"')
# print(match)
