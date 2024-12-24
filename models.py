import random
import json
import os

from datetime import datetime
from typing import List, Union

from settings import TOURNAMENT_FILE_PATH, PLAYERS_FILE_PATH


class Player:
    """un joueur"""

    def __init__(self,
                 national_player_number: str,
                 name: str,
                 first_name: str,
                 birthday: str,
                 score: int = 0
                 ):
        """
        Initializes a player's attributes, including their national
         player number, name, first name, birthday and score.

        :param national_player_number: The unique national player
        number, validated to follow the format 'aa11111'.
        :type national_player_number: str
        :param name: The player's last name, validated and formatted
        with an initial capital letter.
        :type name: str
        :param first_name: The player's first name, validated and
        formatted with an initial capital letter.
        :type first_name: str
        :param birthday: The player's date of birth, validated and
        formatted in the format 'dd/mm/yyyy'.
        :type birthday: str
        :param score: The player's initial score, defaults to 0.
        :type score: int, optional
        """
        self.name = name
        self.first_name = first_name
        self.birthday = birthday
        self.national_player_number = national_player_number
        self.score = score
        self.opponents = []

    def __repr__(self) -> str:
        return (f"{self.national_player_number: <12}"
                f"{self.name: <15}{self.first_name: <15}"
                f"{self.birthday: <12}"
                f"{self.score: <6}")


