import json

from models import Tournament, Player, find_player_in_json, write_new_player_in_json, check_existence_json_file, \
    sort_players, find_tournaments
from views import (
    display_menu, choose_option, display_menu_tournament, display_tournament_start, display_menu_tournament_config,
    ask_national_player_number, player_in_database, player_not_in_database, display_menu_add_player, clear_console,
    display_menu_saved_data, display_menu_add_player_to_tournament, display_players_list, validate_round_creation,
    display_no_players_added_warning, display_menu_saved_data_registered_players, display_assign_match_result,
    display_warning_message_tournament_end, display_matchs, display_add_round_first_warning, display_match_menu,
    display_warning_no_new_players_will_be_able_to_register, display_tournament_creation_message,
    display_confirm_tournament_creation, display_valid_result, display_round_ended_warning,
    display_options_menu, change_tournament_name, change_tournament_place, change_tournament_description,
    change_tournament_max_round, display_add_player_message, display_player_already_registered,
    display_finish_round_first_warning, display_validate_result_menu, display_tournament_ended,
    display_reload_tournament, display_confirm_tournament_loaded, display_all_tournament,
    display_wrong_players_number_message
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


def add_player_database():
    """add a player to Jsonfile 'data/players.json'."""
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
                elif option == "3":
                    print("""Quel ordre:
                            1- Décroissant
                            2- Croissant
                            """)
                    option = choose_option()
                    if option == "1":
                        sorted_players = sort_players(players, "score")
                    else:
                        sorted_players = sort_players(players, "score", True)
                display_players_list(sorted_players)
                input()
        elif option == "2":  # Tournois enregistrés
            loaded_tournament = reload_tournament()
            if loaded_tournament:
                tournament = Tournament(loaded_tournament["name"], loaded_tournament["place"])
                tournament.load(loaded_tournament)
                display_all_tournament(tournament)
        else:
            break


# démarrer le tournoi
def run_tournament(tournament):
    """create tournament instance"""

    while True:
        clear_console()
        display_menu_tournament_config()
        option = choose_option()

        if option == "1":  # Ajouter les joueurs
            if len(tournament.rounds) == 0:
                add_player_to_tournament(tournament)
            else:
                display_no_players_added_warning()
        elif option == "2":  # voir la liste des joueurs inscrits
            display_players_list(tournament.players)
        elif option == "3":  # Démarrer le tour suivant.
            if len(tournament.players) % 2 == 0:
                if len(tournament.rounds) == 0 or tournament.rounds[-1].ended is True:
                    add_round_to_tournament(tournament)
                else:
                    display_finish_round_first_warning()
            else:
                display_wrong_players_number_message()
        elif option == "4":  # Voir les matchs en cours.
            if len(tournament.rounds) != 0:
                display_match_menu(tournament.rounds[-1].matchs)
            else:
                display_add_round_first_warning()
        elif option == "5":  # Entrer des résultats.
            if not tournament.rounds[-1].ended:
                validate_results(tournament)
                if tournament.round_number > tournament.max_round:
                    display_tournament_ended(tournament)
                    tournament.ended()
                    tournament.save()
                    break
            else:
                display_matchs(tournament.rounds[-1].matchs)
                display_round_ended_warning()
        elif option == "6":  # options
            display_options_menu()
            option = choose_option()
            if option == "1":  # change name
                tournament.change_name(change_tournament_name())
            if option == "2":  # change lieu
                tournament.change_place(change_tournament_place())
            if option == "3":  # change description
                tournament.change_descritpion(change_tournament_description())
            if option == "4":  # change le nombre maximum de tour
                tournament.change_max_round(change_tournament_max_round())
        else:  # Suspendre le tournoi
            tournament.save()
            break


# ajouter des joueurs au tournoi a partir de la base de donnée
def add_player_to_tournament(tournament):
    """ajoute des joueurs à un tournoi"""
    clear_console()
    display_add_player_message()
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

            if player:
                display_menu_add_player_to_tournament(player)
            else:
                player = create_new_player(player_number)
                display_menu_add_player_to_tournament(player)
    input()


# ajouter les joueurs qui ne sont pas dans la base de donnée
def create_new_player(player_number):
    """create and save new player in Json file"""
    data = player_not_in_database(player_number)
    new_player = Player(**data)
    write_new_player_in_json(new_player)
    display_players_list([new_player])
    return new_player


# itération sur le nbre de tour
def add_round_to_tournament(tournament):
    """ajoute un tour au tournoi"""
    if len(tournament.rounds) == int(tournament.max_round)+1:
        display_warning_message_tournament_end()
    else:
        if len(tournament.rounds) == 0:
            display_warning_no_new_players_will_be_able_to_register()
        else:
            validate_round_creation()
        while True:
            option = choose_option()
            if option == "1":
                tournament.add_round()
                tournament.rounds[-1].add_match(tournament.rounds)
                if len(tournament.rounds[-1].matchs) != len(tournament.players)/2:
                    print("solution 2")
                    input('')
                    tournament.rounds[-1].players = sort_players(tournament.rounds[-1].players, "score")
                    display_players_list(tournament.rounds[-1].players)
                    tournament.rounds[-1].add_match(tournament.rounds)
                display_tournament_creation_message()
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

        match_number = display_validate_result_menu(tournament.rounds[-1].matchs, match_without_result)
        if match_number != '' or match_number > len(tournament.rounds[-1].matchs):
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
