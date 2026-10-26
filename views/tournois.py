"""Vues liées aux tournois et à leur déroulement."""

from models.match import MATCH_NUL, VICTOIRE_JOUEUR1, VICTOIRE_JOUEUR2
from models.tournoi import NOMBRE_TOURS_PAR_DEFAUT
from views.commun import (afficher_erreur, afficher_tableau, afficher_titre, formater_date, formater_points,
                          nom_joueur)
from views.saisie import (demander_choix, demander_date, demander_entier, demander_oui_non, demander_texte,
                          demander_texte_facultatif)


def statut(tournoi):
    if tournoi.est_termine:
        return "Terminé"
    if not tournoi.est_commence:
        return "Non commencé"
    numero = f"{tournoi.numero_tour_actuel}/{tournoi.nombre_tours}"
    if tournoi.tour_en_cours is not None:
        return f"Round {numero} en cours"
    return f"Round {numero} terminé"


def demander_infos_tournoi():
    print("\nNouveau tournoi")
    nom = demander_texte("Nom du tournoi : ")
    lieu = demander_texte("Lieu : ")
    date_debut = demander_date("Date de début (jj/mm/aaaa) : ")
    date_fin = demander_date("Date de fin (jj/mm/aaaa) : ", minimum=date_debut)
    nombre_tours = demander_entier(
        f"Nombre de tours (Entrée pour {NOMBRE_TOURS_PAR_DEFAUT}) : ", 1, defaut=NOMBRE_TOURS_PAR_DEFAUT)
    description = demander_texte_facultatif("Description / remarques du directeur (facultatif) : ")
    return {
        "nom": nom,
        "lieu": lieu,
        "date_debut": date_debut,
        "date_fin": date_fin,
        "nombre_tours": nombre_tours,
        "description": description,
    }


def confirmer_creation(tournoi):
    print(f"\n{tournoi.nom} - {tournoi.lieu}, du {formater_date(tournoi.date_debut)} "
          f"au {formater_date(tournoi.date_fin)}, {tournoi.nombre_tours} tours")
    return demander_oui_non("Confirmez-vous la création de ce tournoi ?")


def afficher_entete(tournoi):
    afficher_titre(f"Tournoi : {tournoi.nom}")
    print(f"{tournoi.lieu}, du {formater_date(tournoi.date_debut)} au {formater_date(tournoi.date_fin)}")
    print(f"Joueurs inscrits : {len(tournoi.joueurs)} - {statut(tournoi)}")
    if tournoi.description:
        print(f"Description : {tournoi.description}")


def choisir_tournoi(tournois, titre="Choisissez un tournoi :"):
    """Renvoie le tournoi choisi, ou None si l'utilisateur annule."""
    if not tournois:
        print("\nAucun tournoi enregistré.")
        return None
    options = [
        f"{tournoi.nom} ({tournoi.lieu}, {formater_date(tournoi.date_debut)}) - {statut(tournoi)}"
        for tournoi in tournois
    ]
    index = demander_choix(options + ["Annuler"], titre)
    return tournois[index] if index < len(tournois) else None


def afficher_fichiers_illisibles(fichiers):
    for fichier in fichiers:
        afficher_erreur(f"le fichier « {fichier} » est illisible et a été ignoré.")


def demander_description(actuelle):
    print(f"\nDescription actuelle : {actuelle or '(vide)'}")
    return demander_texte_facultatif("Nouvelle description (Entrée pour conserver) : ", defaut=actuelle)


def demander_lancement(numero):
    return demander_oui_non(f"\nLancer le Round {numero} maintenant ?")


def afficher_appariements(tour, joueurs_du_club):
    afficher_titre(f"{tour.nom} - appariements")
    for numero, match in enumerate(tour.matchs, start=1):
        print(f"Match {numero} : {nom_joueur(match.joueur1, joueurs_du_club)} "
              f"contre {nom_joueur(match.joueur2, joueurs_du_club)}")
    if tour.exempt is not None:
        print(f"Exempt (1 point) : {nom_joueur(tour.exempt, joueurs_du_club)}")


def avertir_revanches(matchs, joueurs_du_club):
    print("\nAttention : aucun appariement sans revanche n'était possible pour ce tour.")
    for match in matchs:
        print(f" - {nom_joueur(match.joueur1, joueurs_du_club)} et "
              f"{nom_joueur(match.joueur2, joueurs_du_club)} se sont déjà rencontrés.")


def demander_resultat(match, joueurs_du_club, numero, total):
    """Renvoie le résultat saisi, ou None pour interrompre la saisie."""
    joueur1 = nom_joueur(match.joueur1, joueurs_du_club)
    joueur2 = nom_joueur(match.joueur2, joueurs_du_club)
    resultats = [VICTOIRE_JOUEUR1, VICTOIRE_JOUEUR2, MATCH_NUL, None]
    options = [f"{joueur1} gagne", f"{joueur2} gagne", "Match nul", "Interrompre la saisie (reprise possible)"]
    return resultats[demander_choix(options, f"Match {numero}/{total} : {joueur1} contre {joueur2}")]


def afficher_fin_tour(tour):
    print(f"\n{tour.nom} terminé.")


def afficher_classement(lignes, titre="Classement"):
    """`lignes` : liste de (joueur affiché, points), triée par points décroissants.
    Les ex aequo partagent le même rang."""
    afficher_titre(titre)
    tableau, rang, points_precedents = [], 0, None
    for position, (joueur, points) in enumerate(lignes, start=1):
        if points != points_precedents:
            rang, points_precedents = position, points
        tableau.append([rang, joueur, formater_points(points)])
    afficher_tableau(["Rang", "Joueur", "Points"], tableau)
