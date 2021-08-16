#include "ast.hpp"
#include <iostream>

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

    std::cout << root << std::endl;
    return 0;
}
