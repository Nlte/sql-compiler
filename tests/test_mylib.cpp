#include <gtest/gtest.h>

#include "mylib/lib.hpp"

TEST(TestLibFunction, ReturnsValue) {
    int ret = libfunction_returns_int(6);
    EXPECT_EQ(ret, 6);
}
