#pragma once
#include "Rule.h"
#include <UnitTest++/UnitTest++.h>
#include <fstream>
#include <cstdio>

SUITE(RuleTests) {
    TEST(DefaultConstructor) {
        Rule r;
        CHECK_EQUAL("", r.pattern);
        CHECK_EQUAL("", r.result);
    }

    TEST(ParameterizedConstructor) {
        Rule r("a", "b");
        CHECK_EQUAL("a", r.pattern);
        CHECK_EQUAL("b", r.result);
    }

    TEST(EqualityOperator_True) {
        Rule r1("a", "b");
        Rule r2("a", "b");
        CHECK(r1 == r2);
    }

    TEST(EqualityOperator_False) {
        Rule r1("a", "b");
        Rule r2("a", "c");
        CHECK(!(r1 == r2));
    }
}
