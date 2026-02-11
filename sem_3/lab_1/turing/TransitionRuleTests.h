#include "Tape.h"
#include "TuringMachine.h"
#include "TransitionRule.h"
#include "turing_header.h"
#include <UnitTest++/UnitTest++.h>
#include <fstream>

SUITE(TransitionRuleTests) {
    TEST(CreateTransitionRule) {
        TransitionRule rule;
        rule.current_state = 0;
        rule.new_state = 1;
        rule.current_symbol = 'a';
        rule.new_symbol = 'b';
        rule.move_direction = 1;

        CHECK_EQUAL(0, rule.current_state);
        CHECK_EQUAL(1, rule.new_state);
        CHECK_EQUAL('a', rule.current_symbol);
        CHECK_EQUAL('b', rule.new_symbol);
    }

    TEST(PrintRule) {
        TransitionRule rule;
        rule.current_state = 0;
        rule.new_state = 1;
        rule.current_symbol = 'a';
        rule.new_symbol = 'b';
        rule.move_direction = -1;
        rule.print(); 
        CHECK(true);
    }
}
