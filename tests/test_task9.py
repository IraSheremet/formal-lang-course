from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Variable

from project.task9 import cfpq, hellings


def test_cfpq_example():
    text = """
        S -> A B
        S -> A Q
        Q -> S B
        A -> a
        B -> b
        """
    cfg = CFG.from_text(text)
    graph = MultiDiGraph()
    graph.add_nodes_from(range(0, 3))
    graph.add_edges_from(
        [
            (0, 1, {"label": "a"}),
            (1, 2, {"label": "a"}),
            (2, 0, {"label": "a"}),
            (2, 3, {"label": "b"}),
            (3, 2, {"label": "b"}),
        ]
    )
    expected_hellings = [
        (Variable("A"), 0, 1),
        (Variable("A"), 1, 2),
        (Variable("A"), 2, 0),
        (Variable("B"), 2, 3),
        (Variable("B"), 3, 2),
        (Variable("S"), 1, 3),
        (Variable("Q"), 1, 2),
        (Variable("S"), 0, 2),
        (Variable("Q"), 0, 3),
        (Variable("S"), 2, 3),
        (Variable("Q"), 2, 2),
        (Variable("S"), 1, 2),
        (Variable("Q"), 1, 3),
        (Variable("S"), 0, 3),
        (Variable("Q"), 0, 2),
        (Variable("S"), 2, 2),
        (Variable("Q"), 2, 3),
    ]
    expected_cfpq = {(1, 2), (0, 3), (2, 3), (0, 2), (2, 2), (1, 3)}
    assert hellings(graph, cfg) == expected_hellings
    assert cfpq(graph, cfg, start_symbol=Variable("S")) == expected_cfpq
