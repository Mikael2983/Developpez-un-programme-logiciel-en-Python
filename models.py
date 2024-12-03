import random
import json
import os
import re
from datetime import date


class Player:
    """un joueur"""

    def __init__(self, national_player_number, name, first_name, birthday, score=0):
        """Initialise le nom, le prénom et la darte de naissance"""
        self.name = validate_name(name)
        self.first_name = validate_name(first_name)
        self.birthday = validate_birthday(birthday)
        self.national_player_number = validate_national_player_number(national_player_number)
        self.score = score

    def __repr__(self) -> str:
        return (f"{self.national_player_number:<12} {self.name:<15} {self.first_name:<15} "
                f"{self.birthday:<12} {self.score:<6}")


def validate_name(name: str) -> str:
    """
    Valide et transforme un nom ou prénom.
    Si possible, corrige automatiquement les erreurs (ex. 'dupont' -> 'Dupont').
    """
    try:
        if re.match(r"^[a-zA-ZÀ-ÖØ-öø-ÿ-]+$", name, re.UNICODE):
            return name.title()  # Corrige en "Majuscule initiale"
        raise ValueError(f"Le nom '{name}' contient des caractères non valides.")
    except ValueError as e:
        print(e)
        corrected = input("Veuillez entrer un nom valide.")
        return validate_name(corrected)  # Revalide la nouvelle entrée


def validate_national_player_number(national_player_number: str) -> str:
    """
    Valide le numéro de joueur national.
    Si invalide, demande une correction utilisateur.
    """
    player_number = national_player_number.lower()
    try:
        if re.match(r"^[a-z]{2}\d{5}$", player_number):
            return player_number
        raise ValueError(
            f"Le numéro '{national_player_number}' n'est pas valide."
            "Il doit être sous la forme de deux lettres minuscules suivies de 5 chiffres."
        )
    except ValueError as e:
        print(e)
        corrected = input("Veuillez entrer un numéro valide. ex: aa11111 :")
        return validate_national_player_number(corrected)  # Revalide la nouvelle entrée


def validate_birthday(birthday: str) -> str | None:
    """
    Valide la date de naissance et corrige son format si nécessaire.
    Demande une intervention utilisateur en cas d'erreur.
    """
    try:
        if "-" or "/" in birthday:
            if "-" in birthday:
                day, month, year = birthday.split('-')
            else:
                day, month, year = birthday.split('/')

            day = day.zfill(2)
            month = month.zfill(2)
            if len(year) == 2:
                year = int(year)
                if year > 25:
                    year = f"19{year}"
                elif 0 < year < 9:
                    year = f"200{year}"
                else:
                    year = f"20{year}"
            birthday = f"{day}/{month}/{year}"
        return birthday

    except ValueError as e:
        print(e)
        corrected = input("Veuillez entrer une date valide. ex: dd/mm/aaaa : ")
        return validate_birthday(corrected)


class Tournament:
    """un tournoi"""

    def __init__(self, name, place, description="", max_round=4):
        """Initialise le tournoi"""
        self.name = name
        self.place = place
        self.start_date = date.today()
        self.end_date = date.today()
        self.round_number = 0
        self.max_round = int(max_round)
        self.players = []
        self.rounds = []
        self.description = description

    def add_player(self, player_number):
        """ajoute un participant au tournoi"""

        json_file = "data/players.json"
        check_existence_json_file(json_file)

        found_player = find_player_in_json(player_number)

        if found_player:
            player = Player(found_player["national_player_number"], found_player["name"],
                            found_player["first_name"], found_player["birthday"])
            self.players.append(player)
            return player
        else:
            return

    def add_round(self):
        """Add a round to a tournament"""
        self.rounds.append(Round(len(self.rounds) + 1, self.players, self.rounds))
        return


