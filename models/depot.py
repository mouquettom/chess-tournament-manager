"""Sauvegarde et chargement des données au format JSON."""

import json
import os
import re
import unicodedata
from pathlib import Path

from models.joueur import Joueur
from models.tournoi import Tournoi

DOSSIER_DONNEES = Path(__file__).resolve().parent.parent / "data"


def _ecrire_json(chemin, donnees):
    """Écrit d'abord dans un fichier temporaire pour ne jamais laisser un fichier à moitié écrit."""
    chemin.parent.mkdir(parents=True, exist_ok=True)
    temporaire = chemin.with_name(chemin.name + ".tmp")
    with open(temporaire, "w", encoding="utf-8") as fichier:
        json.dump(donnees, fichier, ensure_ascii=False, indent=4)
    os.replace(temporaire, chemin)


def _nom_de_fichier(texte):
    """« Open de Paris 2025 » -> « open_de_paris_2025 »."""
    decompose = unicodedata.normalize("NFKD", texte)
    ascii_seul = decompose.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "_", ascii_seul.lower()).strip("_") or "tournoi"


class DepotJoueurs:
    """Base des joueurs du club, indépendante des tournois (data/joueurs.json)."""

    def __init__(self, dossier=DOSSIER_DONNEES):
        self.chemin = Path(dossier) / "joueurs.json"

    def charger(self):
        """Renvoie un dictionnaire {identifiant: Joueur}."""
        if not self.chemin.exists():
            return {}
        with open(self.chemin, encoding="utf-8") as fichier:
            donnees = json.load(fichier)
        joueurs = (Joueur.depuis_dict(joueur) for joueur in donnees["joueurs"])
        return {joueur.identifiant: joueur for joueur in joueurs}

    def sauvegarder(self, joueurs):
        tries = sorted(joueurs.values(), key=Joueur.cle_tri)
        _ecrire_json(self.chemin, {"joueurs": [joueur.vers_dict() for joueur in tries]})


class DepotTournois:
    """Un fichier JSON par tournoi dans data/tournois/."""

    def __init__(self, dossier=DOSSIER_DONNEES):
        self.dossier = Path(dossier) / "tournois"
        # Fichiers ignorés lors du dernier appel à lister() car illisibles.
        self.fichiers_illisibles = []

    def lister(self):
        """Renvoie tous les tournois enregistrés, du plus ancien au plus récent."""
        self.fichiers_illisibles = []
        if not self.dossier.exists():
            return []
        tournois = []
        for chemin in sorted(self.dossier.glob("*.json")):
            try:
                with open(chemin, encoding="utf-8") as fichier:
                    tournois.append(Tournoi.depuis_dict(json.load(fichier), fichier=chemin.name))
            except (OSError, ValueError, KeyError, TypeError):
                self.fichiers_illisibles.append(chemin.name)
        return sorted(tournois, key=lambda tournoi: (tournoi.date_debut, tournoi.nom))

    def sauvegarder(self, tournoi):
        if tournoi.fichier is None:
            tournoi.fichier = self._nouveau_nom_de_fichier(tournoi)
        _ecrire_json(self.dossier / tournoi.fichier, tournoi.vers_dict())

    def _nouveau_nom_de_fichier(self, tournoi):
        """Nom unique : deux tournois du même nom ne s'écrasent pas."""
        base = _nom_de_fichier(f"{tournoi.nom} {tournoi.date_debut.year}")
        nom, numero = f"{base}.json", 2
        while (self.dossier / nom).exists():
            nom, numero = f"{base}_{numero}.json", numero + 1
        return nom
