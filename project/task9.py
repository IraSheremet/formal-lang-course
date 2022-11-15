from typing import Set, Union

from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Variable

from project.task1 import get_graph
from project.task6 import to_weak_chomsky_normal_form


def cfpq(
    graph: Union[MultiDiGraph, str],
    cfg: Union[CFG, str],
    start_states: Set = None,
    final_states: Set = None,
    start_symbol: Variable = Variable("S"),
):
    """Performs a context-free path querying in a graph by a context-free grammar.

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
        for (i, var, j) in hellings(graph, cfg)
        if i in start_states and j in final_states and var == start_symbol
    }


def hellings(graph: MultiDiGraph, cfg: CFG):
    """Function based on the Hellings algorithm that solves the reachability problem between all pairs of nodes
    for a given graph and a given context-free grammar.

           Parameters
           ----------
           graph: MultiDiGraph
           cfg: CFG

           Returns
           -------
           result: List[Tuple]
               A list of pairs of nodes solving the reachability problem between all pairs of nodes.
    """
    cfg = to_weak_chomsky_normal_form(cfg)
    term_productions, non_term_productions, eps_productions = set(), set(), set()
    for prod in cfg.productions:
        if len(prod.body) == 1:
            term_productions.add(prod)
        elif len(prod.body) == 2:
            non_term_productions.add(prod)
        else:
            eps_productions.add(prod)
    r = []
    for (u, v, label) in graph.edges(data="label"):
        for prod in term_productions:
            if label == prod.body[0].value:
                r.append((u, prod.head, v))
    for n in graph.nodes:
        for prod in eps_productions:
            r.append((n, prod.head, n))
    m = r.copy()
    while m:
        (v, N, u) = m.pop(0)
        for (x, M, y) in r:
            if y == v:
                for prod in non_term_productions:
                    new_triple = (x, prod.head, u)
                    if prod.body[0] == M and prod.body[1] == N and new_triple not in r:
                        m.append(new_triple)
                        r.append(new_triple)
        for (x, M, y) in r:
            if x == u:
                for prod in non_term_productions:
                    new_triple = (v, prod.head, y)
                    if prod.body[0] == N and prod.body[1] == M and new_triple not in r:
                        m.append(new_triple)
                        r.append(new_triple)
    return r
