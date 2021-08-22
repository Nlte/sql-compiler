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

    // ColumnRef *ref1 = new ColumnRef("media.name");
    // ColumnRef *ref2 = new ColumnRef("media.description");
    // Predicate *pred = new Predicate(ref1, "<", ref2);

    // std::cout << pred << std::endl;
    return 0;
}
