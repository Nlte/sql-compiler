#ifndef AST_H_
#define AST_H_

#include <algorithm>
#include <iomanip>
#include <iostream>
#include <iterator>
#include <list>
#include <sstream>
#include <string>
#include <vector>

class Expression {
    public:
    virtual ~Expression() {}
};

class ScalarExpression : public Expression {
    public:
    ScalarExpression(const std::string &type) : type_(type) {}

    const std::string type() const { return type_; }
    virtual const std::string value() const = 0;

    private:
    friend std::ostream &operator<<(std::ostream &os,
                                    const ScalarExpression *s) {
        os << "{\n";
        os << "\"type\":\"" << s->type() << "\",\n";
        os << "\"value\":\"" << s->value() << "\"\n";
        os << "}\n";
        return os;
    }
    std::string type_;
};

class ColumnRef : public ScalarExpression {
    public:
    ColumnRef(const std::string &name)
        : ScalarExpression("ColumnRef"), name_(name) {}

    const std::string value() const { return name_; }

    private:
    std::string name_;
};

class Table {
    public:
    Table(std::string n) : name_(n), alias_("") {}
    Table(std::string n, std::string a) : name_(n), alias_(a) {}

    bool has_alias() const { return alias_ != ""; }

    const std::string &alias() const { return alias_; }
    const std::string &name() const { return name_; }

    private:
    std::string name_;
    std::string alias_;

    friend std::ostream &operator<<(std::ostream &os, const Table *t) {
        os << "{\n";
        os << "\"name\":\"" << t->name() << "\",\n";
        os << "\"alias\":\"" << t->alias() << "\"\n";
        os << "}\n";
        return os;
    }
};

class Select {

    public:
    Select() {}
    Select(const std::vector<ScalarExpression *> &vec) {
        std::copy(vec.begin(), vec.end(), columns.begin());
    }

    std::vector<ScalarExpression *> columns;

    private:
    friend std::ostream &operator<<(std::ostream &os, const Select *s) {
        os << "[\n";
        std::size_t i = 0;
        for (; i < s->columns.size() - 1; ++i) {
            os << s->columns[i];
            os << ",\n";
        }
        os << s->columns[i];
        os << "]\n";
        return os;
    }
};

class From {

    public:
    std::vector<Table *> tables;

    private:
    friend std::ostream &operator<<(std::ostream &os, const From *f) {
        os << "[\n";
        std::size_t i = 0;
        for (; i < f->tables.size() - 1; ++i) {
            os << f->tables[i];
            os << ",\n";
        }
        os << f->tables[i];
        os << "]\n";
        return os;
    }
};

class Query {

    public:
    Query() : select(nullptr), from(nullptr) {}
    Select *select;
    From *from;

    private:
    friend std::ostream &operator<<(std::ostream &os, const Query *q) {
        os << "{\n";
        os << "\"Select\":";
        os << q->select;
        os << "\"From\":";
        os << q->from;
        os << "}\n";
        return os;
    }
};

#endif // AST_H_
