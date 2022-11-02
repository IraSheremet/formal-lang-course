from project.task2 import create_minimal_dfa_for_regex
from project.task6 import cfg_from_file
from project.task7_ecfg import *


def compare_with_ecfg1(actual: ECFG):
    expected_ecfg = ECFG(
        variables={Variable("S"), Variable("A")},
        productions={Variable("S"): Regex("A"), Variable("A"): Regex("(((S.S)|$)|b)")},
    )
    assert actual.variables == expected_ecfg.variables
    assert actual.start == expected_ecfg.start
    assert all(
        create_minimal_dfa_for_regex(actual.productions[var]).is_equivalent_to(
            create_minimal_dfa_for_regex(expected_ecfg.productions[var])
        )
        for var in expected_ecfg.productions.keys()
    )


def compare_with_ecfg2(actual: ECFG):
    expected_ecfg = ECFG(
        variables={Variable("S")},
        productions={Variable("S"): Regex("(((a.(S.b))|(S.S))|$)")},
    )
    assert actual.variables == expected_ecfg.variables
    assert actual.start == expected_ecfg.start
    assert all(
        create_minimal_dfa_for_regex(actual.productions[var]).is_equivalent_to(
            create_minimal_dfa_for_regex(expected_ecfg.productions[var])
        )
        for var in expected_ecfg.productions.keys()
    )


def test_ecfg_from_cfg1():
    cfg = cfg_from_file("tests/res/cfg1_task6")
    ecfg = ecfg_from_cfg(cfg)
    compare_with_ecfg1(ecfg)


def test_ecfg_from_cfg2():
    cfg = cfg_from_file("tests/res/cfg2_task6")
    ecfg = ecfg_from_cfg(cfg)
    compare_with_ecfg2(ecfg)


def test_ecfg1_from_text():
    text = """
        S -> A
        A -> (b | $ | S S)
        """
    ecfg = ecfg_from_text(text)
    compare_with_ecfg1(ecfg)


def test_ecfg2_from_text():
    text = """
        S -> (a S b | S S | $)
        """
    ecfg = ecfg_from_text(text)
    compare_with_ecfg2(ecfg)
