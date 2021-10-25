#ifndef PARSER_H_
#define PARSER_H_

#include <map>
#include <string>

class Parser {

    public:
    using dict_type = std::map<std::string, std::string>;

    Parser();
    virtual ~Parser();

    std::map<std::string, dict_type>
    parse(std::string &);
    std::map<std::string, dict_type> Program();
    dict_type NumericLiteral();

    private:
    std::string string_;
};

#endif /* PARSER_H_ */
