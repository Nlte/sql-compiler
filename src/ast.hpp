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

    From(std::vector<Table*> &vec) {
        for (size_t i = 0; i < vec.size(); ++i) {
            tables.push_back(vec[i]);
        }
    }

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

class Predicate {
    public:
        ScalarExpression* left_;
        std::string comparator_;
        ScalarExpression* right_;

        Predicate(ScalarExpression* left,
                  const std::string& comp,
                  ScalarExpression* right):
            left_(left),
            comparator_(comp),
            right_(right)
        { }

    private:
    friend std::ostream &operator<<(std::ostream &os, const Predicate *p) {
        os << "{\n";
        os << "\"left\":";
        os << p->left_ << ",\n";
        os << "\"comparator\":";
        os << "\"" << p->comparator_ << "\",\n";
        os << "\"right\":";
        os << p->right_ << ",\n";
        os << "}\n";
        return os;
    }


};


class Condition {

    public:
        Condition():
            predicate_(nullptr),
            left_(nullptr),
            logical_op_(""),
            right_(nullptr)
        { }

        Condition(Predicate *p):
            predicate_(p),
            left_(nullptr),
            logical_op_(""),
            right_(nullptr)
        { }

        Condition(Condition *left, std::string& logical_op, Condition* right):
            predicate_(nullptr),
            left_(left),
            logical_op_(logical_op),
            right_(right)
        { }

        Condition* left() const {
            if (left_ == nullptr) {
                throw std::runtime_error("Condition: left condition is null");
            }
            return left_;
        }

        Condition* right() const {
            if (right_ == nullptr) {
                throw std::runtime_error("Condition: right condition is null");
            }
            return right_;
        }

        Predicate* predicate() const {
            if (predicate_ == nullptr) {
                throw std::runtime_error("Condition: predicate is null");
            }
            return predicate_;
        }

    private:
    Predicate *predicate_;
    Condition *left_;
    std::string logical_op_;
    Condition *right_;


};



class Where {
    /*
    ** Where is a binary tree of condition. Root node = last logical combination.
    */
    public:
        Where() { }
        Where(Condition *root):
            root_(root)
        { }

    private:
    Condition *root_;
    friend std::ostream &operator<<(std::ostream &os, const Where *w) {
        Condition *current = w->root_;
        if (current->predicate() != nullptr) {
            os << current->predicate();
        }
        return os;
    }

};

class Query {

    public:
    Query() : select(nullptr), from(nullptr) {}
    Select *select;
    From *from;
    Where *where;

    private:

    friend std::ostream &operator<<(std::ostream &os, const Query *q) {
        os << "{\n";
        os << "\"Select\":";
        os << q->select;
        os << "\"From\":";
        os << q->from;
        os << "\"Where\":";
        os << q->where;
        os << "}\n";
        return os;
    }
};

#endif // AST_H_
