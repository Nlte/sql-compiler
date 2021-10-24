#include <mylib/lib.hpp>

#include <iostream>

int main() {

    std::cout << "app run" << std::endl;
    std::cout << "libfunction returns " << libfunction_returns_int(6)
              << std::endl;

    return 0;
}
