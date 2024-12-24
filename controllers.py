import json
from typing import Union

from models import Tournament, Player, DataBase
from settings import PLAYERS_FILE_PATH
from views import TournamentView, DataBaseView, ApplicationView


class MainController:

    def __init__(self):
        self.tournament_view = TournamentView()
        self.data_base = DataBase()
        self.data_base_view = DataBaseView()
        self.application_view = ApplicationView()
        self.reload_data_base = ReloadDataBase()

    def run(self):
        """
        Main entry point for the application: displays the home menu.

        This method presents the user with a home menu and handles
        navigation to:
        - Manage tournaments: Access tournament-related options (create, load).
        - Add players to the database: Open the player management menu.
        - Access saved data: View saved players or tournaments.
        - Exit the program.

        """

        while True:
            self.application_view.clear_console()
            self.application_view.display_home_menu()
            option = self.application_view.choose_option()
            if option == "1":  # Manage a tournament
                self.manage_tournament_options()
            elif option == "2":  # Add player to the database
                self.reload_data_base.add_player_database()
            elif option == "3":  # Recorded data
                self.reload_data_base.access_saved_data()
            elif option == "4":  # exit the program
                break
            else:
                continue

    def manage_tournament_options(self):
        """
        Displays the tournament options menu and handles user input.

        The method allows the user to:
        - Start a new tournament by providing its details.
        - Load an ongoing tournament from the database.
        - Exit the tournament options menu.

        """
        while True:
            self.application_view.clear_console()
            self.tournament_view.display_menu_tournament()
            option = self.application_view.choose_option()

            if option == "1":  # start a new tournament
                self.application_view.clear_console()
                data = self.tournament_view.display_tournament_start()

                if data["max_round_number"] == "":
                    data["max_round_number"] = 4

                tournament = Tournament(data["name"],
                                        data["place"],
                                        data["description"],
                                        int(data["max_round_number"])
                                        )
                tournament.save()
                self.tournament_view.display_confirm_tournament_creation()
                self.run_tournament(tournament)

            elif option == "2":  # load a tournament
                loaded_tournament = (self.reload_data_base.
                                     reload_tournament("no_ended"))

                if loaded_tournament:
                    tournament = Tournament(loaded_tournament["name"],
                                            loaded_tournament["place"]
                                            )
                    tournament.load(loaded_tournament)
                    self.tournament_view.display_confirm_tournament_loaded()
                    self.run_tournament(tournament)

            elif option == "3":  # Return
                break
            else:
                continue

    def run_tournament(self, tournament):
        """
        Executes the tournament process, including registering players and
        running the rounds.

        :param tournament: The tournament object containing details about
                            players, rounds, matches, and the tournament's
                            current state.
        :type tournament: Tournament
        """
        # add players
        while True:
            players_boarding_over = (
                self.register_players_to_tournament(tournament))
            # run rounds
            if players_boarding_over:
                self.run_rounds_tournament(tournament)
                break
            else:
                break

    def run_rounds_tournament(self, tournament):
        """
        Manages the execution of rounds within a tournament. Adds rounds,
        processes match results, and handles the conclusion of the tournament.

        :param tournament: The tournament object containing details about
                            players, rounds, matches, and the tournament's
                            current state.
        :type tournament: Tournament
        """

        while True:

            if tournament.round_number != tournament.max_round:
                if (len(tournament.rounds) == 0
                        or tournament.rounds[-1].end_time):

                    self.add_round_to_tournament(tournament)
                    tournament.save()

                    if (len(tournament.rounds[-1].matches) !=
                            len(tournament.players) / 2):
                        self.tournament_view.display_matches_creation_error_message()  # noqa: E501
                        tournament.ended()
                        self.tournament_view.display_tournament_ended(
                            tournament)
                        break

            elif tournament.rounds[-1].end_time:

                tournament.ended()
                tournament.save()
                self.application_view.clear_console()
                self.tournament_view.display_tournament_ended(tournament)
                break

            self.application_view.clear_console()
            self.tournament_view.display_match_menu(tournament.rounds[-1])
            self.tournament_view.display_menu_assign_result()

            option = self.application_view.choose_option()
            if option == "1":  # Enter the results of matches
                self.validate_results(tournament)
            elif option == "2":  # return
                tournament.save()
                break
            else:
                continue

    def register_players_to_tournament(self, tournament):
        """
        Manages the registration of players to a tournament. Ensures that the
        player list meets the required criteria before the tournament starts.

        :param tournament: The tournament instance where players will be
                            registered.
        :type tournament: Tournament
        :return: A boolean indicating whether player registration is complete
                 and the tournament is ready to start.
        :rtype: bool
        :raises ValueError: If the number of players is insufficient or invalid
                            for the tournament.
        """
        while True:
            #  pass this section if tournament is reloaded and round started
            if len(tournament.rounds) != 0:
                return True

            self.application_view.clear_console()
            TournamentView.display_add_player_message()
            if len(tournament.players) != 0:
                self.data_base_view.display_players_list(
                    tournament.players,
                    "Liste des joueurs inscrits")

                self.tournament_view.display_menu_add_player()
                option = self.application_view.choose_option()
                if option == "2":  # start the first round
                    if len(tournament.players) % 2 != 0:
                        (self.tournament_view.display_wrong_players_number_message())  # noqa: E501
                        continue
                    elif len(tournament.players) < int(
                            tournament.max_round) + 1:
                        self.tournament_view.display_too_low_player_number_warning()  # noqa: E501
                        continue
                    elif len(tournament.players) < 2 * int(
                            tournament.max_round):
                        option = (
                            self.tournament_view.display_low_player_number_warning())  # noqa: E501
                        if option == "1":  # start round despite the warning
                            return True
                        else:
                            continue
                    else:
                        return True

                elif option == "1":  # add players
                    self.application_view.clear_console()
                    TournamentView.display_add_player_message()
                    self.data_base_view.display_players_list(
                        tournament.players,
                        "Liste des joueurs participants")
                    self.add_player_to_tournament(tournament)
                    tournament.save()
                else:  # return

                    return False

            else:
                self.add_player_to_tournament(tournament)
                tournament.save()

    def add_player_to_tournament(self, tournament):
        """
        Adds players to a tournament.

        Prompts the user to enter one or more National Player Numbers (NPNs).
         For each NPN:
        - Checks if the player is already registered in the tournament.
        - If not registered, attempts to add the player.
        - If the player is not found in the database,
         prompts the user to create a new player.

        :param tournament: The tournament instance where players will be added.
        :type tournament: Tournament
        """
        players_number = self.data_base_view.ask_national_player_number()

        for player_number in players_number:
            already_registered_player = False
            for player in tournament.players:
                if player.national_player_number == player_number:
                    TournamentView.display_player_already_registered(player)
                    already_registered_player = True
                    break

            if not already_registered_player:
                player = tournament.add_player(player_number)

                if not player:
                    self.reload_data_base.create_new_player(player_number)
                    tournament.add_player(player_number)

    @staticmethod
    def add_round_to_tournament(tournament: Tournament):
        """add one round to the tournament
        :param tournament: The tournament object containing rounds and matches.
        :type tournament: Tournament
        """
        tournament.add_round()
        tournament.rounds[-1].add_match()

    def validate_results(self, tournament: Tournament):
        """
        Validates and assigns results for the matches in the current round
        of a tournament.
        Allows user interaction to assign or confirm match results until
        the round is marked as ended.

        :param tournament: The tournament object containing rounds and matches.
        :type tournament: Tournament

        """
        while not tournament.rounds[-1].end_time:
            tournament.save()
            self.application_view.clear_console()
            match_without_result = 0

            for match in tournament.rounds[-1].matches:
                if match.result == [(match.player1, 0), (match.player2, 0)]:
                    match_without_result += 1

            if match_without_result == 0:
                self.data_base_view.display_matches(
                    tournament.rounds[-1].matches,
                    "liste des matchs"
                )
                TournamentView.display_valid_result()
                option = self.application_view.choose_option()
                if option == "1":  # the user validates the results
                    tournament.rounds[-1].ended()
                    break

            match_number = (self.tournament_view.display_select_results_menu(
                tournament.rounds[-1],
                match_without_result)
            )
            if (match_number.isdigit() and
                    int(match_number) <= len(tournament.rounds[-1].matches)):
                match = tournament.rounds[-1].matches[int(match_number) - 1]
                TournamentView.display_assign_match_result(match)
                result = self.application_view.choose_option()
                if result == "1":
                    match.result = match.assign_result(match.player1)
                elif result == "2":
                    match.result = match.assign_result(match.player2)
                elif result == "3":
                    match.result = match.assign_result()
            else:
                break


