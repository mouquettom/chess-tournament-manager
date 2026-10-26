"""Rapports."""

from views import joueurs as vue_joueurs
from views import menus
from views import rapports as vue
from views import tournois as vue_tournois


class RapportController:

    def __init__(self, depot_tournois, joueur_controller, tournoi_controller):
        self.depot_tournois = depot_tournois
        self.club = joueur_controller
        self.tournois = tournoi_controller

    def menu(self):
        while True:
            choix = menus.menu_rapports()
            if choix == "retour":
                return
            if choix == "joueurs_club":
                self.club.lister()
                continue

            tournois = self.depot_tournois.lister()
            vue_tournois.afficher_fichiers_illisibles(self.depot_tournois.fichiers_illisibles)
            if choix == "tournois":
                vue.afficher_tournois(tournois)
                continue

            tournoi = vue_tournois.choisir_tournoi(tournois)
            if tournoi is None:
                continue
            if choix == "nom_et_dates":
                vue.afficher_nom_et_dates(tournoi)
            elif choix == "joueurs_tournoi":
                vue_joueurs.afficher_joueurs(
                    self.tournois.joueurs_du_tournoi(tournoi), f"Joueurs du tournoi {tournoi.nom}")
            elif choix == "tours_et_matchs":
                vue.afficher_tours_et_matchs(tournoi, self.club.joueurs)
