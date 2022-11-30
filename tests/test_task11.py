from networkx import MultiDiGraph
from pyformlang.cfg import CFG

from project.task11 import cfpq_tensor, tensor
from project.task7_rsm import *
from tests.test_task9 import check_cfpq


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
    check_cfpq(
        algo_res=tensor(graph, cfg),
        cfpq_res=cfpq_tensor(graph, cfg, start_symbol=Variable("S")),
    )
