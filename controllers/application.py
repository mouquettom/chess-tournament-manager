"""Point d'entrée des contrôleurs : chargement des données et menu principal."""

from controllers.joueurs import JoueurController
from controllers.rapports import RapportController
from controllers.tournois import TournoiController
from models.depot import DOSSIER_DONNEES, DepotJoueurs, DepotTournois
from views import menus
from views.commun import afficher_erreur


class ApplicationController:

    def __init__(self, dossier_donnees=DOSSIER_DONNEES):
        self.depot_joueurs = DepotJoueurs(dossier_donnees)
        self.depot_tournois = DepotTournois(dossier_donnees)

    def lancer(self):
        menus.afficher_bienvenue()
        try:
            joueurs = self.depot_joueurs.charger()
        except (OSError, ValueError, KeyError, TypeError) as erreur:
            # On s'arrête plutôt que de risquer d'écraser la base des joueurs.
            afficher_erreur(f"impossible de lire {self.depot_joueurs.chemin} ({erreur}).")
            return

        club = JoueurController(self.depot_joueurs, joueurs)
        tournois = TournoiController(self.depot_tournois, club)
        rapports = RapportController(self.depot_tournois, club, tournois)
        actions = {
            "joueurs": club.menu,
            "creer_tournoi": tournois.creer,
            "ouvrir_tournoi": tournois.ouvrir,
            "rapports": rapports.menu,
        }

        while True:
            choix = menus.menu_principal()
            if choix == "quitter":
                menus.afficher_au_revoir()
                return
            try:
                actions[choix]()
            except OSError as erreur:
                afficher_erreur(f"la sauvegarde a échoué ({erreur}).")
