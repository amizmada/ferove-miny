import random
from constants import ZNAK_MINA, ZNAK_PRAZDNE, SMERY, ZNAK_NEODKRYTE, ZNAK_VLAJKA

def generujPlochu(radky, sloupce, pocet_min):
    # Generuje prázdnou herní plochu a náhodně rozmístí množinu min.

    # inicializujeme prázdnou plochu
    plocha = [[ZNAK_PRAZDNE for _ in range(sloupce)] for _ in range(radky)]
    miny = set()

    # dokud nemáme dost min, náhodně vybíráme políčka
    while len(miny) < pocet_min:
        r = random.randint(0, radky - 1)
        s = random.randint(0, sloupce - 1)
        if (r, s) not in miny:
            miny.add((r, s))
            plocha[r][s] = ZNAK_MINA  # označíme minu na ploše

    return plocha, miny


def prepoctiPlochu(plocha, miny, radky, sloupce):
    # Přepočítá každé políčko podle počtu min v sousedství.
    """
    Pro každou buňku:
      - pokud je v množině min, nechá ZNAK_MINA
      - jinak spočítá miny okolo pomocí SMERY a nastaví číslo nebo ZNAK_PRAZDNE
    """

    for r in range(radky):
        for s in range(sloupce):
            if (r, s) in miny:
                # ponecháme znak miny
                plocha[r][s] = ZNAK_MINA
            else:
                # spočítáme, kolik min je v okolí
                pocet = 0
                for dr, ds in SMERY:
                    nr, ns = r + dr, s + ds
                    if 0 <= nr < radky and 0 <= ns < sloupce and (nr, ns) in miny:
                        pocet += 1
                # číslo nebo prázdné
                plocha[r][s] = str(pocet) if pocet > 0 else ZNAK_PRAZDNE


def odkrytPolicko(plocha, odkryto, r, s):
    # rekurzivně odkrývá políčka
    """
      - pokud je políčko již odkryté, nic nedělá
      - jinak označí odkryto[r][s] = True
      - pokud bylo prázdné (ZNAK_PRAZDNE = 0 sousedů), rekurzivně odkryje sousedy
    """

    # pokud už bylo odkryté, neděláme nic
    if odkryto[r][s]:
        return

    odkryto[r][s] = True  # označíme jako odkryté

    # pokud je v poli ZNAK_PRAZDNE (0 sousedů), rekurzivně odkrýváme okolí
    if plocha[r][s] == ZNAK_PRAZDNE:
        for dr, ds in SMERY:
            nr, ns = r + dr, s + ds
            # kontrolujeme, jestli soused spadá do validního rozsahu
            if 0 <= nr < len(plocha) and 0 <= ns < len(plocha[0]):
                odkrytPolicko(plocha, odkryto, nr, ns)


def vypisPlochu(plocha, odkryto, flags):
    """
    Vytiskne herní pole do konzole v následujícím formátu:
      - první řádek: indexy sloupců
      - vodorovné ohraničení
      - každý řádek: číslo řádku |  buňky:
          - pokud uživatel dá vlajku: ZNAK_VLAJKA
        
          - pokud je odkryto: skutečný obsah plocha[r][s]
          - jinak: ZNAK_NEODKRYTE
      - vodorovné ohraničení
    """
    
    radky = len(plocha)
    sloupce = len(plocha[0])

    # tisk ohraničení sloupců
    print("   " + " ".join(str(i) for i in range(sloupce)))
    print("  " + "-" * (2 * sloupce + 1))

    for r in range(radky):
        row = []
        for s in range(sloupce):
            if flags[r][s]:
                # uživatel zde umístil vlajku
                row.append(ZNAK_VLAJKA)
            elif odkryto[r][s]:
                # políčko je odkryté, ukážeme jeho obsah
                row.append(plocha[r][s])
            else:
                # stále zakryté políčko
                row.append(ZNAK_NEODKRYTE)
        print(f"{r} |" + " ".join(row) + " |")

    # dolní ohraničení
    print("  " + "-" * (2 * sloupce + 1))
