import filecmp
import os

import pytest

from project.gql.task14 import *


@pytest.mark.parametrize(
    "inp, res",
    [
        ("x = 5; /*comment*/", True),
        ("/*comment*/ x = 5;", True),
        ("x /*comment*/ = 5;", True),
        ("x = 5 ; /*comment", False),
        ("x = 5; //comment", False),
        ("x = 5; /*комментарий*/", True),
    ],
)
def test_comment(inp, res):
    assert accept(inp) == res


@pytest.mark.parametrize(
    "inp, res",
    [
        ("(expr)*", True),
        ("(union (expr1, expr2))*", True),
        ("(expr1, expr2)*", False),
        ("()*", False),
    ],
)
def test_star(inp, res):
    assert accept("x = " + inp + ";") == res


@pytest.mark.parametrize(
    "inp, res",
    [
        ("union (expr1, expr2)", True),
        ('union (union ("a", 1), "A")', True),
        ("union (expr)", False),
        ("union (expr1, expr2, expr3)", False),
    ],
)
def test_union(inp, res):
    assert accept("x = " + inp + ";") == res


@pytest.mark.parametrize(
    "inp, res",
    [
        ("concat (expr1, expr2)", True),
        ('concat (concat ("a", 1), "A")', True),
        ("concat (expr)", False),
        ("concat (expr1, expr2, expr3)", False),
    ],
)
def test_concat(inp, res):
    assert accept("x = " + inp + ";") == res


@pytest.mark.parametrize(
    "inp, res",
    [
        ("intersect (expr1, expr2)", True),
        ('intersect (intersect ("a", 1), "A")', True),
        ("intersect (expr)", False),
        ("intersect (expr1, expr2, expr3)", False),
    ],
)
def test_intersect(inp, res):
    assert accept("x = " + inp + ";") == res


@pytest.mark.parametrize(
    "inp, res",
    [
        ("filter (fun (var) {1}, expr)", True),
        ("filter (fun () {}, expr )", False),
        ("filter (fun (var) {1})", False),
        ("filter (fun (var) {1}, expr1, expr2", False),
    ],
)
def test_filter(inp, res):
    assert accept("x = " + inp + ";") == res


@pytest.mark.parametrize(
    "inp, res",
    [
        ("map (fun (var) {1}, expr)", True),
        ("map (fun () {}, expr )", False),
        ("map (fun (var) {1})", False),
    ],
)
def test_map(inp, res):
    assert accept("x = " + inp + ";") == res


@pytest.mark.parametrize(
    "inp, res",
    [
        ("get_edges (var)", True),
        ("get_edges (.not_var)", False),
        ("get_edges var", False),
        ("get_edges (var", False),
        ('{(0, "label1", 1), (1, "label2", 2)}', True),
        ("{(111)}", False),
        ("set()", True),
    ],
)
def test_edges(inp, res):
    assert accept("x = " + inp + ";") == res


@pytest.mark.parametrize(
    "inp, res",
    [
        ("get_labels (var)", True),
        ("get_labels (.not_var)", False),
        ("get_labels var", False),
        ("get_labels (var", False),
        ('{"label1", "label2"}', True),
        ("{lab1}", True),
        ("{true}", False),
        ("set()", True),
    ],
)
def test_labels(inp, res):
    assert accept("x = " + inp + ";") == res


@pytest.mark.parametrize(
    "inp, res",
    [
        ("get_start (var)", True),
        ("get_start (.not_var)", False),
        ("get_start var", False),
        ("get_start (var", False),
        ("get_final (graph)", True),
        ("get_reachable (graph)", True),
        ("get_vertices (graph)", True),
        ('{(0, "label", 1)}', True),
        ('{(0, "label", "ss")}', False),
        ("set()", True),
    ],
)
def test_vertices(inp, res):
    assert accept("x = " + inp + ";") == res


@pytest.mark.parametrize(
    "inp, res",
    [
        ("0", True),
        ("1234567890", True),
        ("(1)", True),
        ("-1", True),
        ('"string"', True),
        ("true", True),
        ("(l", False),
        ("truer", False),
        ("0111", False),
    ],
)
def test_value(inp, res):
    assert accept("x = " + inp + ";") == res


@pytest.mark.parametrize(
    "inp, res",
    [
        ("i_am_variable", True),
        ("_me_too", True),
        ("iAmVariable1234", True),
        ("p/a/t/h.dot", True),
        ("111", False),
        ("/ccc", False),
    ],
)
def test_variable(inp, res):
    assert accept(inp + "= 1; ") == res


@pytest.mark.parametrize(
    "inp, res",
    [
        ("print expr;", True),
        ("print (expr);", True),
        ("print expr", False),
        ("print .not_expr;", False),
    ],
)
def test_print(inp, res):
    assert accept(inp) == res


@pytest.mark.parametrize(
    "inp, res",
    [
        (
            """
        graph = load_graph("p/a/t/h");
        vertices = get_final(graph);
        graph_upd = set_start(get_vertices(graph), graph);
        print vertices;
        print get_labels(graph_upd);
        """,
            True,
        ),
        (
            """
        graph = load_graph("p/a/t/h/2");
        edges = get_edges(graph);
        graph_upd = set_final(get_start(graph), graph);
        print get_final(graph_upd);
        print edges;
        """,
            True,
        ),
        (
            """
        a = union ("A", "a");
        b_a = (union ("b", a))*;
        print concat (a, b_a);
        """,
            True,
        ),
    ],
)
def test_prog(inp, res):
    assert accept(inp) == res


# def test1_write_dot():
#     text = """a = 5;"""
#     save_as_dot(text, "tests/res/temp1_task14.dot")
#     assert filecmp.cmp(
#         "tests/res/temp1_task14.dot", "tests/res/expected1_task14.dot", shallow=False
#     )
#     os.remove("tests/res/temp1_task14.dot")
#
#
# def test2_write_dot():
#     text = """
#         a = union ("A", "a");
#         b_a = (union ("b", a))*;
#         print concat (a, b_a);
#         """
#     save_as_dot(text, "tests/res/temp2_task14.dot")
#     assert filecmp.cmp(
#         "tests/res/temp2_task14.dot", "tests/res/expected2_task14.dot", shallow=False
#     )
#     os.remove("tests/res/temp2_task14.dot")
