from pyformlang.regular_expression import Regex

from project.task2 import create_minimal_dfa_for_regex
from project.task7_ecfg import ecfg_from_text
from project.task7_rsm import *


def test_rsm_from_ecfg():
    text = """
        S -> A B C
        A -> i
        B -> r
        C -> (a | S)
        """
    ecfg = ecfg_from_text(text)
    rsm = rsm_from_ecfg(ecfg)
    expected_productions = {
        Variable("S"): Regex("A B C"),
        Variable("A"): Regex("i"),
        Variable("B"): Regex("r"),
        Variable("C"): Regex("(a | S)"),
    }
    assert rsm.start == Variable("S")
    assert all(
        rsm.boxes[var].is_equivalent_to(expected_productions[var].to_epsilon_nfa())
        for var in expected_productions.keys()
    )


def test_minimize_rsm():
    text = """
        S -> A B C
        A -> i
        B -> r
        C -> (a | S)
        """
    ecfg = ecfg_from_text(text)
    rsm = rsm_from_ecfg(ecfg)
    assert all(
        minimize_rsm(rsm).boxes[var]
        == create_minimal_dfa_for_regex(ecfg.productions[var])
        for var in ecfg.productions.keys()
    )