class ReloadDataBase:

    def __init__(self):
        self.data_base_view = DataBaseView()
        self.application_view = ApplicationView()
        self.data_base = DataBase()

    def add_player_database(self):
        """
        Adds a player to the JSON file 'data/players.json'.

        This function repeatedly prompts the user to enter one
        or more National Player Numbers (NPNs).
        For each NPN:
        - If the player already exists in the database,
                    displays their information.
        - If the player does not exist,
                    prompts the user to create a new player.

        The user is given an option to add more players or exit the function.

        :raises FileNotFoundError: If the JSON file is not found.
        :raises json.JSONDecodeError: If the JSON file is malformed.
        """
        while True:
            self.application_view.clear_console()
            self.data_base_view.display_title_add_player_to_database()
            players_number = self.data_base_view.ask_national_player_number()

            for player_number in players_number:
                found_player = DataBase().find_player_in_json(player_number)

                if found_player:
                    player = Player(found_player["national_player_number"],
                                    found_player["name"],
                                    found_player["first_name"],
                                    found_player["birthday"]
                                    )
                    self.data_base_view.player_in_database(player)
                else:
                    self.create_new_player(player_number)

            self.data_base_view.display_menu_add_player_to_database()
            option = self.application_view.choose_option()
            if option == "1":  # enregistrer un autre joueur
                continue
            else:
                break

    def create_new_player(self, player_number) -> Player:
        """
        Creates a new player and saves them to the JSON file.

        This function:
        - Prompts the user to input information for a new player
            not found in the database.
        - Creates a `Player` object using the provided data.
        - Saves the new player to the JSON file.
        - Displays the newly created player.

        :param player_number: The national player number of the new player.
        :type player_number: str
        :return: The newly created `Player` object.
        :rtype: Player
        """
        data = self.data_base_view.player_not_in_database(player_number)
        new_player = Player(**data)
        DataBase.write_new_player_in_json(new_player)
        self.data_base_view.display_players_list(
            [new_player],
            "Nouveau joueur")
        return new_player

    def access_saved_data(self):
        """
        Provides access to saved data, including registered players and
        completed tournaments.

        This method displays a menu that allows the user to:
        - View and sort the list of registered players, either by national
            player number or name.
        - View details of completed tournaments, including rounds and
            participants.
        """

        while True:
            self.application_view.clear_console()
            self.data_base_view.display_menu_saved_data()
            option = self.application_view.choose_option()

            if option == "1":  # Joueurs enregistrés
                json_file = PLAYERS_FILE_PATH
                DataBase.check_existence_json_file(json_file)

                with (open(json_file, "r", encoding="utf-8") as file):
                    players_data = json.load(file)
                    players = [Player(**data) for data in players_data]
                    self.application_view.clear_console()
                    self.data_base_view.display_menu_registered_players()
                    option = self.application_view.choose_option()

                    if option == "1":  # sorted by national player number
                        sorted_players = self.data_base.sort_players(
                            players,
                            "national_player_number"
                        )
                        title = "Liste des joueurs classée par leur numéro"
                    elif option == "2":  # sorted by name
                        title = "Liste des joueurs classée par leur nom"
                        sorted_players = self.data_base.sort_players(players)
                    self.application_view.clear_console()
                    self.data_base_view.display_players_list(
                        sorted_players,
                        title
                    )
                    self.application_view.break_point()

            elif option == "2":  # Tournois enregistrés
                loaded_tournament = self.reload_tournament()

                if loaded_tournament:
                    tournament = Tournament(
                        loaded_tournament["name"],
                        loaded_tournament["place"]
                    )
                    tournament.load(loaded_tournament)
                    self.application_view.clear_console()
                    self.data_base_view.display_all_tournament(tournament)

            else:
                break

    def reload_tournament(self, criterion: str = "all") -> Union[dict, None]:
        """
        Reloads a tournament based on the specified criterion and
         allows the user to select one from the list.

        :param criterion: Filter for tournaments to display. Options are:
            - "all": Displays all tournaments.
            - "No_ended": Displays tournaments that have not ended.
            - "ended": Displays tournaments that have ended.
            Defaults to "all".
        :type criterion: str, optional
        :return: The tournament data selected by the user.
        :rtype: dict
        :raises IndexError: If the user selects an invalid index from the list.
        """
        tournaments = DataBase().find_tournaments(criterion)
        index = self.data_base_view.display_reload_tournament(tournaments)
        if index != "":
            loaded_tournament = tournaments[int(index) - 1]
            return loaded_tournament
        else:
            return
