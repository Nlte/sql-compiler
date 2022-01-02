from pythonsql.tokenizer import Tokenizer


def main():
    t = Tokenizer()
    t.init("""
    SELECT
    """)
    ret = t.next_token()
    print(ret)
