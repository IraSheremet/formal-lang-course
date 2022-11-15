from pyformlang.cfg import CFG


def cyk(w: str, cfg: CFG):
    """Check whether a word belongs to a context-free grammar.
    Parameters
    ----------
    w: str
        Given word.
    cfg: CFG
        Given context-free grammar.

    Returns
    -------
    res: bool
        the result is whether the word belongs to this context-free grammar.
    """
    n = len(w)
    if n == 0:
        return cfg.generate_epsilon()
    normal_form_cfg = cfg.to_normal_form()
    term_productions, non_term_productions = [], []
    for prod in normal_form_cfg.productions:
        if len(prod.body) == 1:
            term_productions.append(prod)
        if len(prod.body) == 2:
            non_term_productions.append(prod)
    mtx = [[set() for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for prod in term_productions:
            if w[i] == prod.body[0].value:
                mtx[i][i].update({prod.head.value})
    for s in range(1, n):
        for i in range(n - s):
            j = i + s
            for k in range(i, j):
                for prod in non_term_productions:
                    if (
                        prod.body[0].value in mtx[i][k]
                        and prod.body[1].value in mtx[k + 1][j]
                    ):
                        mtx[i][j].update({prod.head.value})
    return normal_form_cfg.start_symbol.value in mtx[0][n - 1]
