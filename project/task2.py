from pyformlang.regular_expression import *
from pyformlang.finite_automaton import *
import networkx as nx
from typing import Set

__all__ = ["create_minimal_dfa_for_regex", "create_nfa_for_graph"]


def create_minimal_dfa_for_regex(regex: Regex) -> DeterministicFiniteAutomaton:
    """Create a minimal DFA for a given regular expression.

    Parameters
    ----------
    regex : Regex
        The specified regular expression.

    Returns
    -------
    dfa : DeterministicFiniteAutomaton
        The minimal deterministic finite automaton.
    """
    return regex.to_epsilon_nfa().to_deterministic().minimize()


def create_nfa_for_graph(
    graph: nx.MultiDiGraph, start_states: Set[int] = None, final_states: Set[int] = None
) -> NondeterministicFiniteAutomaton:
    """Create a NFA for a given graph.

    Parameters
    ----------
    graph : MultiDiGraph
        The graph by which the NFA is created.
    start_states : Set[int]
        Set of starting states.
    final_states : Set[int]
        Set of final states.

    Returns
    -------
    nfa : NondeterministicFiniteAutomaton
        The created nondeterministic finite automaton.
    """
    all_states = graph.nodes
    if start_states is None:
        start_states = all_states
    if final_states is None:
        final_states = all_states
    nfa = NondeterministicFiniteAutomaton(states=all_states)
    for st in start_states:
        nfa.add_start_state(State(st))
    for st in final_states:
        nfa.add_final_state(State(st))

    for (fr, to, label) in graph.edges(data="label"):
        nfa.add_transition(State(fr), Symbol(label), State(to))
    return nfa
