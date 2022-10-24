from pyformlang.cfg import CFG


def to_weak_chomsky_normal_form(cfg: CFG) -> CFG:
    """Convert context-free grammar to the weak Chomsky normal form.

    Parameters
    ----------
    cfg: CFG
        The context-free grammar for conversion.

    Returns
    -------
    new_cfg: CFG
        The equivalent context-free grammar in the weak Chomsky normal form.
    """
    new_cfg = (
        cfg.remove_useless_symbols()
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )
    new_productions = new_cfg._get_productions_with_only_single_terminals()
    new_productions = new_cfg._decompose_productions(new_productions)
    return CFG(start_symbol=new_cfg.start_symbol, productions=set(new_productions))


def cfg_from_file(file) -> CFG:
    """Read context-free grammar from a file.

    Parameters
    ----------
    file: str | bytes | PathLike[str] | PathLike[bytes] | int
        The file(name) to be read from.

    Returns
    -------
    cfg: CFG
        The context-free grammar.
    """
    with open(file) as f:
        cfg = CFG.from_text(f.read())
    return cfg
