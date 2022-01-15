import logging

from pythonsql.tokenizer import Tokenizer
from pythonsql.parser import Parser


logging.basicConfig(level="DEBUG")

def main():
    p = Parser()
    ret = p.parse("""
        SELECT col1
        FROM table1
    """)
    print(ret)
