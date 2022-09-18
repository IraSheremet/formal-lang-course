import pytest
from pyformlang.finite_automaton import *
from pyformlang.regular_expression import Regex
import networkx as nx
import cfpq_data

from project.task2 import *


@pytest.mark.create_minimal_dfa_for_regex
def test_create_minimal_dfa_for_empty_regex():
    dfa = create_minimal_dfa_for_regex(Regex(""))
    assert dfa.is_empty()


@pytest.mark.create_minimal_dfa_for_regex
def test_create_minimal_dfa_for_regex_is_correct():
    dfa = create_minimal_dfa_for_regex(Regex("abc|d"))
    assert dfa.accepts([Symbol("d")])
    assert dfa.accepts([Symbol("abc")])
    assert not dfa.accepts([Symbol("a")])
    assert dfa.is_deterministic()


@pytest.mark.create_nfa_for_graph
def test_create_nfa_for_empty_graph():
    nfa = create_nfa_for_graph(nx.MultiDiGraph())
    assert nfa.is_empty()


@pytest.mark.create_nfa_for_graph
def test_create_nfa_for_graph_is_correct():
    graph = cfpq_data.labeled_two_cycles_graph(3, 3, labels=("A", "B"))
    actual_nfa = create_nfa_for_graph(graph, {0}, {5})

    expected_nfa = NondeterministicFiniteAutomaton()
    expected_nfa.add_start_state(State(0))
    expected_nfa.add_final_state(State(5))
    for (fr, to, label) in graph.edges(data="label"):
        expected_nfa.add_transition(State(fr), Symbol(label), State(to))

    assert actual_nfa.is_equivalent_to(expected_nfa)
