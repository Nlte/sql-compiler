%{
/* #include <stdio.h> */
#include <string.h>
#include <iostream>
#include <string>
#include <cstdlib>
#include "parser.hpp"

#define SAVE_TOKEN yylval.sval = new std::string(yytext, yyleng)
#define TOKEN(t) (yylval.token = t)
#define TOKEN_STR(t, val) (yylval.token = t; yylval.sval = new std::string(yytext); )
#define TOKEN_INT(t, val) (yylval.token = t; yylval.ival = std::atoi(yytext); )
#define TOKEN_DOUBLE(t, val) (yylval.token = t; yylval.dval = std::atof(yytext); )
int yyparse();
void yyerror(const char*);
/* extern "C" int yywrap() { } */

%}

%%

    /* literal keyword tokens */
SELECT { SAVE_TOKEN; return SELECT; }
FROM { SAVE_TOKEN; return FROM; }
WHERE { SAVE_TOKEN; return WHERE; }
GROUP { SAVE_TOKEN; return GROUP; }
BY { SAVE_TOKEN; return BY; }
AS { SAVE_TOKEN; return AS; }


    /* comparison operators */
"=" |
"<>" |
"!=" |
"<" |
">" |
"<=" |
">=" { yylval.sval = new std::string(yytext); return COMPARISON; }


    /* punctuations */
[-+*/:(),.;] { return yytext[0]; }


    /* names */
[a-zA-Z][A-Za-z0-9_]* { yylval.sval = new std::string(yytext); return NAME; }


    /* numbers */
[0-9]+ |
[0-9]+"."[0-9]* |
"."[0-9]* { return INTNUM; }

[0-9]+[eE][+-]?[0-9]+ |
[0-9]+"."[0-9]*[eE][+-]?[0-9]+ |
"."[0-9]*[eE][+-]?[0-9]+ { return APPROXNUM; }


    /* strings */
\"([^\\\"]|\\.)*\"  { return STRING; }

'[^'\n]*$ { yyerror("Unterminated string"); }

\n  yylineno++;


    /* whitespace */
[ \t\r]+ ;


    /* comment */
"--".*$ ;


%%

void yyerror(const char *s)
{
    printf("%d: %s at %s\n", yylineno, s, yytext);
}

/* int main(int argc, char ** argv) */
/* { */
/*     if (argc > 1 && (yyin = fopen(argv[1], "r")) == NULL) { */
/*         perror(argv[1]); */
/*         exit(1); */
/*     } */

/*     if(!yyparse()) { */
/*         std::cout << "SQL parsed successfully" << std::endl; */
/*         if (query->from == nullptr) { */
/*             std::cout << "from field is null" << std::endl; */
/*         } */

/*         if (query->select == nullptr) { */
/*             std::cout << "select field is null" << std::endl; */
/*         } */
/*         else { */
/*             std::cout << "select field is not null" << std::endl; */
/*         } */
/*     } else { */
/*         std::cout << "SQL parsing error" << std::endl; */
/*     } */


/*     return 0; */
/* } */