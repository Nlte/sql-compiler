#include <map>
#include <string>

#include "mylib/parser.hpp"

Parser::Parser() {}

Parser::~Parser() {}

std::map<std::string, Parser::dict_type>
Parser::parse(std::string &s) {
    string_ = s;
    return Program();
}

std::map<std::string, Parser::dict_type>
Parser::Program() {
  std::map<std::string, Parser::dict_type> ret = {
    {"body", NumericLiteral()}
  };
  return ret;
}

Parser::dict_type Parser::NumericLiteral() {
    dict_type ret = {{"type", "NumericLiteral"}, {"value", string_}};
    return ret;
}
