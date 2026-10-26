"""Tournoi et génération des appariements."""

import random
from datetime import date

from models.match import Match
from models.tour import Tour

NOMBRE_TOURS_PAR_DEFAUT = 4
POINTS_EXEMPT = 1.0
# Au-delà de ce nombre d'essais, la recherche d'appariements sans revanche s'arrête.
LIMITE_RECHERCHE = 100_000


class Tournoi:
    """Tournoi d'échecs : joueurs inscrits (identifiants) et tours successifs."""

    def __init__(self, nom, lieu, date_debut, date_fin, description="",
                 nombre_tours=NOMBRE_TOURS_PAR_DEFAUT, joueurs=None, tours=None, fichier=None):
        if not nom.strip() or not lieu.strip():
            raise ValueError("Le nom et le lieu du tournoi sont obligatoires.")
        if date_fin < date_debut:
            raise ValueError("La date de fin ne peut pas précéder la date de début.")
        if nombre_tours < 1:
            raise ValueError("Le tournoi doit compter au moins un tour.")
        self.nom = nom.strip()
        self.lieu = lieu.strip()
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.description = description
        self.nombre_tours = nombre_tours
        self.joueurs = joueurs if joueurs is not None else []
        self.tours = tours if tours is not None else []
        # Nom du fichier de sauvegarde, attribué par DepotTournois.
        self.fichier = fichier

    # --- État du tournoi -------------------------------------------------

    @property
    def numero_tour_actuel(self):
        return len(self.tours)

    @property
    def est_commence(self):
        return bool(self.tours)

    @property
    def tour_en_cours(self):
        """Dernier tour s'il n'est pas encore terminé, sinon None."""
        if self.tours and not self.tours[-1].est_termine:
            return self.tours[-1]
        return None

    @property
    def est_termine(self):
        return self.numero_tour_actuel >= self.nombre_tours and self.tour_en_cours is None

    # --- Joueurs et points -----------------------------------------------

    def inscrire_joueur(self, identifiant):
        if self.est_commence:
            raise ValueError("Impossible d'inscrire un joueur : le tournoi a déjà commencé.")
        if identifiant in self.joueurs:
            raise ValueError(f"Le joueur {identifiant} est déjà inscrit.")
        self.joueurs.append(identifiant)

    def points(self):
        """Points de chaque joueur, recalculés à partir des résultats enregistrés."""
        points = {identifiant: 0.0 for identifiant in self.joueurs}
        for tour in self.tours:
            if tour.exempt is not None:
                points[tour.exempt] += POINTS_EXEMPT
            for match in tour.matchs:
                if match.est_joue:
                    points[match.joueur1] += match.score1
                    points[match.joueur2] += match.score2
        return points

    def paires_deja_jouees(self, avant=None):
        """Ensemble des paires {joueur1, joueur2} déjà opposées (avant le tour `avant` si fourni)."""
        tours = self.tours if avant is None else self.tours[:self.tours.index(avant)]
        return {frozenset(match.joueurs) for tour in tours for match in tour.matchs}

    def revanches(self, tour):
        """Matchs du tour qui opposent deux joueurs s'étant déjà rencontrés."""
        deja_jouees = self.paires_deja_jouees(avant=tour)
        return [match for match in tour.matchs if frozenset(match.joueurs) in deja_jouees]

    # --- Déroulement -----------------------------------------------------

    def demarrer_tour_suivant(self):
        """Crée le tour suivant avec ses appariements et le renvoie."""
        if self.tour_en_cours is not None:
            raise ValueError(f"{self.tour_en_cours.nom} n'est pas encore terminé.")
        if self.est_termine:
            raise ValueError("Le tournoi est terminé.")
        if len(self.joueurs) < 2:
            raise ValueError("Il faut au moins deux joueurs inscrits pour lancer un tour.")
        paires, exempt = self._generer_appariements()
        tour = Tour(
            nom=f"Round {self.numero_tour_actuel + 1}",
            matchs=[Match(joueur1, joueur2) for joueur1, joueur2 in paires],
            exempt=exempt,
        )
        self.tours.append(tour)
        return tour

    def _ordre_d_appariement(self):
        """Premier tour : ordre aléatoire. Tours suivants : points décroissants,
        les égalités étant départagées au hasard (mélange puis tri stable)."""
        joueurs = list(self.joueurs)
        random.shuffle(joueurs)
        if self.est_commence:
            points = self.points()
            joueurs.sort(key=lambda identifiant: points[identifiant], reverse=True)
        return joueurs

    def _generer_appariements(self):
        joueurs = self._ordre_d_appariement()
        deja_jouees = self.paires_deja_jouees()

        if len(joueurs) % 2 == 0:
            candidats_exempt = [None]
        else:
            # Le moins bien classé n'ayant jamais été exempté passe son tour en priorité.
            deja_exemptes = {tour.exempt for tour in self.tours}
            candidats_exempt = [j for j in reversed(joueurs) if j not in deja_exemptes]
            candidats_exempt += [j for j in reversed(joueurs) if j in deja_exemptes]

        for exempt in candidats_exempt:
            restants = [j for j in joueurs if j != exempt]
            paires = _apparier_sans_revanche(restants, deja_jouees, [LIMITE_RECHERCHE])
            if paires is not None:
                return paires, exempt

        # Aucun appariement sans revanche n'existe : on en limite le nombre.
        exempt = candidats_exempt[0]
        restants = [j for j in joueurs if j != exempt]
        return _apparier_au_mieux(restants, deja_jouees), exempt

    # --- Sérialisation ---------------------------------------------------

    def vers_dict(self):
        return {
            "nom": self.nom,
            "lieu": self.lieu,
            "date_debut": self.date_debut.isoformat(),
            "date_fin": self.date_fin.isoformat(),
            "description": self.description,
            "nombre_tours": self.nombre_tours,
            "numero_tour_actuel": self.numero_tour_actuel,
            "joueurs": list(self.joueurs),
            "tours": [tour.vers_dict() for tour in self.tours],
        }

    @classmethod
    def depuis_dict(cls, donnees, fichier=None):
        return cls(
            nom=donnees["nom"],
            lieu=donnees["lieu"],
            date_debut=date.fromisoformat(donnees["date_debut"]),
            date_fin=date.fromisoformat(donnees["date_fin"]),
            description=donnees.get("description", ""),
            nombre_tours=donnees.get("nombre_tours", NOMBRE_TOURS_PAR_DEFAUT),
            joueurs=list(donnees["joueurs"]),
            tours=[Tour.depuis_dict(tour) for tour in donnees["tours"]],
            fichier=fichier,
        )

    def __repr__(self):
        return f"Tournoi({self.nom!r}, {self.numero_tour_actuel}/{self.nombre_tours} tours)"


