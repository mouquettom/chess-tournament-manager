"""Gestion des joueurs du club."""

from models.joueur import Joueur
from views import joueurs as vue
from views import menus
from views.commun import afficher_erreur, afficher_message


class JoueurController:

    def __init__(self, depot, joueurs):
        self.depot = depot
        # {identifiant: Joueur}
        self.joueurs = joueurs

    def menu(self):
        while True:
            choix = menus.menu_joueurs()
            if choix == "ajouter":
                self.creer_joueur()
            elif choix == "lister":
                self.lister()
            else:
                return

    def joueurs_tries(self):
        return sorted(self.joueurs.values(), key=Joueur.cle_tri)

    def lister(self):
        vue.afficher_joueurs(self.joueurs_tries(), "Joueurs du club (ordre alphabétique)")

    def creer_joueur(self):
        """Ajoute un joueur au club et le renvoie (None si l'ajout est annulé)."""
        identifiant = vue.demander_identifiant_joueur()
        while identifiant in self.joueurs:
            afficher_erreur(f"l'identifiant {identifiant} est déjà attribué à "
                            f"{self.joueurs[identifiant].nom_complet}.")
            identifiant = vue.demander_identifiant_joueur()

        joueur = Joueur(identifiant=identifiant, **vue.demander_infos_joueur())
        if not vue.confirmer_ajout(joueur):
            afficher_message("Ajout annulé.")
            return None

        self.joueurs[identifiant] = joueur
        self.depot.sauvegarder(self.joueurs)
        afficher_message(f"{joueur.nom_complet} a été ajouté(e) au club.")
        return joueur
