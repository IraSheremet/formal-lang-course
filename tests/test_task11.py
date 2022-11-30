from networkx import MultiDiGraph
from pyformlang.cfg import CFG

from project.task11 import cfpq_tensor
from project.task7_rsm import *


def test_cfpq_tensor():
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
    expected_cfpq = {(1, 2), (0, 3), (2, 3), (0, 2), (2, 2), (1, 3)}
    assert cfpq_tensor(graph, cfg, start_symbol=Variable("S")) == expected_cfpq
