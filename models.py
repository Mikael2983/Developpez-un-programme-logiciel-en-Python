import random
import json
import os
import re
from datetime import date
from typing import List


class Player:
    """un joueur"""

    def __init__(self, national_player_number, name, first_name, birthday, score=0):
        """Initializes a player's attributes, including their national player number, name, first name, birthday,
        and score.

        :param national_player_number: The unique national player number, validated to follow the format 'aa11111'.
        :type national_player_number: str
        :param name: The player's last name, validated and formatted with an initial capital letter.
        :type name: str
        :param first_name: The player's first name, validated and formatted with an initial capital letter.
        :type first_name: str
        :param birthday: The player's date of birth, validated and formatted in the format 'dd/mm/yyyy'.
        :type birthday: str
        :param score: The player's initial score, defaults to 0.
        :type score: int, optional
        """
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
    Validates and formats a given name or surname. Automatically corrects formatting
    errors when possible (e.g., 'dupont' -> 'Dupont').

    :param name: The name or surname to validate.
    :type name: str
    :raises ValueError: If the name contains invalid characters.
    :return: The validated and formatted name with the first letter capitalized.
    :rtype: str
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
    Validates the national player number format. Prompts the user for a correction
    if the input is invalid.

    :param national_player_number: The national player number to validate, expected in the format 'aa11111'.
    :type national_player_number: str
    :raises ValueError: If the input does not match the expected format (two lowercase letters followed by five digits).
    :return: The validated national player number in lowercase format.
    :rtype: str
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
    Validate and format a birthday string. Corrects the format if necessary
    and prompts the user for input in case of an error.

    :param birthday: The birthday string to validate, expected in the format 'dd-mm-yyyy' or 'dd/mm/yyyy'.
    :type birthday: str
    :raises ValueError: If the input birthday cannot be parsed or corrected.
    :return: The validated and formatted birthday string, in the format 'dd/mm/yyyy'.
    :rtype: str | None
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

    def __init__(self, name: str, place: str, description: str = "", max_round: int = 4):
        """Initializes a tournament with its details.

        :param name: The name of the tournament.
        :type name: str
        :param place: The location where the tournament is held.
        :type place: str
        :param description: A brief description of the tournament. Defaults to an empty string.
        :type description: str, optional
        :param max_round: The maximum number of rounds in the tournament. Defaults to 4.
        :type max_round: int, optional
        """
        self.name = name
        self.place = place
        self.start_date = date.today().isoformat()
        self.end_date = None
        self.round_number = 0
        self.max_round = int(max_round)
        self.players = []
        self.rounds = []
        self.description = description

    def add_player(self, player_number: str):
        """
        Adds a participant to the tournament.

        :param player_number: The national player number of the player to add.
        :type player_number: str
        :return: The `Player` object if the player was successfully added or already exists in the tournament,
                 `False` if the player was not found in the JSON file.
        :rtype: Player or boolean

        """

        json_file = "data/players.json"
        check_existence_json_file(json_file)

        found_player = find_player_in_json(player_number)

        if found_player:
            player = Player(found_player["national_player_number"], found_player["name"],
                            found_player["first_name"], found_player["birthday"])
            if player not in self.players:
                self.players.append(player)
                return player
            else:
                return player
        else:
            return False

    def add_round(self):
        """Add a round to a tournament"""
        self.round_number += 1
        self.rounds.append(Round(self.round_number, self.players))
        return

    def change_name(self, new_name: str):
        """changes the name of the tournament"""
        self.name = new_name

    def change_place(self, new_place: str):
        """changes the place of the tournament"""
        self.place = new_place

    def change_descritpion(self, new_description: str):
        """changes the description of the tournament"""
        self.description = new_description

    def change_max_round(self, new_max_round: str):
        """changes the description of the tournament"""
        self.max_round = new_max_round

    def ended(self):
        self.end_date = date.today().isoformat()

    def save(self):
        json_file = f"data/tournaments/{self.name}.json"
        check_existence_json_file(json_file)

        player_data = []
        for player in self.players:
            player_data.append({"national_player_number": player.national_player_number, "name": player.name,
                                "first_name": player.first_name, "birthday": player.birthday, "score": player.score})

        rounds_data = []
        for played_round in self.rounds:
            match_data = []
            for match in played_round.matchs:
                match_data.append({"match_number": match.number,
                                   "player1": {"national_player_number": match.player1.national_player_number,
                                               "name": match.player1.name, "first_name": match.player1.first_name,
                                               "birthday": match.player1.birthday, "score": match.player1.score},
                                   "player2": {"national_player_number": match.player2.national_player_number,
                                               "name": match.player2.name, "first_name": match.player2.first_name,
                                               "birthday": match.player2.birthday, "score": match.player2.score},
                                   "result": [("Payer1", match.result[0][1]), ("Player2", match.result[1][1])]})

            round_data = {"name": played_round.name, "round_number": played_round.round_number,
                          "ended": played_round.ended, "matchs": match_data}
            rounds_data.append(round_data)

        data = {"name": self.name, "place": self.place, "description": self.description,
                "start_date": self.start_date, "end_date": self.end_date,
                "round_number": self.round_number, "max_round": self.max_round, "players": player_data,
                "rounds": rounds_data
                }

        if not os.path.exists(json_file):
            with open(json_file, "w", encoding="utf-8") as file:
                json.dump([], file)

        with open(json_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        return

    def load(self, loaded_tournament):

        self.start_date = loaded_tournament["start_date"]
        self.end_date = loaded_tournament["end_date"]
        self.round_number = loaded_tournament["round_number"]
        self.max_round = loaded_tournament["max_round"]
        for player in loaded_tournament["players"]:
            self.players.append(Player(player["national_player_number"], player["name"], player["first_name"],
                                player["birthday"], player["score"]))

        for loaded_round in loaded_tournament["rounds"]:
            self.rounds.append(Round(loaded_round["round_number"], self.players))
            for played_match in loaded_round['matchs']:
                data = played_match["player1"]
                player1 = Player(data["national_player_number"], data["name"], data["first_name"],
                                 data["birthday"], data["score"])
                data = played_match["player2"]
                player2 = Player(data["national_player_number"], data["name"], data["first_name"],
                                 data["birthday"], data["score"])
                match = Match(played_match["match_number"], (player1, player2))
                if played_match["result"][0][1] == 1:
                    match.result = [(player1, 1), (player2, 0)]
                elif played_match["result"][1][1] == 1:
                    match.result = [(player1, 0), (player2, 1)]
                elif played_match["result"][1][1] == 0.5:
                    match.result = [(player1, 0.5), (player2, 0.5)]
                else:
                    match.result = [(player1, 0), (player2, 0)]

                self.rounds[-1].matchs.append(match)


class Round:
    """un tour"""

    def __init__(self, round_number: int, players: List[Player]):
        """
        Initializes a tournament round.

        :param round_number: The current round number.
        :type round_number: int
        :param players: A list of players participating in the round.
            - For the first round, players are shuffled randomly.
            - For the next rounds, players are sorted by their scores in descending order.
        :type players: list[Player]
        """
        self.name = f"round {round_number}"
        self.round_number = round_number
        self.ended = False
        if self.round_number == 1:
            random.shuffle(players)
            self.players = players
        else:
            self.players = sort_players(players, "score", True)
        self.matchs = []

    def add_match(self, rounds):
        """
        Adds matches to the current round based on available players.

        The method pairs players who have not yet played against each other in
        previous rounds. Each match is assigned a unique match number.
        :parameter rounds : list of the previous round
        :type rounds : list[Round]
        :return: A list of `Match` objects representing the matches for the round.
        :rtype: list[Match]
        """
        already_try = []
        while True:
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
                    for previous_round in rounds:
                        for previous_match in previous_round.matchs:
                            if ((match.player1, match.player2) == (previous_match.player1, previous_match.player2)
                                    or (match.player2, match.player1) ==
                                    (previous_match.player1, previous_match.player2)):
                                already_played = True
                                break

                    if not already_played and match not in already_try:
                        self.matchs.append(match)
                        match_number += 1
                        used_players.add(player1)
                        used_players.add(player2)
                        break
                    if match in already_try:
                        continue

            if len(self.matchs) != len(self.players) / 2:
                already_try = self.matchs
                self.players = sort_players(self.players, "score")
                continue
            else:
                break
        return


class Match:
    """un match"""

    def __init__(self, match_number, players):
        """
        Initializes a match with the given match number and players.

        :param match_number: The unique number identifying the match.
        :type match_number: int
        :param players: A tuple containing two players participating in the match.
        :type players: tuple[Player]
        :raises ValueError: If `players` does not contain exactly two elements.
        """
        self.number = int(match_number)
        self.player1 = players[0]
        self.player2 = players[1]
        self.result = [(self.player1, 0), (self.player2, 0)]

    def assign_result(self, winner="match nul"):
        """
        Assigns the result of a match by updating player scores.

        :param winner: The winner of the match. Defaults to "match nul" (draw).
            - If it is `self.player1`, `self.player1.score is increased by 1 point.
            - If it is `self.player2`, `self.player2.score is increased by 1 point.
            - If it is "match nul", both players score are increased by 0.5 points.
        :type winner: Player or str
        :return: A list of tuples where each tuple contains a player and their respective score for the match.
        :rtype: list[tuple]
        """
        if winner == self.player1:
            self.player1.score += 1
            return [(self.player1, 1), (self.player2, 0)]

        elif winner == self.player2:
            self.player2.score += 1
            return [(self.player1, 0), (self.player2, 1)]

        else:
            self.player1.score += .5
            self.player2.score += .5
            return [(self.player1, 0.5), (self.player2, 0.5)]


def check_existence_json_file(path: str):
    """
    Check the existence of the Json file

    :param path : path to the file
    :type path: str
    """
    json_file = path
    os.makedirs(os.path.dirname(json_file), exist_ok=True)

    if not os.path.exists(json_file):
        with open(json_file, "w", encoding="utf-8") as file:
            json.dump([], file)


def find_player_in_json(player_number: str):
    """
    Searches for a player by their national number in a JSON file.

    :param player_number: The national player number to search for.
        Must follow the format `r"^[a-z]{2}\\d{5}$"` (e.g., "fr12345").
    :type player_number: str

    :raises FileNotFoundError: If the JSON file does not exist.
    :raises json.JSONDecodeError: If the JSON file is malformed.

    :return: A dictionary containing the player's data if found, otherwise `None`.
    :rtype: dict or None
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
    """
        Returns the sorting key for a player's name.

        :param player: instance de Player .
        :type player: Player
        :return: The player's name to be used as the sorting key.
        :rtype: str
        """

    return player.name


def sort_by_npn(player):
    """
        Returns the sorting key for a player's national player number.

        :param player: instance de Player .
        :type player: Player
        :return: The player's national player number to be used as the sorting key.
        :rtype: str
        """

    return player.national_player_number


def sort_by_score(player):
    """
    Returns the sorting key for a player's score.

    :param player: instance de Player .
    :type player: Player
    :return: The player's score to be used as the sorting key.
    :rtype: int or float
    """
    return player.score


def sort_players(players: List[Player], criterion="name", reverse=False):
    """
     Sorts a list of players based on the given criterion.

    :param players: List of Player instances.
    :type players: list[Player]
    :param criterion: The criterion used for sorting players.
        Valid options are:
        - "name": Sort players alphabetically by their name.
        - "national_player_number": Sort players by their national player number.
        - "score": Sort players by their score, in descending order.
    :type criterion: str
    :param reverse: If True, Sort by descending order.
    :type reverse: Boolean
    :return: Sorted list of player instances.
    :rtype: List[Player]
    """
    sort_functions = {
        "name": sort_by_name,
        "national_player_number": sort_by_npn,
        "score": sort_by_score,
    }

    if criterion not in sort_functions:
        raise ValueError("Critère invalide. Utilisez 'name', 'national_player_number' ou 'score'.")

    return sorted(players, key=sort_functions[criterion], reverse=reverse)


def find_tournaments_in_file():
    """
    Retrieves a list of tournament JSON files from the specified directory.

    :return: A list of filenames for tournament JSON files in the "data/tournaments/" directory.
    :rtype: list[str]
    :raises FileNotFoundError: If the "data/tournaments/" directory does not exist.
    """
    files_path = "data/tournaments/"

    if not os.path.exists(files_path):
        print(f"Le répertoire {files_path} n'existe pas.")
        return []

    tournaments_files = [file for file in os.listdir(files_path) if file.endswith(".json")]

    return tournaments_files


def find_tournaments(criterion="all"):
    """
    Searches for tournaments based on the specified criterion and retrieves their data.

    :param criterion: Filter for tournaments. Options are:
        - "all": Retrieves all tournaments.
        - "no_ended": Retrieves tournaments that have not ended (end_date is None).
        - "ended": Retrieves tournaments that have ended (end_date is not None).
        Defaults to "all".
    :type criterion: str, optional
    :return: A list of tournament data dictionaries matching the specified criterion.
    :rtype: list[dict]
    :raises json.JSONDecodeError: If a JSON file is poorly formatted.
    """
    tournaments_json_files = find_tournaments_in_file()
    find_tournament = []

    for json_file in tournaments_json_files:
        json_path = f"data/tournaments/{json_file}"

        with (open(json_path, "r", encoding="utf-8") as file):
            try:
                tournament_data = json.load(file)
                if criterion == "no_ended":
                    if tournament_data["end_date"] is None:
                        find_tournament.append(tournament_data)
                elif criterion == "ended":
                    if tournament_data["end_date"] is not None:
                        find_tournament.append(tournament_data)
                else:
                    find_tournament.append(tournament_data)

            except json.JSONDecodeError:
                print("Le fichier JSON est mal formaté.")
    return find_tournament
