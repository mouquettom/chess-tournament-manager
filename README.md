# Chess-Tournament-Manager

## Description

An offline console application, written in Python, for running chess
tournaments: it keeps the club's player database, creates tournaments,
generates the pairings for each round, records the results and produces
reports.

The interface is in French. All data is stored in JSON files and saved
automatically after every action, so a tournament can be interrupted and
resumed at any time.

------------------------------------------------------------------------

## Features

-   **Club players:** add players with their national chess ID (two
    letters followed by five digits, e.g. `AB12345`), last name, first
    name, gender and date of birth. The player database is shared by all
    tournaments.
-   **Tournaments:** name, location, start and end dates, number of
    rounds (4 by default) and a description for the director's remarks.
    Players are registered from the club database, or created on the fly.
-   **Rounds:** each round is named (`Round 1`, `Round 2`, ...) and its
    start and end date and time are recorded automatically. Results are
    entered match by match (win, loss or draw).
-   **Pairings:**
    -   round 1: players are shuffled at random;
    -   following rounds: players are sorted by points (ties broken at
        random) and paired in that order, avoiding players who have
        already met whenever possible;
    -   odd number of players: one player sits out each round and gets
        1 point (the lowest-ranked player who has not yet sat out).
-   **Scoring:** 1 point for a win, 0.5 for a draw, 0 for a loss.
-   **Reports:**
    -   all club players, in alphabetical order;
    -   all tournaments;
    -   name and dates of a given tournament;
    -   players of a given tournament, in alphabetical order;
    -   all rounds of a given tournament and all matches of each round.

------------------------------------------------------------------------

## Prerequisites

-   Python 3.8 or later (tested from 3.8 to 3.13)
-   No third-party package is needed to run the application. The
    packages listed in `requirements.txt` are only used to check PEP 8
    compliance (see below).

------------------------------------------------------------------------

## Installation and Usage

### 1. Clone the repository

``` bash
git clone https://github.com/mouquettom/chess-tournament-manager.git
cd chess-tournament-manager
```

### 2. Create a virtual environment

``` bash
python -m venv env
```

### 3. Activate the virtual environment

#### Windows (Command Prompt)

``` bash
env\Scripts\activate.bat
```

#### Windows (PowerShell)

``` bash
env\Scripts\Activate.ps1
```

#### macOS / Linux

``` bash
source env/bin/activate
```

### 4. Run the application

``` bash
python main.py
```

(Use `python3 main.py` on macOS / Linux if `python` points to Python 2.)

------------------------------------------------------------------------

## Data

The `data/` folder is created next to `main.py` the first time something
is saved:

-   `data/joueurs.json`: the club's players;
-   `data/tournois/<name>_<year>.json`: one file per tournament, with
    its registered players (by ID), its rounds and every match stored as
    `[["AB12345", 1.0], ["CD67890", 0.0]]`.

Dates are stored in ISO format (`2025-01-31`) and displayed as
`31/01/2025`. The `data/` folder is excluded from Git.

------------------------------------------------------------------------

## Tests

``` bash
python -m unittest
```

------------------------------------------------------------------------

## PEP 8 Compliance

The flake8 configuration is in `.flake8` (maximum line length: 119).

``` bash
pip install -r requirements.txt
flake8
```

To generate the HTML report in the `rapport_flake8` folder:

``` bash
flake8 --format=html --htmldir=rapport_flake8
```

------------------------------------------------------------------------

## MVC Architecture

The project follows the Model-View-Controller pattern:

-   **Models** (`models/`): data and business rules, with no keyboard
    input or display.
    -   `joueur.py`: `Joueur` (club player)
    -   `match.py`: `Match`
    -   `tour.py`: `Tour` (round)
    -   `tournoi.py`: `Tournoi` and the pairing algorithm
    -   `depot.py`: saving and loading the JSON files
-   **Views** (`views/`): every prompt and every display.
    -   `saisie.py`: validated keyboard input
    -   `menus.py`: menus
    -   `joueurs.py`, `tournois.py`, `rapports.py`: screens and reports
-   **Controllers** (`controllers/`): connect the views and the models.
    -   `application.py`: loading the data and main menu
    -   `joueurs.py`, `tournois.py`, `rapports.py`
-   `main.py`: application entry point.
-   `tests/`: unit tests.

------------------------------------------------------------------------

## Author

@tom_mouquet

Project developed as part of the OpenClassrooms **Développeur
d'application Python** training program.
