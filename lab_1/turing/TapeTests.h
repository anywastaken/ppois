#include "Tape.h"
#include "TuringMachine.h"
#include "TransitionRule.h"
#include "turing_header.h"
#include <UnitTest++/UnitTest++.h>
#include <fstream>

SUITE(TapeTests) {
    TEST(CreateTape) {
        Tape tape;
        tape.create({ 'a','b','c' });
        CHECK_EQUAL('a', tape.read());
    }

    TEST(WriteAtBeginning) {
        Tape tape;
        tape.create({ 'a' });
        tape.write('x');
        CHECK_EQUAL('x', tape.read());
    }

    TEST(MoveRightAndLeft) {
        Tape tape;
        tape.create({ '1','0','1' });
        CHECK_EQUAL('1', tape.read());
        tape.move(1);
        CHECK_EQUAL('0', tape.read());
        tape.move(-1);
        CHECK_EQUAL('1', tape.read());
    }

    TEST(MoveBeyondBoundsRight) {
        Tape tape;
        tape.create({ '1' });
        tape.move(1);
        tape.write('0');
        CHECK_EQUAL('0', tape.read());
    }

    TEST(MoveBeyondBoundsLeft) {
        Tape tape;
        tape.create({ '1' });
        tape.move(-1);
        tape.write('z');
        CHECK_EQUAL('z', tape.read());
    }

    TEST(WriteAndReadMultiple) {
        Tape tape;
        tape.create({ 'a' });
        tape.write('b');
        CHECK_EQUAL('b', tape.read());
        tape.move(1);
        tape.write('c');
        CHECK_EQUAL('c', tape.read());
    }

    TEST(PrintTape) {
        Tape tape;
        tape.create({ 'a','b' });
        tape.print();
        CHECK(true);
    }
}
