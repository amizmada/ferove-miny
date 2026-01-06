# FÉROVÉ MINY (Fair Minesweeper)

[cite_start]**Autor:** Adam Zima [cite: 3, 26]
[cite_start]**Předmět:** Programování 1 (NPRG030) [cite: 4, 27]

## 📖 Úvod
[cite_start]Tento projekt je implementací klasické hry Minesweeper v konzolovém prostředí, která je však obohacena o „férovou“ dedukční logiku[cite: 6].

### Co znamená „Férová logika“?
Hra zajišťuje, že každé automatické odhalení nebo označení miny probíhá spravedlivě:
1.  **Bezpečný začátek:** Začínáte bez jakýchkoli informací. [cite_start]Pokud v dané situaci není možné logicky a jednoznačně najít bezpečné políčko (např. na začátku hry), hra garantuje, že po odkrytí libovolného políčka na něm mina nebude[cite: 10, 29].
2.  [cite_start]**Trest za chybu:** Pokud existuje políčko, které je jistě bez miny (lze to dedukovat), a vy přesto riskujete a odhalíte políčko, u kterého tuto jistotu nemáte, mina na něm bude[cite: 11, 30].
3.  [cite_start]**Řešitelnost:** Tento přístup garantuje, že každý tah je buď čistě logický, nebo (v nutných případech) jde o hádání, které neskončí prohrou[cite: 36].

---

## 🎮 Uživatelská dokumentace

### Cíl hry
Cílem je odkrýt všechna políčka, která neobsahují miny. [cite_start]Je nutné se vyhnout minám náhodně rozmístěným po ploše[cite: 8].

### Ovládání
[cite_start]Hra se ovládá zadáváním textových příkazů do konzole[cite: 13].

* **Odkrytí políčka:**
    [cite_start]Zadejte souřadnice ve formátu `Řádek Sloupec` (např. `2 3`)[cite: 15].
* **Vlajka (označení miny):**
    [cite_start]Zadejte souřadnice následované písmenem F: `Řádek Sloupec F` (např. `1 4 F`)[cite: 15]. [cite_start]Příkaz slouží k přidání i odstranění vlajky[cite: 15].

### Symboly na herní ploše
* [cite_start]`-` (pomlčka): Zakryté políčko[cite: 17].
* [cite_start]`1`–`8`: Počet min v okolních 8 políčkách[cite: 17].
* [cite_start]` ` (mezera): Představuje 0, tedy políčko bez sousedních min (automaticky odkryje své okolí)[cite: 17, 18].
* [cite_start]`*` (hvězdička): Zobrazuje minu (objeví se při prohře nebo při férovém odstranění)[cite: 18].
* [cite_start]`F`: Vlajka uživatele pro označení miny[cite: 18].

### Konec hry
[cite_start]Hra může skončit třemi způsoby[cite: 20]:
1.  [cite_start]**PROHRA:** Hráč odkryje políčko, kde je mina[cite: 21].
2.  [cite_start]**PROHRA:** Hráč odkryje neznámé políčko v situaci, kdy mohl mít jistotu o jiném bezpečném poli[cite: 22].
3.  [cite_start]**VÝHRA:** Hráč úspěšně odkryje všechna neminová políčka[cite: 23].

---

## 🛠 Programátorská dokumentace

### Popis algoritmu
[cite_start]Program udržuje stav hry v matici, která obsahuje souřadnice min, množinu odhalených polí (`odkryto`) a vlajky (`flags`)[cite: 32].

#### Dedukční modul
[cite_start]Při každém tahu algoritmus na základě sousedních čísel generuje dvě množiny[cite: 33]:
* **safe:** Políčka, jejichž bezpečnost lze potvrdit logikou (podmnožinová pravidla, základní pravidla).
* **forced:** Políčka, kde se mina podle čísel musí nacházet.

#### Logika přesunu miny
Pokud uživatel nemůže mít jistotu (množina *safe* je prázdná) a trefí minu:
1.  [cite_start]Algoritmus vybere náhodné políčko z dosud neoznačených a neodhalených pozic[cite: 34].
2.  Přesune minu na toto nové místo.
3.  [cite_start]Lokálně opraví čísla v okolí, aniž by přepočítával celou plochu[cite: 35].

### Struktura projektu a moduly
[cite_start]Projekt je rozdělen do následujících souborů[cite: 37]:

#### 1. `constants.py`
[cite_start]Definice sdílených konstant pro snadnou konfiguraci hry[cite: 38, 44].
* [cite_start]**Symboly:** `znakMina` (*), `znakVlajka` (F), `znakNeodkryte` (-), `znakPrazdne` (mezera) [cite: 46-51].
* [cite_start]**Parametry plochy:** `pocetRadku`, `pocetSloupcu`, `pocetMin` [cite: 54-56].
* [cite_start]**Směry:** Seznam 8 směrů pro posun souřadnic[cite: 58].

#### 2. `board.py`
[cite_start]Zodpovídá za správu herní plochy bez interakce s hráčem[cite: 61].
* [cite_start]`generujPlochu(radky, sloupce, pocet_min)`: Vytvoří matici a náhodně rozmístí miny[cite: 63, 64].
* [cite_start]`prepoctiPlochu(...)`: Spočítá sousední miny pro každou buňku[cite: 66, 67].
* [cite_start]`odkrytPolicko(...)`: Rekurzivní flood-fill pro odkrývání prázdných oblastí[cite: 68, 69].
* [cite_start]`vypisPlochu(...)`: Vykreslí aktuální stav do konzole včetně ohraničení a souřadnic[cite: 70, 71].

#### 3. `solver.py`
[cite_start]Jádro umělé inteligence hry[cite: 73].
* `jePolickoSafe(...)`: Hlavní dedukční funkce. Vrací množiny `safe` a `vynuceneMiny` na základě:
    * [cite_start]Pravidla n=0 (všichni sousedé nuly jsou bezpeční)[cite: 78].
    * [cite_start]Pravidla úplného pokrytí (počet vlajek + zakrytých = číslo v políčku)[cite: 79].
    * [cite_start]Podmnožinové dedukce (porovnávání omezení sousedů)[cite: 80].
* [cite_start]`jePodmonozina(a, b)`: Pomocná funkce pro množinové operace[cite: 74].

#### 4. `fair_rules.py`
* [cite_start]`vyhodnot_tah(...)`: Určuje výsledek tahu[cite: 82]:
    * [cite_start]Vrací **PROHRA**: Pokud hráč klikne na jistou minu nebo na nebezpečné pole, když existovalo bezpečné[cite: 83, 84].
    * [cite_start]Vrací **ODEBRANA_MINA**: Pokud hráč klikne na minu v situaci "nutného hádání" (přesun miny)[cite: 85].
    * [cite_start]Vrací **OK**: Standardní odkrytí[cite: 86].

#### 5. `game_logic.py`
[cite_start]Zajišťuje hlavní smyčku (`hra()`), vstupy a řízení toku[cite: 88, 95].
* [cite_start]Cyklus: Výpočet interních vlajek -> Dedukce (solver) -> Vykreslení -> Vstup -> Vyhodnocení (fair_rules)[cite: 96].
* [cite_start]`validniSouradnice(...)`: Kontrola rozsahu pole[cite: 91].
* [cite_start]`vyhra(...)`: Kontrola, zda jsou odkryta všechna neminová pole[cite: 93].

#### 6. `tests.py`
[cite_start]Obsahuje unit testy pro ověření funkčnosti[cite: 42].
