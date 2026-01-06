from board import generujPlochu, prepoctiPlochu, vypisPlochu
from constants import POCET_RADKU, POCET_SLOUPCU, POCET_MIN, ZNAK_VLAJKA
from solver import jePolickoSafe
from fair_rules import vyhodnotTah


def validniSouradnice(r, s, radky, sloupce):
    return 0 <= r < radky and 0 <= s < sloupce

def vyhra(odkryto, miny):
    radky, sloupce = len(odkryto), len(odkryto[0])
    for r in range(radky):
        for s in range(sloupce):
            if (r, s) not in miny and not odkryto[r][s]:
                return False
    return True

def hra():
    R, S, M = POCET_RADKU, POCET_SLOUPCU, POCET_MIN
    plocha, miny = generujPlochu(R, S, M)
    prepoctiPlochu(plocha, miny, R, S)
    odkryto = [[False] * S for _ in range(R)]
    flags = [[False] * S for _ in range(R)]

    while True:
        interniVlajky = [[False] * S for _ in range(R)]
        bezpecnaPole, skryteVlajky = jePolickoSafe(odkryto, plocha, interniVlajky)
        vypisPlochu(plocha, odkryto, flags)
        if vyhra(odkryto, miny):
            print("Gratuluji, vyhrál jsi!")
            break
        vstup = input("Zadej 'řádek sloupec' nebo 'řádek sloupec F': ").split()
        if len(vstup) not in (2, 3):
            print("Neplatný vstup.")
            continue
        try:
            r, s = map(int, vstup[:2])
        except ValueError:
            print("Neplatné souřadnice.")
            continue
        if not validniSouradnice(r, s, R, S):
            print("Souřadnice mimo rozsah.")
            continue
        if len(vstup) == 3 and vstup[2].upper() == 'F':
            flags[r][s] = not flags[r][s]
            continue
        # ODHALENÍ POLÍČKA 
        status, plocha, miny, odkryto = vyhodnotTah(plocha, miny, odkryto, flags, bezpecnaPole, skryteVlajky, r, s)

        if status != "OK":
            if status == "PROHRA":
                # určujeme důvod prohry
                if (r, s) in skryteVlajky:
                    duvod = "MINA! Prohrál jsi."
                elif bezpecnaPole and (r, s) not in bezpecnaPole:
                    duvod = "Ignoroval jsi bezpečné políčko! Prohrál jsi."
                else:
                    duvod = "MINA! Prohrál jsi."

                vypisPlochu(plocha, odkryto, flags)
                print(duvod)
                break
            else:  # status == "ODEBRANA_MINA"
                print("Mina odstraněna, pokračuj.")
        vypisPlochu(plocha, odkryto, flags)
        if status == "PROHRA":
            print("PROHRA!")
            break
