import json

from models import Tournament, Player, find_player_in_json, write_new_player_in_json, check_existence_json_file, \
    sort_players, find_tournaments
from views2 import (
    display_menu, choose_option, display_menu_tournament, display_tournament_start, ask_national_player_number,
    player_in_database, player_not_in_database, display_menu_add_player, clear_console, display_menu_saved_data,
    display_players_list, display_menu_saved_data_registered_players, display_assign_match_result, display_matchs,
    display_match_menu, display_confirm_tournament_creation, display_valid_result, display_add_player_message,
    display_player_already_registered, display_validate_result_menu, display_tournament_ended,
    display_reload_tournament, display_confirm_tournament_loaded, display_all_tournament,
    display_wrong_players_number_message, break_point
)


def run():
    """ menu d'accueil """
    while True:
        clear_console()
        display_menu()
        option = choose_option()
        if option == "1":  # Gérer un tournoi
            manage_tournament_options()
        elif option == "2":  # Ajouter des joueurs à la base de donnée
            add_player_database()
        elif option == "3":  # données enregistrées
            access_saved_data()
        elif option == "4":  # Quitter le programme
            break
        else:
            continue


def manage_tournament_options():
    """menu pour options de tournoi """
    while True:
        clear_console()
        display_menu_tournament()
        option = choose_option()

        if option == "1":  # Démarrer un nouveau tournoi
            clear_console()
            data = display_tournament_start()

            if data["max_round_number"] == "":
                data["max_round_number"] = 4

            tournament = Tournament(data["name"], data["place"], data["description"], int(data["max_round_number"]))
            display_confirm_tournament_creation()
            run_tournament(tournament)

        elif option == "2":  # Reprendre un tournoi
            loaded_tournament = reload_tournament("no_ended")

            if loaded_tournament:
                tournament = Tournament(loaded_tournament["name"], loaded_tournament["place"])
                tournament.load(loaded_tournament)
                display_confirm_tournament_loaded()
                run_tournament(tournament)

        else:  # Retour
            break


def run_tournament(tournament):
    """run a tournament instance"""
    while True:
        clear_console()
        display_add_player_message()
        if len(tournament.players) != 0:
            display_players_list(tournament.players)
            display_menu_add_player()
            option = choose_option()
            if option == "2":
                if len(tournament.players) % 2 != 0:
                    display_wrong_players_number_message()
                    continue
                else:
                    break
            else:
                clear_console()
                display_add_player_message()
                display_players_list(tournament.players)
                add_player_to_tournament(tournament)
        else:
            add_player_to_tournament(tournament)

    while tournament.round_number <= tournament.max_round:
        if len(tournament.rounds) == 0 or tournament.rounds[-1].ended is True:
            add_round_to_tournament(tournament)
        else:
            clear_console()
            display_match_menu(tournament.rounds[-1])
            validate_results(tournament)

    display_tournament_ended(tournament)
    del tournament.rounds[-1]
    tournament.ended()
    tournament.save()
    break_point()


def add_player_to_tournament(tournament):
    """
    Adds players to a tournament.

    Prompts the user to enter one or more National Player Numbers (NPNs). For each NPN:
    - Checks if the player is already registered in the tournament.
    - If not registered, attempts to add the player using `tournament.add_player`.
    - If the player is not found in the database, prompts the user to create a new player.

    :param tournament: The tournament instance where players will be added.
    :type tournament: Tournament
    """
    players_number = ask_national_player_number()

    for player_number in players_number:
        already_registered_player = False
        for player in tournament.players:
            if player.national_player_number == player_number:
                display_player_already_registered(player)
                already_registered_player = True
                break

        if not already_registered_player:
            player = tournament.add_player(player_number)

            if not player:
                create_new_player(player_number)


