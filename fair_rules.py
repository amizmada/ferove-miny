from board import prepoctiPlochu, odkrytPolicko
from constants import ZNAK_MINA

def vyhodnotTah(plocha, miny, odkryto, flags, bezpecnaPole, skryteVlajky, r, s):
    """Vyhodnotí uživatelský klik podle férových pravidel."""
    if (r, s) in skryteVlajky:
        for mr, ms in miny:        # odkryjeme VŠECHNY miny
            odkryto[mr][ms] = True
        return "PROHRA", plocha, miny, odkryto
    if bezpecnaPole and (r, s) not in bezpecnaPole:
        miny.add((r, s))
        plocha[r][s] = ZNAK_MINA
        prepoctiPlochu(plocha, miny, len(plocha), len(plocha[0]))
        return "PROHRA", plocha, miny, odkryto
    if not bezpecnaPole and not skryteVlajky and (r, s) in miny:
        # férově odstraníme minu a políčko okamžitě odkryjeme
        miny.remove((r, s))
        prepoctiPlochu(plocha, miny, len(plocha), len(plocha[0]))
        odkrytPolicko(plocha, odkryto, r, s)
        return "ODEBRANA_MINA", plocha, miny, odkryto
    if (r, s) in miny:
        return "PROHRA", plocha, miny, odkryto
    odkrytPolicko(plocha, odkryto, r, s)
    return "OK", plocha, miny, odkryto