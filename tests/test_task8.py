from project.task6 import cfg_from_file
from project.task8 import cyk


def test1_cyk():
    cfg = cfg_from_file("tests/res/cfg1_task6")
    assert all([cyk(w=w, cfg=cfg) for w in ["", "b", "bb", "bbbbbbbbbbbbbbbbbbbbb"]])
    assert not all([cyk(w=w, cfg=cfg) for w in ["a", "ba", "b "]])


def test2_cyk():
    cfg = cfg_from_file("tests/res/cfg2_task6")
    assert all([cyk(w=w, cfg=cfg) for w in ["", "ab", "aabb", "abab", "aaaabbabbabb"]])
    assert not all([cyk(w=w, cfg=cfg) for w in ["a", "ba", "b", "abba", "aaabb"]])
