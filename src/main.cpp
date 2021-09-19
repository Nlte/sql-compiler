#include "ast.hpp"
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

extern FILE *yyin;
extern int yyparse();
extern Query *root;

int main(int argc, char *argv[]) {

    if (argc > 1 && (yyin = fopen(argv[1], "r")) == NULL) {
        perror(argv[1]);
        exit(1);
    }

    if (!yyparse()) {
        std::cout << "SQL parsed successfully" << std::endl;
    } else {
        std::cout << "SQL parsing error" << std::endl;
    };
    fclose(yyin);

    std::stringstream str_stream;
    std::ifstream f(argv[1]);
    if (f.is_open()) {
        str_stream << f.rdbuf();
        std::string str = str_stream.str();
        std::cout << "Query\n\n";
        std::cout << str << std::endl;
        std::cout << "\n\n";
    }

    std::cout << root << std::endl;

    // ColumnRef *ref1 = new ColumnRef("media.name");
    // ColumnRef *ref2 = new ColumnRef("media.description");
    // Predicate *pred = new Predicate(ref1, "<", ref2);

    // std::cout << pred << std::endl;
    return 0;
}
