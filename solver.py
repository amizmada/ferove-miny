from constants import ZNAK_MINA, ZNAK_PRAZDNE, SMERY


def jePodmonozina(a, b):
    """
    Kontroluje, zda je seznam "a" podmnožinou seznamu "b".
    Vrací True, pokud každý prvek z "a" se nachází v "b".
    Používá se v podmnožinové dedukci.
    """

    return all(x in b for x in a)


def jePolickoSafe(odkryto, plocha, interniVlajky):
    """
    Provede dedukci a vrátí:
      - safe: seznam políček, kde je 100% jistota, že tam není mina
      - vynuceneMiny: seznam políček, kde musí být mina podle logiky

    Implementovaná pravidla:
      1) Pravidlo n == 0: pokud odkryté políčko obsahuje 0 (ZNAK_PRAZDNE),
         jeho všichni sousedé, kteří jsou stále zakrytí, jsou safe.
      2) Úplné pokrytí: pokud kolem políčka s číslem n leží
         přesně n zakrytých sousedů (bez vlajek), pak jsou všichni ti
         zakrytí sousedé vynuceneMiny (jsou to miny).
      3) Podmnožinová dedukce:
         - vezme dve omezeni (zakrytaPole1, zbyvajiciMiny1) a (zakrytaPole2, zbyvajiciMiny2),
         - pokud zakrytaPole1 je podmnožinou zakrytaPole2 a zbyvajiciMiny2 - zbyvajiciMiny1 == 0 ->
           rozdíl zakrytaPole2\zakrytaPole1 jsou safe,
         - pokud zakrytaPole1 je podmnožunou zakrytaPole2 a zbyvajiciMiny2 - zbyvajiciMiny1 == len(zakrytaPole2) - len(zakrytaPole1) ->
           zakrytaPole2\zakrytaPole1 jsou vynuceneMiny.
    """

    radky   = len(plocha)
    sloupce = len(plocha[0])
    omezeni = []    # seznam páru (zakryto, need) pro každé odkryté číslo
    safe    = set()    # množina bezpečných políček
    vynuceneMiny  = set()    # množina vynucených min

    # 1) Vytvoříme omezení
    for r in range(radky):
        for s in range(sloupce):
            # bereme pouze odkrytá políčka s číslem
            if odkryto[r][s] and plocha[r][s] not in (ZNAK_PRAZDNE, ZNAK_MINA):
                try:
                    n = int(plocha[r][s])  # cílová hodnota min kolem
                except ValueError:
                    continue  # není číslo

                zakryto = []    # zakrytá políčka bez vlajky
                pocetInternichVlajek = 0  # počet interních interniVlajky

                for dr, ds in SMERY:
                    nr, ns = r + dr, s + ds
                    if 0 <= nr < radky and 0 <= ns < sloupce and not odkryto[nr][ns]:
                        if interniVlajky[nr][ns]:
                            pocetInternichVlajek += 1  # soused už označen jako vlajka
                        else:
                            zakryto.append((nr, ns))

                # pravidlo 1: n == 0 -> všichni zakryto sousedé jsou safe
                if n == 0:
                    safe.update(zakryto)

                # pravidlo 2: pocetInternichVlajek + len(zakryto) == n -> všechny zakryto jsou vynuceneMiny
                if pocetInternichVlajek + len(zakryto) == n:
                    vynuceneMiny.update(zakryto)

                # uložíme omezení s upravenou potřebou (n - pocetInternichVlajek)
                omezeni.append((zakryto, n - pocetInternichVlajek))

    # 2) Podmnožinová dedukce
    zmena = True
    while zmena:
        zmena = False
        new_safe = set()
        new_vynuceneMiny = set()

        # porovnáme každý pár omezení
        for i in range(len(omezeni)):
            zakrytaPole1, zbyvajiciMiny1 = omezeni[i]
            for j in range(len(omezeni)):
                if i == j:
                    continue
                zakrytaPole2, zbyvajiciMiny2 = omezeni[j]

                # zakrytaPole1 je podmnožinou zakrytaPole2 a zbyvajiciMiny2 == zbyvajiciMiny1 -> rozdíl je safe
                if jePodmonozina(zakrytaPole1, zakrytaPole2) and zbyvajiciMiny2 == zbyvajiciMiny1:
                    rozdil = set(zakrytaPole2) - set(zakrytaPole1)
                    new_safe.update(rozdil)

                # zakrytaPole1 je podmnožunou zakrytaPole2 a zbyvajiciMiny2-zbyvajiciMiny1 == |zakrytaPole2|-|zakrytaPole1| -> rozdíl je vynuceneMiny
                if jePodmonozina(zakrytaPole1, zakrytaPole2) and (zbyvajiciMiny2 - zbyvajiciMiny1) == len(zakrytaPole2) - len(zakrytaPole1):
                    rozdil = set(zakrytaPole2) - set(zakrytaPole1)
                    new_vynuceneMiny.update(rozdil)

        # pokud jsme našli nová safe/vynuceneMiny, aktualizujeme hlavní množiny a constrainty
        if new_safe or new_vynuceneMiny:
            # přidáme k výsledkům
            safe.update(new_safe)
            vynuceneMiny.update(new_vynuceneMiny)

            # odstraníme je z omezeni, aby nedocházelo k nekonečné smyčce
            updated = []
            for cover, need in omezeni:
                filtered = [c for c in cover if c not in new_safe and c not in new_vynuceneMiny]
                updated.append((filtered, need))
            omezeni = updated

            zmena = True  # zopakujeme dedukci, dokud vznikají změny

    # vrátíme výsledky jako listy
    return list(safe), list(vynuceneMiny)
