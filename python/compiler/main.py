from compiler.parser import Parser
import re

from pprint import pprint


p = Parser()
pprint(p.parse("""
/* comment
*
*/

  42;

"hello";
"""))

# pattern = re.compile('"[^"]*"')
# match = pattern.match('"abcd"')
# print(match)