class Tournament:
    """un tournoi"""

    def __init__(self,
                 name: str,
                 place: str,
                 description: str = "",
                 max_round: int = 4
                 ):
        """
        Initializes a tournament with its details.

        :param name: The name of the tournament.
        :type name: str
        :param place: The location where the tournament is held.
        :type place: str
        :param description: A brief description of the tournament.
         Defaults to an empty string.
        :type description: str, optional
        :param max_round: The maximum number of rounds in the tournament.
         Defaults to 4.
        :type max_round: int, optional
        """
        self.name = name
        self.place = place
        self.start_date = datetime.now()
        self.end_date = None
        self.round_number = 0
        self.max_round = int(max_round)
        self.players = []
        self.rounds = []
        self.description = description

    def add_player(self,
                   player_number: str) \
            -> Union[Player, None]:
        """
        Adds a participant to the tournament.

        :param player_number: The national player number of the player to add.
        :type player_number: str
        :return: The `Player` object if the player was successfully added
        or already exists in the tournament,
                 `False` if the player was not found in the JSON file.
        :rtype: Player or boolean
        """
        json_file = PLAYERS_FILE_PATH
        DataBase.check_existence_json_file(json_file)

        found_player = DataBase().find_player_in_json(player_number)

        if found_player:
            player = Player(found_player["national_player_number"],
                            found_player["name"],
                            found_player["first_name"],
                            found_player["birthday"]
                            )
            if player not in self.players:
                self.players.append(player)
                return player
            else:
                return player
        else:
            return None

    def add_round(self):
        """Add a round to a tournament"""
        self.round_number += 1
        self.rounds.append(Round(self.round_number, self.players))
        return

    def ended(self):
        """
        Marks the current tournament as ended by setting the end date to the
        current date and time.
        """
        self.end_date = datetime.now()

    def save(self):
        """
        Saves the tournament data to a JSON file.

        The method serializes the tournament details,
        including players, rounds, and matches,
        into a JSON file.
        The JSON file is saved in the directory `data/tournaments/`
        with the tournament name as the filename.
        """
        json_file = f"{TOURNAMENT_FILE_PATH}{self.name}.json"
        DataBase.check_existence_json_file(json_file)

        player_data = []
        for player in self.players:
            player_data.append(
                {"national_player_number": player.national_player_number,
                 "name": player.name,
                 "first_name": player.first_name,
                 "birthday": player.birthday,
                 "score": player.score
                 }
            )

        rounds_data = []
        for played_round in self.rounds:
            match_data = []
            for match in played_round.matches:
                data = {
                    "match_number": match.number,
                    "player1": {
                        "national_player_number": match.player1.national_player_number,  # noqa: E501
                        "name": match.player1.name,
                        "first_name": match.player1.first_name,
                        "birthday": match.player1.birthday,
                        "score": match.player1.score
                    },
                    "player2": {
                        "national_player_number": match.player2.national_player_number,  # noqa: E501
                        "name": match.player2.name,
                        "first_name": match.player2.first_name,
                        "birthday": match.player2.birthday,
                        "score": match.player2.score},
                    "result":
                        [("Payer1", match.result[0][1]),
                         ("Player2", match.result[1][1])
                         ]
                }
                match_data.append(data)

            if played_round.end_time:
                end = played_round.end_time.strftime("%d-%m-%Y %H:%M")
            else:
                end = None

            round_data = {
                "name": played_round.name,
                "round_number": played_round.round_number,
                "start_time": played_round.start_time.strftime("%d-%m-%Y %H:%M"),  # noqa: E501
                "end_time": end,
                "matches": match_data
            }
            rounds_data.append(round_data)

        if self.end_date:
            end = self.end_date.strftime("%d-%m-%Y %H:%M")
        else:
            end = None

        data = {"name": self.name,
                "place": self.place,
                "description": self.description,
                "start_date": self.start_date.strftime("%d-%m-%Y %H:%M"),
                "end_date": end,
                "round_number": self.round_number,
                "max_round": self.max_round,
                "players": player_data,
                "rounds": rounds_data
                }

        if not os.path.exists(json_file):
            with open(json_file, "w", encoding="utf-8") as file:
                json.dump([], file)

        with open(json_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        return

    def load(self, loaded_tournament):
        """
        Loads a tournament's data into the current instance.

        This method initializes the tournament object with
        data loaded from a serialized source.
        It recreates the players, rounds, and matches.

        :param loaded_tournament: The serialized tournament data to load.
        :type loaded_tournament: dict
        """

        self.start_date = datetime.strptime(
            loaded_tournament["start_date"], "%d-%m-%Y %H:%M")
        if loaded_tournament["end_date"]:
            self.end_date = datetime.strptime(
                loaded_tournament["end_date"], "%d-%m-%Y %H:%M")
        else:
            self.end_date = False
        self.round_number = loaded_tournament["round_number"]
        self.max_round = loaded_tournament["max_round"]
        self.description = loaded_tournament["description"]

        for player in loaded_tournament["players"]:
            self.players.append(
                Player(player["national_player_number"],
                       player["name"],
                       player["first_name"],
                       player["birthday"],
                       player["score"]
                       )
            )

        for loaded_round in loaded_tournament["rounds"]:
            self.rounds.append(Round(
                loaded_round["round_number"],
                self.players
            )
            )
            self.rounds[-1].start_time = datetime.strptime(
                loaded_round["start_time"], "%d-%m-%Y %H:%M")

            if loaded_round["end_time"]:
                self.rounds[-1].end_time = datetime.strptime(
                    loaded_round["end_time"], "%d-%m-%Y %H:%M")
            else:
                self.rounds[-1].end_time = False

            for played_match in loaded_round['matches']:

                player1 = next(player for player in self.players if
                               player.national_player_number ==
                               played_match["player1"][
                                   "national_player_number"])
                player2 = next(player for player in self.players if
                               player.national_player_number ==
                               played_match["player2"][
                                   "national_player_number"])

                player1.opponents.append(player2.national_player_number)
                player2.opponents.append(player1.national_player_number)

                match = Match(
                    played_match["match_number"],
                    (player1, player2)
                )

                if played_match["result"][0][1] == 1:
                    match.result = [(player1, 1), (player2, 0)]
                elif played_match["result"][1][1] == 1:
                    match.result = [(player1, 0), (player2, 1)]
                elif played_match["result"][1][1] == 0.5:
                    match.result = [(player1, 0.5), (player2, 0.5)]
                else:
                    match.result = [(player1, 0), (player2, 0)]

                self.rounds[-1].matches.append(match)


class Round:
    """un tour"""

    def __init__(self, round_number: int, players: List[Player]):
        """
        Initializes a tournament round.

        :param round_number: The current round number.
        :type round_number: int
        :param players: A list of players participating in the round.
            - For the first round, players are shuffled randomly.
            - For the next rounds, players are sorted by
                their scores in descending order.
        :type players: list[Player]
        """
        self.name = f"round {round_number}"
        self.round_number = round_number
        self.start_time = datetime.now()
        self.end_time = False
        if self.round_number == 1:
            random.shuffle(players)
            self.players = players
        else:
            self.players = DataBase().sort_players(
                players, "score", True
            )
        self.matches = []

    def add_match(self):
        """
        Adds matches to the current round based on available players.

        The method pairs players who have not yet played against each other in
        previous rounds. Each match is assigned a unique match number.
        :return: A list of `Match` objects representing the matches for
            the round.
        :rtype: list[Match]
        """
        attempt = 0
        while True:
            used_players = set()
            match_number = 1

            for i, player1 in enumerate(self.players):

                if player1 in used_players:
                    continue

                for j in range(i + 1, len(self.players)):
                    player2 = self.players[j]

                    if (player2 in used_players or
                            player2.national_player_number in
                            player1.opponents):
                        continue

                    match = Match(match_number, (player1, player2))
                    self.matches.append(match)
                    match_number += 1

                    player1.opponents.append(player2.national_player_number)
                    player2.opponents.append(player1.national_player_number)
                    used_players.add(player1)
                    used_players.add(player2)

                    break

            if len(self.matches) != len(self.players) / 2:
                attempt += 1
                for match in self.matches:
                    del match.player1.opponents[-1]
                    del match.player2.opponents[-1]
                self.matches = []
                if attempt == 1:
                    self.players = DataBase().sort_players(
                        self.players,
                        "score"
                    )
                    continue
                elif attempt == 2:
                    self.players = DataBase().sort_players(
                        self.players,
                        "name"
                    )
                elif attempt == 3:
                    self.players = DataBase().sort_players(
                        self.players,
                        "name", True
                    )
                elif attempt == 4:
                    self.players = DataBase().sort_players(
                        self.players,
                        "national_player_number"
                    )
                elif attempt == 5:
                    self.players = DataBase().sort_players(
                        self.players,
                        "national_player_number", True
                    )
                else:
                    break
            else:
                break
        return

    def ended(self):
        """
        Marks the current round as ended by setting the end date to the
        current date and time.
        """
        self.end_time = datetime.now()


class Match:
    """un match"""

    def __init__(self, match_number, players):
        """
        Initializes a match with the given match number and players.

        :param match_number: The unique number identifying the match.
        :type match_number: int
        :param players: A tuple containing two players participating
        in the match.
        :type players: tuple[Player]
        """
        self.number = int(match_number)
        self.player1 = players[0]
        self.player2 = players[1]
        self.result = [(self.player1, 0), (self.player2, 0)]

    def assign_result(self, winner="match nul"):
        """
        Assigns the result of a match by updating player scores.

        :param winner: The winner of the match. Defaults to "match nul" (draw).
            - If it is "player1", player1.score is increased by 1 point.
            - If it is "player2", player2.score is increased by 1 point.
            - If it is "match nul", both players score are increased
                        by 0.5 points.
        :type winner: Player or str
        :return: A list of tuples where each tuple contains a player and
         their respective score for the match.
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


class DataBase:

    @staticmethod
    def check_existence_json_file(path: str):
        """
        Check the existence of the Json file.
        Create the file if it's not found

        :param path : path to the file
        :type path: str
        """
        json_file = path
        os.makedirs(os.path.dirname(json_file), exist_ok=True)

        if not os.path.exists(json_file):
            with open(json_file, "w", encoding="utf-8") as file:
                json.dump([], file)

    def find_player_in_json(self, player_number: str) -> Union[dict, None]:
        """
        Searches for a player by their national number in a JSON file.

        :param player_number: The national player number to search for.
            Must follow the format `r"^[a-z]{2}\\d{5}$"` (e.g., "fr12345").
        :type player_number: str

        :raises json.JSONDecodeError: If the JSON file is malformed.

        :return: A dictionary containing the player's data if found,
                otherwise `None`.
        :rtype: dict or None
        """

        self.check_existence_json_file(PLAYERS_FILE_PATH)

        found_player = None
        with open(PLAYERS_FILE_PATH, "r", encoding="utf-8") as file:
            try:
                players_data = json.load(file)
                for data in players_data:
                    if data["national_player_number"] == player_number:
                        found_player = data
                        break
            except json.JSONDecodeError:
                print("Le fichier JSON est mal formaté.")
        return found_player

    @staticmethod
    def write_new_player_in_json(player):
        """Write a new player in the Json file

        :param player: instances de Player.
        """
        data = {
            "national_player_number": player.national_player_number,
            "name": player.name,
            "first_name": player.first_name,
            "birthday": player.birthday,
            "score": player.score
        }
        if not os.path.exists(PLAYERS_FILE_PATH):
            with open(PLAYERS_FILE_PATH, "w", encoding="utf-8") as file:
                json.dump([], file)

        with open(PLAYERS_FILE_PATH, "r", encoding="utf-8") as file:
            players_data = json.load(file)

        players_data.append(data)

        with open(PLAYERS_FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(players_data, file, indent=4, ensure_ascii=False)

        return

    @staticmethod
    def find_tournaments_in_file():
        """
        Retrieves a list of tournament JSON files from the specified directory.

        :return: A list of filenames in the "data/tournaments/" directory.
        :rtype: list[str]
        """

        if not os.path.exists(TOURNAMENT_FILE_PATH):
            print(f"Le répertoire {TOURNAMENT_FILE_PATH} n'existe pas.")
            return []

        tournaments_files = [file for file in os.listdir(TOURNAMENT_FILE_PATH)
                             if file.endswith(".json")]

        return tournaments_files

    def find_tournaments(self, criterion="all") -> list[dict]:
        """
        Searches for tournaments based on the specified criterion and
        retrieves their data.

        :param criterion: Filter for tournaments. Options are:
            - "all": Retrieves all tournaments.
            - "no_ended": Retrieves tournaments that have not ended.
            - "ended": Retrieves tournaments that have ended.
            Defaults to "all".
        :type criterion: str, optional
        :return: A list of tournament data dictionaries matching the
                    specified criterion.
        :rtype: list[dict]
        """
        tournaments_json_files = self.find_tournaments_in_file()
        find_tournament = []

        for json_file in tournaments_json_files:
            json_path = f"{TOURNAMENT_FILE_PATH}{json_file}"

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

    @staticmethod
    def sort_players(players: List[Player],
                     criterion="name",
                     reverse=False) -> list[Player]:
        """
         Sorts a list of players based on the given criterion.

        :param players: List of Player instances.
        :type players: list[Player]
        :param criterion: The criterion used for sorting players.
            Valid options are:
            - "name": Sort players alphabetically by their name.
            - "national_player_number": Sort players by their national
                                        player number.
            - "score": Sort players by their score, in descending order.
        :type criterion: str
        :param reverse: If True, Sort by descending order.
        :type reverse: Boolean
        :return: Sorted list of player instances.
        :rtype: List[Player]
        """
        sort_keys = {
            "name":
                lambda player: player.name,
            "national_player_number":
                lambda player: player.national_player_number,
            "score":
                lambda player: player.score
        }

        if criterion not in sort_keys:
            raise ValueError(
                "Critère invalide. Utilisez 'name',"
                "'national_player_number' ou 'score'.")

        return sorted(players, key=sort_keys[criterion], reverse=reverse)
