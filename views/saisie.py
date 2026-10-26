"""Saisies au clavier, toujours validées avant d'être renvoyées."""

from datetime import datetime

from models.joueur import Joueur
from views.commun import FORMAT_DATE, afficher_erreur, formater_date

REPONSES_OUI = ("o", "oui", "y", "yes")
REPONSES_NON = ("n", "non", "no")


def demander_texte(message):
    """Texte obligatoire."""
    while True:
        texte = input(message).strip()
        if texte:
            return texte
        afficher_erreur("ce champ est obligatoire.")


def demander_texte_facultatif(message, defaut=""):
    return input(message).strip() or defaut


def demander_date(message, minimum=None, maximum=None):
    """Date au format jj/mm/aaaa, éventuellement bornée."""
    while True:
        saisie = input(message).strip()
        try:
            valeur = datetime.strptime(saisie, FORMAT_DATE).date()
        except ValueError:
            afficher_erreur("date invalide, utilisez le format jj/mm/aaaa.")
            continue
        if minimum is not None and valeur < minimum:
            afficher_erreur(f"la date doit être postérieure ou égale au {formater_date(minimum)}.")
        elif maximum is not None and valeur > maximum:
            afficher_erreur(f"la date doit être antérieure ou égale au {formater_date(maximum)}.")
        else:
            return valeur


def demander_entier(message, minimum, maximum=None, defaut=None):
    """Nombre entier ; une saisie vide renvoie `defaut` s'il est fourni."""
    while True:
        saisie = input(message).strip()
        if not saisie and defaut is not None:
            return defaut
        try:
            valeur = int(saisie)
        except ValueError:
            valeur = None
        if valeur is not None and valeur >= minimum and (maximum is None or valeur <= maximum):
            return valeur
        borne = f"entre {minimum} et {maximum}" if maximum is not None else f"supérieur ou égal à {minimum}"
        afficher_erreur(f"veuillez entrer un nombre {borne}.")


def demander_oui_non(message):
    while True:
        reponse = input(f"{message} (o/n) : ").strip().lower()
        if reponse in REPONSES_OUI:
            return True
        if reponse in REPONSES_NON:
            return False
        afficher_erreur("répondez par « o » (oui) ou « n » (non).")


def demander_choix(options, titre=None):
    """Affiche une liste numérotée et renvoie l'indice (à partir de 0) de l'option choisie."""
    if titre:
        print(f"\n{titre}\n")
    for numero, option in enumerate(options, start=1):
        print(f"{numero}. {option}")
    return demander_entier("\nVotre choix : ", 1, len(options)) - 1


def demander_identifiant(message):
    """Identifiant national d'échecs : deux lettres et cinq chiffres (ex. AB12345)."""
    while True:
        identifiant = input(message).strip().upper()
        if Joueur.identifiant_valide(identifiant):
            return identifiant
        afficher_erreur("l'identifiant doit comporter deux lettres suivies de cinq chiffres (ex. AB12345).")
