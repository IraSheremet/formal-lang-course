from typing import Dict, AbstractSet

from pyformlang.cfg import Variable, CFG
from pyformlang.regular_expression import Regex


class ECFG:
    """Class for representing Extended Context-Free Grammar."""

    def __init__(
        self,
        variables: AbstractSet[Variable],
        productions: Dict[Variable, Regex],
        start: Variable = Variable("S"),
    ):
        self.variables = variables
        self.start = start
        self.productions = productions


def ecfg_from_cfg(cfg: CFG):
    """Create a extended context-free grammar from the context-free grammar.

    Parameters
    ----------
    cfg: CFG
        Context-Free Grammar.

    Returns
    -------
    ecfg: ECFG
        The equivalent extended context-free grammar.
    """
    productions = {}
    for prod in cfg.productions:
        regex = Regex(
            " ".join([x.to_text() for x in prod.body] if len(prod.body) > 0 else "$")
        )
        productions[prod.head] = (
            productions[prod.head].union(regex) if prod.head in productions else regex
        )
    return ECFG(
        variables=cfg.variables, start=cfg.start_symbol, productions=productions
    )


def ecfg_from_text(text: str):
    """Read extended context-free grammar from a text.

    Parameters
    ----------
    text: str
        The text in which the extended context-free grammar is written.

    Returns
    -------
    ecfg: ECFG
        The extended context-free grammar.
    """
    variables = set()
    productions = {}
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        head_s, body_s = line.split("->")
        head = Variable(head_s.strip())
        variables.add(head)
        productions[head] = Regex(body_s)
    return ECFG(variables=variables, productions=productions)


def ecfg_from_file(file):
    """Read extended context-free grammar from a file.

    Parameters
    ----------
    file: str | bytes | PathLike[str] | PathLike[bytes] | int
        The file(name) to be read from.

    Returns
    -------
    ecfg: ECFG
        The extended context-free grammar.
    """
    with open(file) as f:
        ecfg = ecfg_from_text(f.read())
    return ecfg
