# Gestion de Tournois d'Échecs

## Description

Cette application Python permet de gérer les tournois d'échecs de manière autonome et hors ligne. Elle est conçue pour répondre aux besoins des clubs d'échecs locaux, en leur offrant une solution simple pour organiser des tournois, suivre les résultats et gérer les joueurs.

L'application respecte le modèle de conception Modèle-Vue-Contrôleur (MVC) pour garantir une structure maintenable et extensible.

## Fonctionnalités

- Gestion des joueurs avec stockage des informations dans un fichier JSON.
- Organisation et gestion des tournois incluant :
  - Enregistrement des joueurs.
  - Génération des tours et des appariements selon les scores.
  - Calcul des scores à la fin de chaque tour.
- Sauvegarde et chargement des données des joueurs et des tournois.
- Génération de rapports tels que :
    - Liste des joueurs (par ordre alphabétique ou par numéro de joueur).
    - Liste des tournois avec leurs détails.
    - Résultats d’un tournoi (par tours et matchs).

Fonctionnalités d’export ultérieur prévues pour les rapports.

## Prérequis

Python 3.x

Modules Python listés dans requirements.txt

## Installation

1. Clonez ce repository sur votre machine locale :
   ```bash
   git clone https://github.com/Mikael2983/Developpez-un-programme-logiciel-en-Python.git

2. Accédez au dossier du projet :
   ```bash
   cd '04-Développer un programme logiciel en python'

3. Créez et activez un environnement virtuel (recommandé) :
   ```bash
    python -m venv env
    source env/bin/activate  # Sur Windows : env\Scripts\activate

4. Installez les dépendances requises :
   ```bash
   pip install -r requirements.txt

5. Lancez le programme :
   ```bash
   python main.py

## Structure des Données

- Joueurs : Stockés dans un fichier JSON, chaque joueur contient :
  - Nom de famille
  - Prénom
  - Date de naissance
  - Identifiant national d’échecs


- Tournois : Également stockés en JSON, chaque tournoi contient :
  - Nom, 
  - lieu, 
  - dates de début et fin
  - Nombre de tours (par défaut : 4)
  - Liste des joueurs inscrits
  - Liste des tours avec leurs matchs et scores

## Conventions de Codage

Style de code : Conforme à la PEP 8.
Vérification automatique : Utilisez flake8 pour analyser le code et générer un rapport avec flake8-html. 
Pour générer ce rapport :
   ```bash
   flake8 --format=html --htmldir=reports controllers.py models.py views.py main.py
```

## Fonctionnement

L'application propose un menu principal permettant d'accéder aux fonctionnalités principales :

- Gérer un tournoi
  - créer un tournoi
  - Gérer un tournoi existant (ajouter des tours, renseigner les résultats)
- Ajouter un joueur à la base de données
- Accéder à la basse de données
  - Afficher la liste des joueurs.
  - Consulter les rapports

## Limitations

L’application ne gère pas encore l’export des rapports.

Suppression des joueurs non implémentée.

## Contributions

Les contributions sont les bienvenues. Merci de soumettre une pull request avec une description claire des modifications proposées.

## Auteur

Développé par un développeur Python junior dans le cadre d'un projet d’amélioration des compétences en programmation orientée objet.


