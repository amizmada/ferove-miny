# FÉROVÉ MINY (Fair Minesweeper)

**Autor:** Adam Zima
**Předmět:** Programování 1 (NPRG030)

## 📖 Úvod
Tento projekt je implementací klasické hry Minesweeper v konzolovém prostředí, která je obohacena o „férovou“ dedukční logiku.

### Co znamená „Férová logika“?
Hra zajišťuje, že každé odhalení nebo označení miny probíhá spravedlivě:
1.  **Bezpečný začátek:** Začínáte bez jakýchkoli informací. Pokud v dané situaci není možné logicky najít bezpečné políčko (např. na začátku hry), hra garantuje, že po odkrytí libovolného políčka na něm mina nebude.
2.  **Trest za chybu:** Pokud existuje políčko, které je jistě bez miny (lze to dedukovat), a vy přesto riskujete odhalením jiného neznámého pole, na kterém je mina, prohráváte.
3.  **Řešitelnost:** Tento přístup garantuje, že každý tah je buď čistě logický, nebo (v nutných případech) jde o hádání, které neskončí prohrou.

---

## 🎮 Uživatelská dokumentace

### Cíl hry
Cílem je odkrýt všechna políčka, která neobsahují miny. Je nutné se vyhnout minám náhodně rozmístěným po ploše.

### Ovládání
Hra se ovládá zadáváním textových příkazů do konzole.

* **Odkrytí políčka:**
  Zadejte souřadnice ve formátu `Řádek Sloupec` (např. `2 3`).
* **Vlajka (označení miny)::**
  Zadejte souřadnice následované písmenem F: `Řádek Sloupec F` (např. `1 4 F`). Příkaz slouží k přidání i odstranění vlajky.

### Symboly na herní ploše
* `-` (pomlčka): Zakryté políčko.
* `1`–`8`: Počet min v okolních 8 políčkách.
* ` ` (mezera): Představuje 0, tedy políčko bez sousedních min (automaticky odkryje své okolí).
* `*` (hvězdička): Zobrazuje minu (objeví se při prohře nebo při férovém odstranění).
* `F`: Vlajka uživatele pro označení miny.

### Konec hry
Hra může skončit třemi způsoby:
1.  **PROHRA:** Hráč odkryje políčko, kde je mina.
2.  **PROHRA:** Hráč odkryje neznámé políčko v situaci, kdy mohl mít jistotu o jiném bezpečném poli.
3.  **VÝHRA:** Hráč úspěšně odkryje všechna neminová políčka.

---

## 🛠 Programátorská dokumentace

### Popis algoritmu
Program udržuje stav hry v matici, která obsahuje souřadnice min, množinu odhalených polí (`odkryto`) a vlajky (`flags`).

#### Dedukční modul
Při každém tahu algoritmus na základě sousedních čísel generuje dvě množiny:
* **safe:** Políčka, jejichž bezpečnost lze potvrdit logikou (podmnožinová pravidla, základní pravidla).
* **forced:** Políčka, kde se mina podle čísel musí nacházet.

#### Logika přesunu miny
Pokud uživatel nemůže mít jistotu (množina *safe* je prázdná) a trefí minu:
1.  Algoritmus vybere náhodné políčko z dosud neoznačených a neodhalených pozic.
2.  Přesune minu na toto nové místo.
3.  Lokálně opraví čísla v okolí, aniž by přepočítával celou plochu.

### Struktura projektu a moduly

#### 1. `constants.py`
Definice sdílených konstant pro snadnou konfiguraci hry.
* **Symboly:** `znakMina` (*), `znakVlajka` (F), `znakNeodkryte` (-), `znakPrazdne` (mezera).
* **Parametry plochy:** `pocetRadku`, `pocetSloupcu`, `pocetMin`.
* **Směry:** Seznam 8 směrů pro posun souřadnic.

#### 2. `board.py`
Zodpovídá za správu herní plochy bez interakce s hráčem.
* `generujPlochu(radky, sloupce, pocet_min)`: Vytvoří matici a náhodně rozmístí miny.
* `prepoctiPlochu(...)`: Spočítá sousední miny pro každou buňku.
* `odkrytPolicko(...)`: Rekurzivní flood-fill pro odkrývání prázdných oblastí.
* `vypisPlochu(...)`: Vykreslí aktuální stav do konzole včetně ohraničení a souřadnic.

#### 3. `solver.py`
Jádro umělé inteligence hry.
* `jePolickoSafe(...)`: Hlavní dedukční funkce. Vrací množiny `safe` a `vynuceneMiny`. Využívá pravidla n=0, pravidla úplného pokrytí a podmnožinovou dedukci.
* `jePodmonozina(a, b)`: Pomocná funkce pro množinové operace.

#### 4. `fair_rules.py`
* `vyhodnot_tah(...)`: Určuje výsledek tahu:
    * Vrací **PROHRA**: Pokud hráč klikne na jistou minu nebo na nebezpečné pole, když existovalo bezpečné.
    * Vrací **ODEBRANA_MINA**: Pokud hráč klikne na minu v situaci "nutného hádání" (přesun miny).
    * Vrací **OK**: Standardní odkrytí.

#### 5. `game_logic.py`
Zajišťuje hlavní smyčku (`hra()`), vstupy a řízení toku.
* Cyklus: Výpočet interních vlajek -> Dedukce (solver) -> Vykreslení -> Vstup -> Vyhodnocení (fair_rules).
* `validniSouradnice(...)`: Kontrola rozsahu pole.
* `vyhra(...)`: Kontrola, zda jsou odkryta všechna neminová pole.

#### 6. `tests.py`
Obsahuje unit testy pro ověření funkčnosti jednotlivých komponent.
