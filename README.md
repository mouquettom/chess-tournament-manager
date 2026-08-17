# Chess-Tournament-Manager

## Description

This program is an offline Python application for managing chess
tournaments. It allows users to add players, manage tournaments,
generate dynamic pairings based on match results, and produce detailed
reports.

Data is saved and loaded using JSON files.

------------------------------------------------------------------------

## Features

-   **Player Management:** Add players with their last name, first name,
    gender, and date of birth
-   **Tournament Management:** Create tournaments and manage rounds and
    matches
-   **Reports:** Generate lists of players, tournaments, rounds, and
    matches
-   **User Interface:** Interactive console-based menu

------------------------------------------------------------------------

## Prerequisites

-   Python 3.8 or later
-   Dependencies can optionally be installed with:

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## Installation and Usage

### 1. Clone the Repository

Open a terminal, navigate to the directory of your choice, and clone the
repository:

``` bash
git clone https://github.com/mouquettom/chess-tournament-manager.git
cd chess-tournament-manager
```

### 2. Create a Virtual Environment

``` bash
python -m venv env
```

### 3. Activate the Virtual Environment

#### Windows

``` bash
env\scripts\activate.bat
```

#### macOS / Linux

``` bash
source env/bin/activate
```

### 4. Run the Application

You can now run the program from the terminal:

``` bash
python3 main.py
```

------------------------------------------------------------------------

## PEP 8 Compliance

An HTML report generated with Flake8 is available in the
`rapport_flake8` directory.

------------------------------------------------------------------------

## MVC Architecture

The project follows the MVC architecture, which separates
responsibilities into three layers:

-   **Model:** manages data and business logic
-   **View:** displays data and handles user interactions
-   **Controller:** connects the Model and the View by processing user
    actions and updating the data or interface accordingly

### Main Files

-   `models.py`: defines the main classes (`Player`, `Match`,
    `Tournament`)
-   `views.py`: handles user interactions, including display and input
-   `controllers.py`: contains the business logic, such as tournament
    creation and player management
-   `main.py`: application entry point

------------------------------------------------------------------------

## Author

@tom_mouquet

Project developed as part of the OpenClassrooms **Développeur
d'application Python** training program.
