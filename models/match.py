"""Match entre deux joueurs."""

VICTOIRE_JOUEUR1 = "victoire_joueur1"
VICTOIRE_JOUEUR2 = "victoire_joueur2"
MATCH_NUL = "nul"

SCORES = {
    VICTOIRE_JOUEUR1: (1.0, 0.0),
    VICTOIRE_JOUEUR2: (0.0, 1.0),
    MATCH_NUL: (0.5, 0.5),
}


class Match:
    """Match stocké sous la forme ([identifiant1, score1], [identifiant2, score2]).

    Les scores valent None tant que le résultat n'a pas été saisi.
    """

    def __init__(self, joueur1, joueur2, score1=None, score2=None):
        if joueur1 == joueur2:
            raise ValueError("Un joueur ne peut pas se rencontrer lui-même.")
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.score1 = score1
        self.score2 = score2

    @property
    def est_joue(self):
        return self.score1 is not None

    @property
    def joueurs(self):
        return self.joueur1, self.joueur2

    def enregistrer_resultat(self, resultat):
        if resultat not in SCORES:
            raise ValueError(f"Résultat inconnu : {resultat!r}.")
        self.score1, self.score2 = SCORES[resultat]

    def vers_tuple(self):
        return [self.joueur1, self.score1], [self.joueur2, self.score2]

    @classmethod
    def depuis_tuple(cls, donnees):
        (joueur1, score1), (joueur2, score2) = donnees
        return cls(joueur1, joueur2, score1, score2)

    def __repr__(self):
        return f"Match({self.vers_tuple()})"
