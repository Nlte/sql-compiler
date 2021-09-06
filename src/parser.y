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
        Predicate *predicate;
        Condition *condition;
        Where *where;
        std::vector<ScalarExpression*> *scalarexpvec;
        std::vector<Table*> *tablevec;
        std::vector<Condition*> *conditionvec;
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
        SELECT selection
        FROM table_exp
        opt_where_clause {
                $<query>$ = new Query();
                $<query>$->select = $<select>2;
                $<query>$->from = $<from>4;
                $<query>$->where = $<where>5;
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
        |       NAME '.' NAME /* table.column */ {
                $<sval>$ = new std::string(*$<sval>1 + '.' + *$<sval>3);
        }
        |       NAME '.' NAME '.' NAME /* schema.table.column */ {
                $<sval>$ = new std::string(*$<sval>1 + '.' + *$<sval>3 + '.' + *$<sval>5);
        }
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
                }
        ;

from_clause:
                table_ref_commalist {
                        $<from>$ = new From(*$<tablevec>1);
                }
        ;

table_ref_commalist:
                table_ref {
                        $<tablevec>$ = new std::vector<Table*>();
                        $<tablevec>$->push_back($<table>1);
                }
        |       table_ref_commalist ',' table_ref {
                        $<tablevec>$->push_back($<table>3);
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
        |       NAME '.' NAME /* schema.table */ {
                $<sval>$ = new std::string(*$<sval>1 + '.' + *$<sval>3);
        }
        ;

column:
                NAME
        ;

opt_where_clause:
                /* empty */
        |       WHERE where_clause {
                // TODO Where clause from vector of cond
        }
        ;


where_clause:
        search_condition {
                // TODO vector
        }
        ;

        /*  search conditions */

search_condition:
        |       search_condition OR search_condition {
                        $<condition>$ = new Condition(
                                $<condition>1,
                                *$<sval>2,
                                $<condition>3
                        );
                }
        |       search_condition AND search_condition {
                        $<condition>$ = new Condition(
                                $<condition>1,
                                *$<sval>2,
                                $<condition>3
                        );
                }
        |       NOT search_condition
        |       '(' search_condition ')'
        |       predicate {
                        std::cout << "creating condition predicate" << std::endl;
                        $<condition>$ = new Condition($<predicate>1);
                        std::cout << "created condition predicate" << std::endl;
                }
        ;

predicate:
                comparison_predicate
        ;

comparison_predicate:
        scalar_exp COMPARISON scalar_exp {
                $<predicate>$ = new Predicate($<scalarexp>1, *$<sval>2, $<scalarexp>3);
        }
        ;

opt_group_by_clause:
            /* empty */
        |       GROUP BY column_ref_commalist
        ;

column_ref_commalist:
                column_ref
        |       column_ref_commalist ',' column_ref
        ;
