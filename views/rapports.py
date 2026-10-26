"""Rapports."""

from views.commun import (afficher_tableau, afficher_titre, formater_date, formater_date_heure, formater_points,
                          nom_joueur)
from views.tournois import statut


def afficher_tournois(tournois):
    afficher_titre("Liste de tous les tournois")
    afficher_tableau(
        ["Nom", "Lieu", "Début", "Fin", "Joueurs", "Statut"],
        [
            [tournoi.nom, tournoi.lieu, formater_date(tournoi.date_debut), formater_date(tournoi.date_fin),
             len(tournoi.joueurs), statut(tournoi)]
            for tournoi in tournois
        ],
    )


def afficher_nom_et_dates(tournoi):
    afficher_titre(tournoi.nom)
    print(f"Du {formater_date(tournoi.date_debut)} au {formater_date(tournoi.date_fin)}")


def _resultat(match, joueurs_du_club):
    joueur1 = nom_joueur(match.joueur1, joueurs_du_club)
    joueur2 = nom_joueur(match.joueur2, joueurs_du_club)
    if not match.est_joue:
        return f"{joueur1} contre {joueur2} : à jouer"
    return f"{joueur1} {formater_points(match.score1)} - {formater_points(match.score2)} {joueur2}"


def afficher_tours_et_matchs(tournoi, joueurs_du_club):
    afficher_titre(f"Tours et matchs : {tournoi.nom}")
    if not tournoi.tours:
        print("Aucun tour n'a encore été joué.")
        return
    for tour in tournoi.tours:
        print(f"\n{tour.nom} (début : {formater_date_heure(tour.debut)}, fin : {formater_date_heure(tour.fin)})")
        for match in tour.matchs:
            print(f"  - {_resultat(match, joueurs_du_club)}")
        if tour.exempt is not None:
            print(f"  - Exempt : {nom_joueur(tour.exempt, joueurs_du_club)}")
