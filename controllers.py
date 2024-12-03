import json
from models import Tournament, Player, find_player_in_json, write_new_player_in_json, check_existence_json_file, \
    sort_players
from views import (display_menu, choose_option, display_menu_tournament, display_tournament_start,
                   display_menu_tournament_config, ask_national_player_number, player_in_database,
                   player_not_in_database, display_menu_add_player, clear_console, display_menu_saved_data,
                   display_menu_add_player_to_tournament, display_players_list, display_no_players_added,
                   display_menu_saved_data_registered_players, validate_round_creation, display_tournament_end,
                   display_match, display_add_round_first, display_warning_no_new_players_will_be_able_to_register,
                   display_tournament_creation_message, display_choose_match, display_assign_match_result,
                   display_confirm_tournament_creation,display_valid_result, display_round_ended_message)


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
        else:  # Quitter le programme
            break


def manage_tournament_options():
    """menu pour options de tournoi """
    while True:
        clear_console()
        display_menu_tournament()
        option = choose_option()
        if option == "1":  # Démarrer un nouveau tournoi
            run_tournament()
        elif option == "2":  # Reprendre un tournoi
            pass
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
                    sorted_players = sort_players(players, "score")

                display_players_list(sorted_players)
                input()
        elif option == "2":  # Tournois enregistrés
            pass
        else:
            break


def run_tournament():
    """create tournament instance"""
    data = display_tournament_start()
    if data["round_number"] == "":
        data["round_number"] = 4

    tournament = Tournament(data["name"], data["place"], data["description"], int(data["round_number"]))
    while True:
        clear_console()
        display_confirm_tournament_creation()
        display_menu_tournament_config()
        option = choose_option()
        if option == "1":  # Ajouter les joueurs
            if len(tournament.rounds) == 0:
                add_player_to_tournament(tournament)
            else:
                display_no_players_added()
        elif option == "2":
            display_players_list(tournament.players)
        elif option == "3":  # Démarrer le tour suivant.
            add_round_to_tournament(tournament)
        elif option == "4":  # Voir les matchs en cours.
            if tournament.rounds[-1]:
                display_match(tournament.rounds[-1].matchs)
            else:
                display_add_round_first()
        elif option == "5":  # Entrer des résultats.
            if not tournament.rounds[-1].ended:
                validate_results(tournament)
            else:
                display_match(tournament.rounds[-1].matchs)
                display_round_ended_message()
        else:  # Suspendre le tournoi
            pass


def add_player_to_tournament(tournament):
    """ajoute des joueurs à un tournoi"""
    players_number = ask_national_player_number()

    for player_number in players_number:
        player = tournament.add_player(player_number)
        if player:
            display_menu_add_player_to_tournament(player)
        else:
            player = create_new_player(player_number)
            display_menu_add_player_to_tournament(player)


def create_new_player(player_number):
    """create and save new player in Json file"""
    data = player_not_in_database(player_number)
    new_player = Player(**data)
    write_new_player_in_json(new_player)
    display_players_list([new_player])
    return new_player


def add_round_to_tournament(tournament):
    """ajoute un tour au tournoi"""
    if len(tournament.rounds) == int(tournament.max_round):
        display_tournament_end()
    else:
        if len(tournament.rounds) == 0:
            display_warning_no_new_players_will_be_able_to_register()
        validate_round_creation()
        while True:
            option = choose_option()
            if option == "1":
                tournament.add_round()
                display_tournament_creation_message()
                break
            else:
                break

    # ajouter des joueurs au tournoi a partir de la base de donnée
    # ajouter les joueurs qui ne sont pas dans la base de donnée
    # démarrer le tournoi 
    # itération sur le nbre de tour 
    # génerer les paires pour le tour
    # aléatoire 1er tour
    # tri selon score pour suivant
    # sans doublons des matchs précédents.
    # création des matchs
    # entrer les résultats des matchs 
    # afficher un débrief du tournoi
    # liste des tours, et pour chaque tour liste des matchs


def validate_results(tournament):
    while not tournament.rounds[-1].ended:
        match_without_result = 0

        for match in tournament.rounds[-1].matchs:
            if match.result == [(match.player1, 0), (match.player2, 0)]:
                match_without_result += 1

        print(f"il reste {match_without_result} matchs en cours")
        display_match(tournament.rounds[-1].matchs)

        if match_without_result == 0:
            display_valid_result()
            option = choose_option()
            if option == "1":
                tournament.rounds[-1].ended = True
                break

        match_number = display_choose_match()
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


if __name__ == "__main__":
    run()
