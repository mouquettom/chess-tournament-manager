"""Joueur inscrit au club."""

import re
import unicodedata
from datetime import date

FORMAT_IDENTIFIANT = re.compile(r"^[A-Z]{2}\d{5}$")
GENRES = ("h", "f")


def cle_alphabetique(texte):
    """Clé de tri insensible à la casse et aux accents ("Émile" se range avec "Emile")."""
    decompose = unicodedata.normalize("NFKD", texte)
    sans_accents = "".join(c for c in decompose if not unicodedata.combining(c))
    return sans_accents.casefold()


class Joueur:
    """Joueur du club, identifié par son identifiant national d'échecs (ex. AB12345)."""

    def __init__(self, identifiant, nom, prenom, date_naissance, genre):
        if not Joueur.identifiant_valide(identifiant):
            raise ValueError(f"Identifiant invalide : {identifiant!r} (format attendu : AB12345).")
        if not nom.strip() or not prenom.strip():
            raise ValueError("Le nom et le prénom sont obligatoires.")
        if genre not in GENRES:
            raise ValueError(f"Genre invalide : {genre!r} (attendu : 'h' ou 'f').")
        if date_naissance > date.today():
            raise ValueError("La date de naissance ne peut pas être dans le futur.")
        self.identifiant = identifiant
        self.nom = nom.strip()
        self.prenom = prenom.strip()
        self.date_naissance = date_naissance
        self.genre = genre

    @staticmethod
    def identifiant_valide(identifiant):
        return bool(FORMAT_IDENTIFIANT.match(identifiant))

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"

    def cle_tri(self):
        """Ordre alphabétique : nom de famille, puis prénom."""
        return cle_alphabetique(self.nom), cle_alphabetique(self.prenom)

    def vers_dict(self):
        return {
            "identifiant": self.identifiant,
            "nom": self.nom,
            "prenom": self.prenom,
            "date_naissance": self.date_naissance.isoformat(),
            "genre": self.genre,
        }

    @classmethod
    def depuis_dict(cls, donnees):
        return cls(
            identifiant=donnees["identifiant"],
            nom=donnees["nom"],
            prenom=donnees["prenom"],
            date_naissance=date.fromisoformat(donnees["date_naissance"]),
            genre=donnees["genre"],
        )

    def __repr__(self):
        return f"Joueur({self.identifiant}, {self.nom_complet})"
