from Scanner import *


def test_check_boolean():
    assert not check_boolean("")
    assert check_boolean("0")
    assert check_boolean("1")
    assert not check_boolean("a")


def test_check_integer():
    assert not check_integer("")
    assert check_integer("0")
    assert check_integer("+12")
    assert check_integer("-12")
    assert check_integer("12")
    assert not check_integer("7ab")
    assert not check_integer("+0")
    assert not check_integer("-0")
    assert not check_integer("+1.1")
    assert not check_integer("-1.1")
    assert not check_integer("1.1")
    assert not check_integer("012")


def test_check_real():
    assert not check_real("")
    assert check_real("0.0")
    assert check_real("1.01")
    assert check_real("+1.01")
    assert check_real("-1.01")
    assert not check_real("1.")
    assert not check_real(".1")
    assert not check_real("+0.0")
    assert not check_real("-0.0")
    assert not check_real("abc.0")
    assert not check_real("0.abc")


def test_check_character():
    assert not check_character("")
    assert check_character("\'a\'")
    assert check_character("\'1\'")
    assert not check_character("a")
    assert not check_character("\'a1\'")
    assert not check_character("\'$\'")


def test_check_string():
    assert not check_string("")
    assert check_string("\"\"")
    assert check_string("\"a\"")
    assert check_string("\"1\"")
    assert check_string("\"a1\"")
    assert not check_string("\"$a\"")
    assert not check_string("\'a\'")


def test_check_name():
    assert not check_name("")
    assert check_name("\"Az\"")
    assert check_name("\"David\"")
    assert not check_name("\"David1\"")
    assert not check_name("\"David$\"")
    assert not check_name("\'David\'")
    assert not check_name("David")


def test_check_identifier():
    assert not check_identifier("")
    assert check_identifier("a")
    assert check_identifier("David1")
    assert not check_identifier("1David")
    assert not check_identifier("David$")
    assert not check_identifier("7")


def test_check_identifier_regex():
    assert not check_identifier_regex("")
    assert check_identifier_regex("a")
    assert check_identifier_regex("David1")
    assert not check_identifier_regex("1David")
    assert not check_identifier_regex("David$")
    assert not check_identifier_regex("7")


test_check_boolean()
test_check_integer()
test_check_real()
test_check_character()
test_check_string()
test_check_name()

test_check_identifier()
test_check_identifier_regex()
