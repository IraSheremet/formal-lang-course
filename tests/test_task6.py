from pyformlang.cfg import Variable, Terminal

from project.task6 import *


def test_empty_cfg_from_file():
    cfg = cfg_from_file("tests/res/empty_cfg_task6")
    assert cfg.is_empty()


def test_empty_cfg_in_wcnf():
    cfg = cfg_from_file("tests/res/empty_cfg_task6")
    assert to_weak_chomsky_normal_form(cfg).is_empty()


def is_wcnf(production):
    if len(production.body) == 2:
        return isinstance(production.body[0], Variable) and isinstance(
            production.body[1], Variable
        )
    elif len(production.body) == 1:
        return isinstance(production.body[0], Terminal)
    elif len(production.body) == 0:
        # for eps
        return True
    else:
        return False


def test_cfg1():
    cfg = cfg_from_file("tests/res/cfg1_task6")
    weak_cfg = to_weak_chomsky_normal_form(cfg)
    words = ["", "b", "bb", "bbbbbbbbbbbbbbbbbbbbb"]
    for word in words:
        assert cfg.contains(word)
        assert weak_cfg.contains(word)
    not_words = ["a", "ba", "b "]
    for word in not_words:
        assert not cfg.contains(word)
        assert not weak_cfg.contains(word)
    assert all([is_wcnf(production) for production in weak_cfg.productions])


def test_cfg2():
    cfg = cfg_from_file("tests/res/cfg2_task6")
    weak_cfg = to_weak_chomsky_normal_form(cfg)
    words = ["", "ab", "aabb", "abab", "aaaabbabbabb"]
    for word in words:
        assert cfg.contains(word)
        assert weak_cfg.contains(word)
    not_words = ["a", "ba", "b", "abba", "aaabb"]
    for word in not_words:
        assert not cfg.contains(word)
        assert not weak_cfg.contains(word)
    assert all([is_wcnf(production) for production in weak_cfg.productions])
