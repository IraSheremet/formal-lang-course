import cfpq_data

from project.task4 import *


def test_empty_rpq():
    graph = cfpq_data.labeled_two_cycles_graph(3, 3, labels=("a", "b"))
    regex = PythonRegex("(c|d)*")
    res = rpq(graph, regex)
    res_for_each_node = rpq(graph, regex, is_for_each_node=True)
    assert res == set()
    assert res_for_each_node == set()


def test_full_rpq():
    graph = cfpq_data.labeled_two_cycles_graph(3, 3, labels=("a", "b"))
    regex = PythonRegex("(a|b)*")
    res = rpq(graph, regex)
    assert res == {0, 1, 2, 3, 4, 5, 6}


def test_rpq():
    graph = cfpq_data.labeled_two_cycles_graph(3, 3, labels=("a", "b"), common_node=0)
    regex = PythonRegex("(a|b)(aa)*")
    result = rpq(graph, regex, {0})
    assert result == {1, 3, 4}


def test_rpq_for_each_node():
    graph = cfpq_data.labeled_two_cycles_graph(3, 3, labels=("a", "b"), common_node=0)
    regex = PythonRegex("aa")
    result = rpq(graph, regex, is_for_each_node=True)
    assert result == {(0, 2), (2, 0), (1, 3), (3, 1)}
