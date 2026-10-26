"""Fonctions d'affichage partagées par toutes les vues."""

FORMAT_DATE = "%d/%m/%Y"
FORMAT_DATE_HEURE = "%d/%m/%Y %H:%M"


def formater_date(valeur):
    return valeur.strftime(FORMAT_DATE)


def formater_date_heure(valeur):
    return valeur.strftime(FORMAT_DATE_HEURE) if valeur else "-"


def formater_points(points):
    """1.0 -> « 1 », 2.5 -> « 2.5 »."""
    return f"{points:g}"


def nom_joueur(identifiant, joueurs_du_club):
    """« Prénom Nom (AB12345) », même si le joueur a disparu de la base du club."""
    joueur = joueurs_du_club.get(identifiant)
    if joueur is None:
        return f"Joueur inconnu ({identifiant})"
    return f"{joueur.nom_complet} ({identifiant})"


def afficher_titre(titre):
    print(f"\n{titre}\n{'-' * len(titre)}")


def afficher_message(message):
    print(message)


def afficher_erreur(message):
    print(f"Erreur : {message}")


def afficher_tableau(entetes, lignes):
    """Affiche un tableau aligné en colonnes."""
    if not lignes:
        print("(aucune donnée)")
        return
    lignes = [[str(cellule) for cellule in ligne] for ligne in lignes]
    largeurs = [
        max(len(entete), *(len(ligne[colonne]) for ligne in lignes))
        for colonne, entete in enumerate(entetes)
    ]

    def formater(cellules):
        return "  ".join(cellule.ljust(largeur) for cellule, largeur in zip(cellules, largeurs)).rstrip()

    print(formater(entetes))
    print("  ".join("-" * largeur for largeur in largeurs))
    for ligne in lignes:
        print(formater(ligne))
