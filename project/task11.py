from typing import Set, Union

from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Variable
from pyformlang.finite_automaton import EpsilonNFA, State
from scipy.sparse import eye, dok_matrix

from project.task1 import get_graph
from project.task2 import create_nfa_for_graph
from project.task3 import BoolDecomposition
from project.task7_ecfg import ecfg_from_cfg
from project.task7_rsm import rsm_from_ecfg, minimize_rsm


def cfpq_tensor(
    graph: Union[MultiDiGraph, str],
    cfg: Union[CFG, str],
    start_states: Set = None,
    final_states: Set = None,
    start_symbol: Variable = Variable("S"),
):
    """Performs a context-free path querying in a graph by a context-free grammar using tensor product.

    Parameters
    ----------
    graph: MultiDiGraph | str
    cfg: CFG | str
    start_states: Set[int]
    final_states: Set[int]
    start_symbol: Variable

    Returns
    -------
    result: Set[Tuple]
        A set of pairs of nodes solving the reachability problem and corresponding to the
        conditions (starting and final nodes, starting symbol).
    """
    if isinstance(graph, str):
        graph = get_graph(graph)
    if isinstance(cfg, str):
        cfg = CFG.from_text(cfg)
    if start_states is None:
        start_states = graph.nodes
    if final_states is None:
        final_states = graph.nodes
    return {
        (i, j)
        for (i, var, j) in tensor(graph, cfg)
        if i in start_states and j in final_states and var == start_symbol
    }


def tensor(graph: MultiDiGraph, cfg: CFG):
    """Function based on the Tensor algorithm that solves the reachability problem between all pairs of nodes
             for a given graph and a given context-free grammar.

    Parameters
    ----------
    graph: MultiDiGraph
    cfg: CFG

    Returns
    -------
    result: Set[Tuple]
        A set of pairs of nodes solving the reachability problem between all pairs of nodes.
    """
    rsm = rsm_from_ecfg(ecfg_from_cfg(cfg))
    to_bd_rsm = minimize_rsm(rsm)
    rsm_to_nfa = EpsilonNFA()
    for var, a in to_bd_rsm.boxes.items():
        for st in a.start_states:
            rsm_to_nfa.add_start_state(State((var, st)))
        for st in a.final_states:
            rsm_to_nfa.add_final_state(State((var, st)))
        for (start, label, final) in a:
            rsm_to_nfa.add_transition(State((var, start)), label, State((var, final)))
    rsm_decomposed = BoolDecomposition(rsm_to_nfa)
    graph_decomposed = BoolDecomposition(create_nfa_for_graph(graph))
    diag = eye(graph_decomposed.all_states, dtype=bool).todok()
    for var in cfg.get_nullable_symbols():
        if var.value in graph_decomposed.bool_matrix.keys():
            graph_decomposed.bool_matrix[var] += diag
        else:
            graph_decomposed.bool_matrix[var] = diag
    prev_trans_clos_nnz = -1
    cur_trans_clos_nnz = 0
    while prev_trans_clos_nnz != cur_trans_clos_nnz:
        intersected = rsm_decomposed.intersect_automata(graph_decomposed)
        transitive_closure = intersected.get_transitive_closure()
        prev_trans_clos_nnz = cur_trans_clos_nnz
        cur_trans_clos_nnz = transitive_closure.nnz
        for (i, j) in list(zip(*transitive_closure.nonzero())):
            rsm_i = i // graph_decomposed.all_states
            rsm_j = j // graph_decomposed.all_states
            graph_i = i % graph_decomposed.all_states
            graph_j = j % graph_decomposed.all_states
            start_rsm_state = rsm_decomposed.index_to_state[rsm_i]
            final_rsm_state = rsm_decomposed.index_to_state[rsm_j]
            (var, _) = start_rsm_state.value
            if (
                start_rsm_state in rsm_decomposed.start_states
                and final_rsm_state in rsm_decomposed.final_states
            ):
                if var not in graph_decomposed.bool_matrix.keys():
                    graph_decomposed.bool_matrix[var] = dok_matrix(
                        (graph_decomposed.all_states, graph_decomposed.all_states),
                        dtype=bool,
                    )
                graph_decomposed.bool_matrix[var][graph_i, graph_j] = True
    res = set()
    for (var, mtx) in graph_decomposed.bool_matrix.items():
        for (i, j) in zip(*mtx.nonzero()):
            res.add(
                (
                    graph_decomposed.index_to_state[i],
                    var,
                    graph_decomposed.index_to_state[j],
                )
            )
    return res