class Round:
    """un tour"""

    def __init__(self, round_number: int, players: list, rounds: list):
        """initialise un tour"""
        self.name = f"round {round_number}"
        self.round_number = round_number
        self.match_result = []
        self.rounds = rounds
        self.ended = False
        if self.round_number == 1:
            random.shuffle(players)
            self.players = players
        else:
            self.players = sorted(players, key=lambda player: player.score, reverse=True)
        self.matchs = self.add_match()

    def add_match(self):
        """ add match to round"""
        self.matchs = []
        used_players = set()
        match_number = 1
        for i, player1 in enumerate(self.players):
            if player1 in used_players:
                continue

            for j in range(i + 1, len(self.players)):
                player2 = self.players[j]
                if player2 in used_players:
                    continue

                match = Match(match_number, (player1, player2))

                already_played = False
                for previous_round in self.rounds:
                    for previous_match in previous_round.matchs:
                        if ((match.player1, match.player2) == (previous_match.player1, previous_match.player2)
                                or (match.player2, match.player1) == (previous_match.player1, previous_match.player2)):
                            already_played = True
                            break

                if not already_played:
                    self.matchs.append(match)
                    match_number += 1
                    used_players.add(player1)
                    used_players.add(player2)
                    break
        return self.matchs


class Match:
    """un match"""

    def __init__(self, match_number, players):
        """initialise un match"""
        self.number = int(match_number)
        self.player1 = players[0]
        self.player2 = players[1]
        self.result = [(self.player1, 0), (self.player2, 0)]

    def assign_result(self, gagnant="match nul"):
        """define the winner of the match"""
        if gagnant == self.player1:
            self.player1.score += 1
            return [(self.player1, 1), (self.player2, 0)]

        elif gagnant == self.player2:
            self.player2.score += 1
            return [(self.player1, 0), (self.player2, 1)]

        else:
            self.player1.score += .5
            self.player2.score += .5
            return [(self.player1, 0.5), (self.player2, 0.5)]


def check_existence_json_file(path):
    """Check the existence of the Json file"""
    json_file = path

    if not os.path.exists(json_file):
        with open(json_file, "w", encoding="utf-8") as file:
            json.dump([], file)


def find_player_in_json(player_number: str):
    """search a player by his national number in one Json file

    :param player_number: national player number.
    :return: Player data dictionary or None.
    """
    json_file = "data/players.json"
    check_existence_json_file(json_file)

    found_player = None
    with open(json_file, "r", encoding="utf-8") as file:
        try:
            players_data = json.load(file)
            for data in players_data:
                if data["national_player_number"] == player_number:
                    found_player = data
                    break
        except json.JSONDecodeError:
            print("Le fichier JSON est mal formaté.")
    return found_player


def write_new_player_in_json(player):
    """Write a new player in the Json file

    :param player: instances de Player.
    """

    json_file = "data/players.json"
    data = {"national_player_number": player.national_player_number, "name": player.name,
            "first_name": player.first_name, "birthday": player.birthday, "score": player.score
            }
    if not os.path.exists(json_file):
        with open(json_file, "w", encoding="utf-8") as file:
            json.dump([], file)

    with open(json_file, "r", encoding="utf-8") as file:
        players_data = json.load(file)

    players_data.append(data)

    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(players_data, file, indent=4, ensure_ascii=False)

    return


def sort_by_name(player):
    """Retourne la clé de tri pour le nom."""
    return player.name


def sort_by_npn(player):
    """Retourne la clé de tri pour le numéro national."""
    return player.national_player_number


def sort_by_score(player):
    """Retourne la clé de tri pour le score."""
    return player.score


def sort_players(players, criterion="name", reverse=False):
    """
    Trie une liste de joueurs selon un critère donné.

    :param players: Liste d'instances de Player.
    :param criterion: Critère de tri, parmi "name", "national_player_number", "score".
    :param reverse: Si True, tri en ordre décroissant.
    :return: Liste triée de joueurs.
    """
    sort_functions = {
        "name": sort_by_name,
        "national_player_number": sort_by_npn,
        "score": sort_by_score,
    }

    if criterion not in sort_functions:
        raise ValueError("Critère invalide. Utilisez 'name', 'national_player_number' ou 'score'.")

    return sorted(players, key=sort_functions[criterion], reverse=reverse)
