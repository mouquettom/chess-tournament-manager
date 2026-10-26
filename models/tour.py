"""Tour (round) d'un tournoi."""

from datetime import datetime

from models.match import Match


def maintenant():
    return datetime.now().replace(microsecond=0)


class Tour:
    """Tour nommé ("Round 1"...), horodaté au début et à la fin.

    `exempt` contient l'identifiant du joueur sans adversaire lorsque le
    nombre de joueurs est impair.
    """

    def __init__(self, nom, matchs=None, exempt=None, debut=None, fin=None):
        self.nom = nom
        self.matchs = matchs if matchs is not None else []
        self.exempt = exempt
        self.debut = debut if debut is not None else maintenant()
        self.fin = fin

    @property
    def est_termine(self):
        return self.fin is not None

    @property
    def matchs_a_jouer(self):
        return [match for match in self.matchs if not match.est_joue]

    def terminer(self):
        """Clôture le tour (date et heure de fin) une fois tous les résultats saisis."""
        if self.est_termine:
            raise ValueError(f"{self.nom} est déjà terminé.")
        if self.matchs_a_jouer:
            raise ValueError(f"Il reste des résultats à saisir pour {self.nom}.")
        self.fin = maintenant()

    def vers_dict(self):
        return {
            "nom": self.nom,
            "debut": self.debut.isoformat(),
            "fin": self.fin.isoformat() if self.fin else None,
            "exempt": self.exempt,
            "matchs": [match.vers_tuple() for match in self.matchs],
        }

    @classmethod
    def depuis_dict(cls, donnees):
        return cls(
            nom=donnees["nom"],
            matchs=[Match.depuis_tuple(match) for match in donnees["matchs"]],
            exempt=donnees.get("exempt"),
            debut=datetime.fromisoformat(donnees["debut"]),
            fin=datetime.fromisoformat(donnees["fin"]) if donnees.get("fin") else None,
        )