def _apparier_sans_revanche(joueurs, deja_jouees, budget):
    """Apparie les joueurs dans l'ordre donné en évitant les paires déjà jouées.

    Le premier joueur affronte le suivant qu'il n'a pas encore rencontré ; si cela
    bloque la suite, on essaie l'adversaire d'après (retour sur trace).
    Renvoie None si c'est impossible ou si le budget d'essais est épuisé.
    """
    if not joueurs:
        return []
    premier, autres = joueurs[0], joueurs[1:]
    for index, adversaire in enumerate(autres):
        budget[0] -= 1
        if budget[0] < 0:
            return None
        if frozenset((premier, adversaire)) in deja_jouees:
            continue
        suite = _apparier_sans_revanche(autres[:index] + autres[index + 1:], deja_jouees, budget)
        if suite is not None:
            return [(premier, adversaire)] + suite
    return None


def _apparier_au_mieux(joueurs, deja_jouees):
    """Chaque joueur affronte le premier adversaire qu'il n'a pas rencontré, sinon le suivant."""
    restants = list(joueurs)
    paires = []
    while len(restants) >= 2:
        premier = restants.pop(0)
        inedits = [j for j in restants if frozenset((premier, j)) not in deja_jouees]
        adversaire = inedits[0] if inedits else restants[0]
        restants.remove(adversaire)
        paires.append((premier, adversaire))
    return paires
