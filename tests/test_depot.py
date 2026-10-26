import tempfile
import unittest
from datetime import date
from pathlib import Path

from models.depot import DepotJoueurs, DepotTournois
from models.joueur import Joueur
from models.match import VICTOIRE_JOUEUR2
from models.tournoi import Tournoi


class TestDepot(unittest.TestCase):

    def setUp(self):
        self._dossier = tempfile.TemporaryDirectory()
        self.dossier = Path(self._dossier.name)

    def tearDown(self):
        self._dossier.cleanup()

    def test_joueurs_aller_retour(self):
        depot = DepotJoueurs(self.dossier)
        joueur = Joueur("AB12345", "Zola", "Émile", date(2000, 1, 1), "h")
        depot.sauvegarder({joueur.identifiant: joueur})
        recharge = depot.charger()["AB12345"]
        self.assertEqual(recharge.vers_dict(), joueur.vers_dict())

    def test_aucun_fichier_joueurs(self):
        self.assertEqual(DepotJoueurs(self.dossier).charger(), {})

    def test_tournoi_aller_retour_avec_tours_et_scores(self):
        depot = DepotTournois(self.dossier)
        tournoi = Tournoi("Open de Paris", "Paris", date(2025, 1, 1), date(2025, 1, 5), description="Test")
        for identifiant in ("AB00001", "AB00002", "AB00003"):
            tournoi.inscrire_joueur(identifiant)
        tour = tournoi.demarrer_tour_suivant()
        tour.matchs[0].enregistrer_resultat(VICTOIRE_JOUEUR2)
        tour.terminer()
        depot.sauvegarder(tournoi)

        recharge = depot.lister()[0]
        self.assertEqual(recharge.vers_dict(), tournoi.vers_dict())
        self.assertEqual(recharge.points(), tournoi.points())
        self.assertEqual(recharge.paires_deja_jouees(), tournoi.paires_deja_jouees())

    def test_tournois_homonymes_dans_des_fichiers_distincts(self):
        depot = DepotTournois(self.dossier)
        for _ in range(2):
            depot.sauvegarder(Tournoi("Open", "Paris", date(2025, 1, 1), date(2025, 1, 1)))
        self.assertEqual(len(depot.lister()), 2)

    def test_fichier_illisible_ignore(self):
        depot = DepotTournois(self.dossier)
        depot.sauvegarder(Tournoi("Open", "Paris", date(2025, 1, 1), date(2025, 1, 1)))
        (depot.dossier / "casse.json").write_text("{pas du json", encoding="utf-8")
        self.assertEqual(len(depot.lister()), 1)
        self.assertEqual(depot.fichiers_illisibles, ["casse.json"])


class TestJoueur(unittest.TestCase):

    def test_identifiant(self):
        self.assertTrue(Joueur.identifiant_valide("AB12345"))
        for invalide in ("ab12345", "AB1234", "A123456", "AB123456", ""):
            self.assertFalse(Joueur.identifiant_valide(invalide), invalide)

    def test_tri_insensible_a_la_casse_et_aux_accents(self):
        noms = ["Zola", "de Gaulle", "Éluard", "Dupont"]
        joueurs = [Joueur(f"AB0000{i}", nom, "X", date(2000, 1, 1), "h") for i, nom in enumerate(noms)]
        self.assertEqual([j.nom for j in sorted(joueurs, key=Joueur.cle_tri)],
                         ["de Gaulle", "Dupont", "Éluard", "Zola"])

    def test_date_de_naissance_future_refusee(self):
        with self.assertRaises(ValueError):
            Joueur("AB12345", "Zola", "Émile", date(2999, 1, 1), "h")


if __name__ == "__main__":
    unittest.main()
