#include <mylib/parser.hpp>

#include <iostream>
#include <map>
#include <string>

int main() {

    Parser parser;

    std::string s = "123";
    std::map<std::string, Parser::dict_type> ast = parser.parse(s);
    for (auto e : ast) {
      std::cout << e.first << ":" << std::endl;
      for (auto f: e.second)
        std::cout << f.first << " " << f.second << std::endl;
    }

    return 0;
}
