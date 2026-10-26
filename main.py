"""Gestionnaire de tournois d'échecs hors ligne. Lancement : python main.py"""

from controllers.application import ApplicationController
from views import menus


def main():
    try:
        ApplicationController().lancer()
    except (KeyboardInterrupt, EOFError):
        # Les données sont sauvegardées après chaque action : rien n'est perdu.
        menus.afficher_au_revoir()


if __name__ == "__main__":
    main()
