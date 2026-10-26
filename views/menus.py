"""Menus de l'application. Chaque menu renvoie une clé, jamais un libellé."""

from views.saisie import demander_choix


def _choisir(titre, options):
    cles = [cle for cle, _ in options]
    libelles = [libelle for _, libelle in options]
    return cles[demander_choix(libelles, titre)]


def afficher_bienvenue():
    print("\n*** GESTIONNAIRE DE TOURNOIS D'ÉCHECS ***")


def afficher_au_revoir():
    print("\nAu revoir !")


def menu_principal():
    return _choisir("Menu principal :", [
        ("joueurs", "Joueurs du club"),
        ("creer_tournoi", "Créer un tournoi"),
        ("ouvrir_tournoi", "Ouvrir un tournoi"),
        ("rapports", "Rapports"),
        ("quitter", "Quitter"),
    ])


def menu_joueurs():
    return _choisir("Joueurs du club :", [
        ("ajouter", "Ajouter un joueur"),
        ("lister", "Liste des joueurs"),
        ("retour", "Retour"),
    ])


def menu_tournoi(tournoi):
    """Les options proposées dépendent de l'avancement du tournoi."""
    options = []
    if not tournoi.est_commence:
        options.append(("inscrire", "Inscrire des joueurs"))
    if tournoi.tour_en_cours is not None:
        options.append(("jouer", f"Saisir les résultats du {tournoi.tour_en_cours.nom}"))
    elif not tournoi.est_termine:
        options.append(("jouer", f"Lancer le Round {tournoi.numero_tour_actuel + 1}"))
    options += [
        ("classement", "Classement"),
        ("description", "Modifier la description"),
        ("retour", "Retour au menu principal"),
    ]
    return _choisir("Que souhaitez-vous faire ?", options)


def menu_rapports():
    return _choisir("Rapports :", [
        ("joueurs_club", "Liste de tous les joueurs du club (ordre alphabétique)"),
        ("tournois", "Liste de tous les tournois"),
        ("nom_et_dates", "Nom et dates d'un tournoi"),
        ("joueurs_tournoi", "Joueurs d'un tournoi (ordre alphabétique)"),
        ("tours_et_matchs", "Tours et matchs d'un tournoi"),
        ("retour", "Retour"),
    ])
