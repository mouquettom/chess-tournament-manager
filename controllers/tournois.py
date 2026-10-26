"""Création et déroulement des tournois."""

from models.joueur import Joueur
from models.tournoi import Tournoi
from views import joueurs as vue_joueurs
from views import menus
from views import tournois as vue
from views.commun import afficher_erreur, afficher_message, nom_joueur


class TournoiController:

    def __init__(self, depot, joueur_controller):
        self.depot = depot
        self.club = joueur_controller

    # --- Création et ouverture -------------------------------------------

    def creer(self):
        tournoi = Tournoi(**vue.demander_infos_tournoi())
        if not vue.confirmer_creation(tournoi):
            afficher_message("Création annulée.")
            return
        self.depot.sauvegarder(tournoi)
        afficher_message(f"Le tournoi « {tournoi.nom} » a été créé.")
        self.gerer(tournoi)

    def ouvrir(self):
        tournois = self.depot.lister()
        vue.afficher_fichiers_illisibles(self.depot.fichiers_illisibles)
        tournoi = vue.choisir_tournoi(tournois, "Quel tournoi voulez-vous ouvrir ?")
        if tournoi is not None:
            self.gerer(tournoi)

    def gerer(self, tournoi):
        while True:
            vue.afficher_entete(tournoi)
            choix = menus.menu_tournoi(tournoi)
            if choix == "inscrire":
                self.inscrire_joueurs(tournoi)
            elif choix == "jouer":
                self.jouer(tournoi)
            elif choix == "classement":
                self.afficher_classement(tournoi)
            elif choix == "description":
                tournoi.description = vue.demander_description(tournoi.description)
                self.depot.sauvegarder(tournoi)
            else:
                return

    # --- Inscriptions ----------------------------------------------------

    def inscrire_joueurs(self, tournoi):
        while True:
            disponibles = [joueur for joueur in self.club.joueurs_tries()
                           if joueur.identifiant not in tournoi.joueurs]
            choix = vue_joueurs.choisir_joueur_a_inscrire(disponibles, len(tournoi.joueurs))
            if choix is None:
                return
            joueur = self.club.creer_joueur() if choix == vue_joueurs.NOUVEAU_JOUEUR else choix
            if joueur is not None:
                tournoi.inscrire_joueur(joueur.identifiant)
                self.depot.sauvegarder(tournoi)
                afficher_message(f"{joueur.nom_complet} est inscrit(e) au tournoi.")

    # --- Déroulement -----------------------------------------------------

    def jouer(self, tournoi):
        """Lance le tour suivant (ou reprend le tour en cours) et fait saisir les résultats.

        Le tournoi est sauvegardé après chaque résultat : on peut quitter et reprendre à tout moment.
        """
        while not tournoi.est_termine:
            tour = tournoi.tour_en_cours
            nouveau_tour = tour is None
            if nouveau_tour:
                if len(tournoi.joueurs) < 2:
                    afficher_erreur("inscrivez au moins deux joueurs avant de lancer le tournoi.")
                    return
                tour = tournoi.demarrer_tour_suivant()
                self.depot.sauvegarder(tournoi)

            vue.afficher_appariements(tour, self.club.joueurs)
            revanches = tournoi.revanches(tour) if nouveau_tour else []
            if revanches:
                vue.avertir_revanches(revanches, self.club.joueurs)

            total = len(tour.matchs)
            for match in tour.matchs_a_jouer:
                numero = tour.matchs.index(match) + 1
                resultat = vue.demander_resultat(match, self.club.joueurs, numero, total)
                if resultat is None:
                    afficher_message("Saisie interrompue : les résultats déjà saisis sont enregistrés.")
                    return
                match.enregistrer_resultat(resultat)
                self.depot.sauvegarder(tournoi)

            tour.terminer()
            self.depot.sauvegarder(tournoi)
            vue.afficher_fin_tour(tour)

            if tournoi.est_termine:
                self.afficher_classement(tournoi, "Classement final")
                return
            self.afficher_classement(tournoi)
            if not vue.demander_lancement(tournoi.numero_tour_actuel + 1):
                return

    def afficher_classement(self, tournoi, titre="Classement"):
        points = tournoi.points()
        club = self.club.joueurs

        def cle(identifiant):
            joueur = club.get(identifiant)
            return -points[identifiant], joueur.cle_tri() if joueur else (identifiant, "")

        lignes = [(nom_joueur(identifiant, club), points[identifiant])
                  for identifiant in sorted(tournoi.joueurs, key=cle)]
        vue.afficher_classement(lignes, titre)

    def joueurs_du_tournoi(self, tournoi):
        """Joueurs inscrits, par ordre alphabétique (les identifiants inconnus du club sont ignorés)."""
        joueurs = [self.club.joueurs[i] for i in tournoi.joueurs if i in self.club.joueurs]
        return sorted(joueurs, key=Joueur.cle_tri)
