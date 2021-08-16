%code requires {
        #include "ast.hpp"
}

%{

#include <stdio.h>
#include <string.h>
#include <string>
#include <vector>
#include "ast.hpp"

extern char *yytext;

Query *root;

int yylex();
int yyparse();
void yyerror(const char*);

%}

/* symbolic tokens */

%union {
        int ival;
        double dval;
        std::string *sval;
        int subtok;
        Query *query;
        Select *select;
        ScalarExpression *scalarexp;
        ColumnRef *columnref;
        From *from;
        Table *table;
        std::vector<ScalarExpression*> *scalarexpvec;

}

%token NAME
%token STRING
%token INTNUM APPROXNUM

%type   <sval>          table_ref
%type   <sval>          NAME
%type   <ival>          INTNUM
%type   <dval>          APPROXNUM

/* operators */

%left OR
%left AND
%left NOT
%left <subtok> COMPARISON /* = <> < > <= >= */
%left '+' '-'
%left '*' '/'
%nonassoc UMINUS

/* literal keyword tokens */
%token SELECT FROM WHERE GROUP BY AS

%%

sql:
                select_statement
        ;

column_commalist:

                column
        |       column_commalist ',' column
        ;

select_statement:
                SELECT selection table_exp {
                        $<query>$ = new Query();
                        $<query>$->select = $<select>2;
                        $<query>$->from=$<from>3;
                        root = $<query>$;
                }
        ;

selection:
                scalar_exp_commalist
        |       '*'
        ;

scalar_exp_commalist:
                scalar_exp {
                        $<select>$ = new Select();
                        $<select>$->columns.push_back($<scalarexp>1);
                }
        |       scalar_exp_commalist ',' scalar_exp {
                        $<select>1->columns.push_back($<scalarexp>3);
                }
        ;

scalar_exp:
                column_ref { $<columnref>$ = new ColumnRef(*$<sval>1); }
        |       binary_op
        |       atom
        ;

column_ref:
                NAME
        |       NAME '.' NAME /* table.column */
        |       NAME '.' NAME '.' NAME /* schema.table.column */
        ;

binary_op:
                '(' scalar_exp '+' scalar_exp ')'
        |       '(' scalar_exp '-' scalar_exp ')'
        |       '(' scalar_exp '*' scalar_exp ')'
        |       '(' scalar_exp '/' scalar_exp ')'
        |       scalar_exp '+' scalar_exp
        |       scalar_exp '-' scalar_exp
        |       scalar_exp '*' scalar_exp
        |       scalar_exp '/' scalar_exp
        ;

atom:
                literal
        ;

literal:

        |       INTNUM
        |       APPROXNUM
        ;


table_exp:
                from_clause {
                        $<from>$ = $<from>1;
                        std::cout << "table_exp: num tables: " << $<from>1->tables.size() << '\n';
                }
                /* opt_where_clause */
                /* opt_group_by_clause */
        ;

from_clause:
                FROM table_ref_commalist {
                        $<from>$ = $<from>2;
                }
        ;

table_ref_commalist:
                table_ref {
                        $<from>$ = new From();
                        $<from>$->tables.push_back($<table>1);
                }
        |       table_ref_commalist ',' table_ref {
                        $<from>1->tables.push_back($<table>3);
                }
        ;

table_ref:
                table {
                        $<table>$ = new Table(*$<sval>1);
                        std::cout << "in table" << std::endl;
                }
        |       table NAME {
                        $<table>$ = new Table(*$<sval>1, *$<sval>2);
                        std::cout << "in table NAME" << std::endl;
                }
        |       table AS NAME {
                        $<table>$ = new Table(*$<sval>1, *$<sval>3);
                        std::cout << "in table AS NAME" << std::endl;
                }
        ;

table:
                NAME
        |       NAME '.' NAME /* schema.table */
        ;

column:
                NAME
        ;

opt_where_clause:
                /* empty */
        |       where_clause
        ;

where_clause:
                WHERE search_condition
        ;

        /*  search conditions */

search_condition:
        |       search_condition OR search_condition
        |       search_condition AND search_condition
        |       NOT search_condition
        |       '(' search_condition ')'
        |       predicate
        ;

predicate:
                comparison_predicate
        ;

comparison_predicate:
                scalar_exp COMPARISON scalar_exp
        ;

opt_group_by_clause:
            /* empty */
        |       GROUP BY column_ref_commalist
        ;

column_ref_commalist:
                column_ref
        |       column_ref_commalist ',' column_ref
        ;
