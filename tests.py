import unittest
import board, game_logic, solver
from fair_rules import vyhodnotTah
from constants import ZNAK_PRAZDNE, ZNAK_MINA


class TestZakladniFunkce(unittest.TestCase):
    """Jednodušší základní kontroly nad moduly board/solver/game_logic."""

    def test_generuj_a_prepocti(self):
        plocha, miny = board.generujPlochu(4, 4, 5)
        board.prepoctiPlochu(plocha, miny, 4, 4)
        # každá buňka je jedno­znakový string
        for radek in plocha:
            for znak in radek:
                self.assertIsInstance(znak, str)
                self.assertEqual(len(znak), 1)

    def test_validniSouradnice(self):
        self.assertTrue(game_logic.validniSouradnice(1, 1, 3, 3))
        self.assertFalse(game_logic.validniSouradnice(3, 0, 3, 3))

    def test_vyhra_funkce(self):
        odkryto = [[True, False], [True, True]]
        miny = {(0, 1)}
        self.assertTrue(game_logic.vyhra(odkryto, miny))
        # skryjeme neminové pole – tím už nemají být všechny ne-miny odkryté -> nevýhra
        odkryto[0][0] = False  # neminové pole skryté
        self.assertFalse(game_logic.vyhra(odkryto, miny))


class TestFerovaLogika(unittest.TestCase):
    """Komplexní testy férové logiky (fair_engine)."""
    def _init_board(self, R=5, S=5, minySouradnice={(0, 0)}):
        """Vytvoří desku (standardně 5×5) s minami podle minySouradnice."""
        plocha = [[ZNAK_PRAZDNE for _ in range(S)] for _ in range(R)]
        miny = set(minySouradnice)
        for r, s in miny:
            plocha[r][s] = ZNAK_MINA
        board.prepoctiPlochu(plocha, miny, R, S)
        odkryto = [[False] * S for _ in range(R)]
        flags   = [[False] * S for _ in range(R)]
        return plocha, miny, odkryto, flags

    def _assert_cislaNaPlose(self, plocha, miny):
        """Kontrola, že všechna čísla sedí k poloze min."""
        radky, sloupce = len(plocha), len(plocha[0])
        for r in range(radky):
            for s in range(sloupce):
                expected = ZNAK_MINA if (r, s) in miny else self.pocetSousednichMin(r, s, miny, radky, sloupce)
                self.assertEqual(plocha[r][s], expected,
                                 msg=f"({r},{s}): očekávám '{expected}', dostal '{plocha[r][s]}'")

    def pocetSousednichMin(self, r, s, miny, R, S):
        if (r, s) in miny:
            return ZNAK_MINA
        pocet = 0
        for dr in (-1, 0, 1):
            for ds in (-1, 0, 1):
                if dr == ds == 0:
                    continue
                nr, ns = r + dr, s + ds
                if 0 <= nr < R and 0 <= ns < S and (nr, ns) in miny:
                    pocet += 1
        return ZNAK_PRAZDNE if pocet == 0 else str(pocet)

    # nové testy
    def test_odebraniMinyHadani(self):
        plocha, miny, odkryto, flags = self._init_board()
        status, plocha, miny, odkryto = vyhodnotTah(plocha, miny, odkryto, flags, bezpecnaPole=[], skryteVlajky=[], r=0, s=0)
        self.assertEqual(status, "ODEBRANA_MINA")
        self.assertNotIn((0, 0), miny)
        self._assert_cislaNaPlose(plocha, miny)

    def test_pridaniMinyProhra(self):
        plocha, miny, odkryto, flags = self._init_board()
        status, plocha, miny, _ = vyhodnotTah(plocha, miny, odkryto, flags, bezpecnaPole=[(1, 1)], skryteVlajky=[], r=1, s=0)
        self.assertEqual(status, "PROHRA")
        self.assertIn((1, 0), miny)
        self._assert_cislaNaPlose(plocha, miny)

    def test_klikNaSkrytouMinu(self):
        plocha, miny, odkryto, flags = self._init_board()
        status, plocha, miny, odkryto = vyhodnotTah(plocha, miny, odkryto, flags, bezpecnaPole=[], skryteVlajky=[(1, 0)], r=1, s=0)
        self.assertEqual(status, "PROHRA")

    def test_bezneOdkryti(self):
        plocha, miny, odkryto, flags = self._init_board()
        status, plocha, miny, odkryto = vyhodnotTah(plocha, miny, odkryto, flags, bezpecnaPole=[], skryteVlajky=[], r=1, s=1)
        self.assertEqual(status, "OK")
        self.assertTrue(odkryto[1][1])
        self._assert_cislaNaPlose(plocha, miny)


if __name__ == "__main__":
    unittest.main()