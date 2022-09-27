import cfpq_data
from pyformlang.finite_automaton import Symbol

from project.task3 import *


def test_decomposition_empty_nfa():
    nfa = EpsilonNFA()
    decomposition = BoolDecomposition(nfa)
    assert not decomposition.start_states
    assert not decomposition.final_states
    assert not decomposition.state_to_index
    assert not decomposition.bool_matrix
    assert decomposition.all_states == 0


def test_decomposition_non_empty_nfa():
    nfa = EpsilonNFA()
    nfa.add_start_state(State(0))
    nfa.add_final_state(State(2))
    nfa.add_transition(State(0), Symbol("a"), State(1))
    nfa.add_transition(State(1), Symbol("b"), State(2))
    nfa.add_transition(State(0), Symbol("c"), State(0))
    decomposition = BoolDecomposition(nfa)
    assert decomposition.start_states == {State(0)}
    assert decomposition.final_states == {State(2)}
    assert decomposition.state_to_index == {State(0): 0, State(1): 1, State(2): 2}
    assert decomposition.all_states == 3


def test_intersect_nfa_with_empty_nfa():
    nfa = EpsilonNFA()
    nfa.add_start_state(State(0))
    nfa.add_transition(State(0), Symbol("b"), State(1))
    decomposed_nfa = BoolDecomposition(nfa)
    empty_nfa = EpsilonNFA()
    decomposed_empty_nfa = BoolDecomposition(empty_nfa)
    intersection = BoolDecomposition.intersect_automata(
        decomposed_nfa, decomposed_empty_nfa
    )
    assert not intersection.start_states
    assert not intersection.final_states
    assert not intersection.state_to_index
    assert not intersection.bool_matrix
    assert intersection.all_states == 0


def test_intersect_two_nfa():
    nfa1 = EpsilonNFA()
    nfa1.add_start_state(State(0))
    nfa1.add_final_state(State(1))
    nfa1.add_transition(State(0), Symbol("b"), State(1))
    nfa1.add_transition(State(1), Symbol("a"), State(1))
    decomposed_nfa1 = BoolDecomposition(nfa1)

    nfa2 = EpsilonNFA()
    nfa2.add_start_state(State(0))
    nfa2.add_final_state(State(2))
    nfa2.add_transition(State(0), Symbol("d"), State(0))
    nfa2.add_transition(State(0), Symbol("b"), State(1))
    nfa2.add_transition(State(1), Symbol("d"), State(1))
    nfa2.add_transition(State(1), Symbol("a"), State(2))
    decomposed_nfa2 = BoolDecomposition(nfa2)

    actual_intersection = BoolDecomposition.intersect_automata(
        decomposed_nfa1, decomposed_nfa2
    )

    expected_nfa = EpsilonNFA()
    expected_nfa.add_start_state(State(0))
    expected_nfa.add_final_state(State(5))
    expected_nfa.add_transition(State(0), Symbol("b"), State(4))
    expected_nfa.add_transition(State(4), Symbol("a"), State(5))

    expected_intersection = BoolDecomposition(expected_nfa)

    assert actual_intersection.all_states == len(nfa1.states) * len(nfa2.states)
    assert actual_intersection.start_states == expected_intersection.start_states
    assert actual_intersection.final_states == expected_intersection.final_states
    for label in actual_intersection.bool_matrix.keys():
        assert (
            actual_intersection.bool_matrix[label].nnz
            == expected_intersection.bool_matrix[label]
        ).nnz


def test_regular_path_querying():
    graph = cfpq_data.labeled_two_cycles_graph(3, 3, labels=("a", "b"), common_node=0)
    regex = PythonRegex("(a|b)(aa)*")
    result = regular_path_querying(graph, regex, {0}, {4})
    assert result == {(State(0), State(4))}