def add_player_database():
    """
    Adds a player to the JSON file 'data/players.json'.

    This function repeatedly prompts the user to enter one or more National Player Numbers (NPNs).
    For each NPN:
    - If the player already exists in the database, displays their information.
    - If the player does not exist, prompts the user to create a new player.

    The user is given an option to add more players or exit the function.

    :raises FileNotFoundError: If the JSON file 'data/players.json' is not found.
    :raises json.JSONDecodeError: If the JSON file is malformed.
    """
    while True:
        clear_console()
        players_number = ask_national_player_number()

        for player_number in players_number:
            found_player = find_player_in_json(player_number)

            if found_player:
                player = Player(found_player["national_player_number"], found_player["name"],
                                found_player["first_name"], found_player["birthday"])
                player_in_database(player)
            else:
                create_new_player(player_number)

        display_menu_add_player()
        option = choose_option()
        if option == "1":  # enregistrer un autre joueur
            continue
        else:
            break


def create_new_player(player_number):
    """
    Creates a new player and saves them to the JSON file.

    This function:
    - Prompts the user to input information for a new player not found in the database.
    - Creates a `Player` object using the provided data.
    - Saves the new player to the JSON file.
    - Displays the newly created player.

    :param player_number: The national player number of the new player.
    :type player_number: str
    :return: The newly created `Player` object.
    :rtype: Player
    """
    data = player_not_in_database(player_number)
    new_player = Player(**data)
    write_new_player_in_json(new_player)
    display_players_list([new_player])
    return new_player


def add_round_to_tournament(tournament):
    """ajoute un tour au tournoi"""

    while True:
        tournament.add_round()
        tournament.rounds[-1].add_match(tournament.rounds)
        if len(tournament.rounds[-1].matchs) != len(tournament.players)/2:
            tournament.round[-1].players = sort_players(tournament.round[-1].players, "score")
            tournament.rounds[-1].add_match(tournament.rounds)
            break
        else:
            break


def validate_results(tournament):
    """
    Validates and assigns results for the matches in the current round of a tournament.
    Allows user interaction to assign or confirm match results until the round is marked as ended.

    :param tournament: The tournament object containing rounds and matches.
    :type tournament: Tournament

    """
    while not tournament.rounds[-1].ended:
        clear_console()
        match_without_result = 0

        for match in tournament.rounds[-1].matchs:
            if match.result == [(match.player1, 0), (match.player2, 0)]:
                match_without_result += 1

        if match_without_result == 0:
            display_matchs(tournament.rounds[-1].matchs)
            display_valid_result()
            option = choose_option()
            if option == "1":
                tournament.rounds[-1].ended = True
                break

        match_number = display_validate_result_menu(tournament.rounds[-1], match_without_result)
        if match_number != '':
            match = tournament.rounds[-1].matchs[int(match_number) - 1]
            display_assign_match_result(match)
            result = choose_option()
            if result == "1":
                match.result = match.assign_result(match.player1)
                continue
            elif result == "2":
                match.result = match.assign_result(match.player2)
                continue
            elif result == "3":
                match.result = match.assign_result()
                continue
            else:
                continue
        else:
            break


def access_saved_data():
    """accéder aux données sauvegardées"""
    while True:
        clear_console()
        display_menu_saved_data()
        option = choose_option()
        if option == "1":  # Joueurs enregistrés
            json_file = "data/players.json"
            check_existence_json_file(json_file)
            with open(json_file, "r", encoding="utf-8") as file:
                players_data = json.load(file)
                players = [Player(**data) for data in players_data]
                display_menu_saved_data_registered_players()
                option = choose_option()
                if option == "1":
                    sorted_players = sort_players(players, "national_player_number")
                elif option == "2":
                    sorted_players = sort_players(players)

                display_players_list(sorted_players)
                break_point()
        elif option == "2":  # Tournois enregistrés
            loaded_tournament = reload_tournament("ended")
            if loaded_tournament:
                tournament = Tournament(loaded_tournament["name"], loaded_tournament["place"])
                tournament.load(loaded_tournament)
                display_all_tournament(tournament)
        else:
            break


def reload_tournament(criterion="all"):
    """
    Reloads a tournament based on the specified criterion and allows the user to select one from the list.

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
    tournaments = find_tournaments(criterion)
    index = display_reload_tournament(tournaments)
    if index != "":
        loaded_tournament = tournaments[int(index) - 1]
        return loaded_tournament
    else:
        return


if __name__ == "__main__":
    run()
