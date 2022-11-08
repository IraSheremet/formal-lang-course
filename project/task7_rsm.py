from typing import Dict

from pyformlang.cfg import Variable
from pyformlang.finite_automaton import EpsilonNFA

from project.task7_ecfg import ECFG


class RSM:
    """Class for representing Recursive State Machine."""

    def __init__(self, start: Variable, boxes: Dict[Variable, EpsilonNFA]):
        self.start = start
        self.boxes = boxes


def rsm_from_ecfg(ecfg: ECFG):
    """Create a RSM from the Extended Context-Free Grammar.

    Parameters
    ----------
    ecfg: ECFG
        Extended Context-Free Grammar.

    Returns
    -------
    rsm: RSM
        The equivalent recursive state machine.
    """
    boxes = {}
    for k, v in ecfg.productions.items():
        boxes[k] = v.to_epsilon_nfa()
    return RSM(start=ecfg.start, boxes=boxes)


def minimize_rsm(rsm: RSM):
    """Minimize the current Recursive State Machine.

    Parameters
    ----------
    rsm: RSM
        Recursive State Machine.

    Returns
    -------
    rsm: RSM
        The minimal RSM.
    """
    res = RSM(start=rsm.start, boxes={})
    for v, nfa in rsm.boxes.items():
        res.boxes[v] = nfa.minimize()
    return res
