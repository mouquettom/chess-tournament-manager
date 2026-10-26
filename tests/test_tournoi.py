import random
import unittest
from datetime import date

from models.match import MATCH_NUL, VICTOIRE_JOUEUR1, VICTOIRE_JOUEUR2
from models.tournoi import Tournoi

RESULTATS = [VICTOIRE_JOUEUR1, VICTOIRE_JOUEUR2, MATCH_NUL]


def creer_tournoi(nombre_joueurs, nombre_tours=4):
    tournoi = Tournoi("Open", "Paris", date(2025, 1, 1), date(2025, 1, 2), nombre_tours=nombre_tours)
    for numero in range(nombre_joueurs):
        tournoi.inscrire_joueur(f"AB{numero:05d}")
    return tournoi


def jouer_tour(tournoi, resultat=None):
    tour = tournoi.demarrer_tour_suivant()
    for match in tour.matchs:
        match.enregistrer_resultat(resultat or random.choice(RESULTATS))
    tour.terminer()
    return tour


class TestCreation(unittest.TestCase):

    def test_date_de_fin_avant_le_debut_refusee(self):
        with self.assertRaises(ValueError):
            Tournoi("Open", "Paris", date(2025, 1, 2), date(2025, 1, 1))

    def test_nom_vide_refuse(self):
        with self.assertRaises(ValueError):
            Tournoi("  ", "Paris", date(2025, 1, 1), date(2025, 1, 1))

    def test_quatre_tours_par_defaut(self):
        self.assertEqual(Tournoi("Open", "Paris", date(2025, 1, 1), date(2025, 1, 1)).nombre_tours, 4)

    def test_inscription_impossible_apres_le_debut(self):
        tournoi = creer_tournoi(4)
        tournoi.demarrer_tour_suivant()
        with self.assertRaises(ValueError):
            tournoi.inscrire_joueur("ZZ99999")

    def test_double_inscription_refusee(self):
        tournoi = creer_tournoi(2)
        with self.assertRaises(ValueError):
            tournoi.inscrire_joueur("AB00000")


class TestAppariements(unittest.TestCase):

    def test_premier_tour_aleatoire(self):
        appariements = set()
        for graine in range(50):
            random.seed(graine)
            tour = creer_tournoi(4).demarrer_tour_suivant()
            appariements.add(frozenset(frozenset(match.joueurs) for match in tour.matchs))
        # Avec 4 joueurs, il existe 3 appariements possibles : tous doivent apparaître.
        self.assertEqual(len(appariements), 3)

    def test_tours_suivants_par_points(self):
        random.seed(0)
        tournoi = creer_tournoi(8)
        jouer_tour(tournoi, VICTOIRE_JOUEUR1)
        points = tournoi.points()
        tour = tournoi.demarrer_tour_suivant()
        # Les gagnants du premier tour se rencontrent entre eux.
        for match in tour.matchs:
            self.assertEqual(points[match.joueur1], points[match.joueur2])

    def test_aucune_revanche_quand_c_est_possible(self):
        for graine in range(100):
            random.seed(graine)
            tournoi = creer_tournoi(8, nombre_tours=5)
            while not tournoi.est_termine:
                tour = jouer_tour(tournoi)
                self.assertEqual(tournoi.revanches(tour), [], f"graine {graine}, {tour.nom}")

    def test_nombre_impair_de_joueurs_exempt_different_a_chaque_tour(self):
        random.seed(1)
        tournoi = creer_tournoi(5)
        exemptes = [jouer_tour(tournoi).exempt for _ in range(4)]
        self.assertNotIn(None, exemptes)
        self.assertEqual(len(set(exemptes)), 4)

    def test_tous_les_joueurs_jouent_ou_sont_exemptes(self):
        tournoi = creer_tournoi(7)
        tour = tournoi.demarrer_tour_suivant()
        presents = {joueur for match in tour.matchs for joueur in match.joueurs} | {tour.exempt}
        self.assertEqual(presents, set(tournoi.joueurs))


class TestDeroulement(unittest.TestCase):

    def test_un_tour_par_round(self):
        tournoi = creer_tournoi(4)
        jouer_tour(tournoi)
        jouer_tour(tournoi)
        self.assertEqual([tour.nom for tour in tournoi.tours], ["Round 1", "Round 2"])
        self.assertEqual(tournoi.numero_tour_actuel, 2)

    def test_tour_horodate(self):
        tour = jouer_tour(creer_tournoi(2))
        self.assertIsNotNone(tour.debut)
        self.assertIsNotNone(tour.fin)
        self.assertLessEqual(tour.debut, tour.fin)

    def test_impossible_de_terminer_un_tour_incomplet(self):
        tour = creer_tournoi(4).demarrer_tour_suivant()
        with self.assertRaises(ValueError):
            tour.terminer()

    def test_impossible_de_lancer_un_tour_avant_la_fin_du_precedent(self):
        tournoi = creer_tournoi(4)
        tournoi.demarrer_tour_suivant()
        with self.assertRaises(ValueError):
            tournoi.demarrer_tour_suivant()

    def test_tournoi_termine_apres_le_dernier_tour(self):
        tournoi = creer_tournoi(4, nombre_tours=2)
        jouer_tour(tournoi)
        self.assertFalse(tournoi.est_termine)
        jouer_tour(tournoi)
        self.assertTrue(tournoi.est_termine)
        with self.assertRaises(ValueError):
            tournoi.demarrer_tour_suivant()

    def test_il_faut_deux_joueurs(self):
        with self.assertRaises(ValueError):
            creer_tournoi(1).demarrer_tour_suivant()

    def test_points(self):
        tournoi = creer_tournoi(3, nombre_tours=1)
        tour = tournoi.demarrer_tour_suivant()
        match = tour.matchs[0]
        match.enregistrer_resultat(MATCH_NUL)
        points = tournoi.points()
        self.assertEqual(points[match.joueur1], 0.5)
        self.assertEqual(points[match.joueur2], 0.5)
        self.assertEqual(points[tour.exempt], 1.0)


if __name__ == "__main__":
    unittest.main()
