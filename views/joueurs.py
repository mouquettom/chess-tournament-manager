"""Vues liées aux joueurs."""

from datetime import date

from views.commun import afficher_erreur, afficher_tableau, afficher_titre, formater_date
from views.saisie import demander_choix, demander_date, demander_identifiant, demander_oui_non, demander_texte

NOUVEAU_JOUEUR = "nouveau"
GENRES = {"h": "Homme", "f": "Femme"}


def demander_identifiant_joueur():
    return demander_identifiant("\nIdentifiant national d'échecs (ex. AB12345) : ")


def demander_infos_joueur():
    """Renvoie les champs d'un nouveau joueur, hors identifiant."""
    prenom = demander_texte("Prénom : ")
    nom = demander_texte("Nom de famille : ")
    genre = input("Genre (h/f) : ").strip().lower()
    while genre not in GENRES:
        afficher_erreur("répondez par « h » (homme) ou « f » (femme).")
        genre = input("Genre (h/f) : ").strip().lower()
    date_naissance = demander_date("Date de naissance (jj/mm/aaaa) : ", maximum=date.today())
    return {"prenom": prenom, "nom": nom, "genre": genre, "date_naissance": date_naissance}


def confirmer_ajout(joueur):
    print(f"\n{joueur.nom_complet} ({joueur.identifiant}), né(e) le {formater_date(joueur.date_naissance)}")
    return demander_oui_non("Confirmez-vous l'ajout de ce joueur ?")


def afficher_joueurs(joueurs, titre):
    """Liste de joueurs, dans l'ordre fourni."""
    afficher_titre(titre)
    afficher_tableau(
        ["Nom", "Prénom", "Identifiant", "Genre", "Date de naissance"],
        [
            [joueur.nom, joueur.prenom, joueur.identifiant, GENRES[joueur.genre],
             formater_date(joueur.date_naissance)]
            for joueur in joueurs
        ],
    )


def choisir_joueur_a_inscrire(joueurs_disponibles, nombre_inscrits):
    """Renvoie un joueur du club, NOUVEAU_JOUEUR ou None pour terminer."""
    options = [f"{joueur.nom} {joueur.prenom} ({joueur.identifiant})" for joueur in joueurs_disponibles]
    options += ["Créer un nouveau joueur dans le club", "Terminer les inscriptions"]
    titre = f"Joueurs inscrits : {nombre_inscrits}. Choisissez un joueur du club à inscrire :"
    index = demander_choix(options, titre)
    if index < len(joueurs_disponibles):
        return joueurs_disponibles[index]
    if index == len(joueurs_disponibles):
        return NOUVEAU_JOUEUR
    return None
