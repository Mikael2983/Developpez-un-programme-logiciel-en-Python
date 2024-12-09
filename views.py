import os
import re
from typing import List

from models import (validate_national_player_number, validate_name, validate_birthday, sort_players, Player, Match)


def clear_console():
    # Vérifie le système d'exploitation
    if os.name == 'nt':  # Pour Windows
        os.system('cls')
    else:  # Pour macOS et Linux
        os.system('clear')


def break_point():
    input()


def display_menu():
    """welcome menu"""
    print("""Bienvenue dans votre outil de gestion de tournoi
    --------------------------------------------
          Que souhaitez vous faire?
          1- Gérer un tournoi. 
          2- Ajouter des joueurs à la base de donnée.
          3- Données enregistrées         
          4- Quitter le programme
          """)


def choose_option():
    """select one option"""
    return input("Sélectionnez une option:")


def display_menu_tournament():
    """menu to organize tournaments"""
    print(""" GERER UN TOURNOI
    -------------------
    Veuillez sélectionner une option
          1- Démarrer un nouveau tournoi
          2- Reprendre un tournoi
          3- Retour
          """)


def display_tournament_start():
    """request information to create a tournament"""
    print(" CREER UN NOUVEAU TOURNOI ")
    print("--------------------------")
    print('')
    name = input("Nom du tournoi :")
    place = input("Lieu du tournoi :")
    description = input("Description (facultatif) :")
    max_round_number = input("Nombre de tour (4 par défaut) :")
    return {"name": name, "place": place, "description": description, "max_round_number": max_round_number}


def display_confirm_tournament_creation():
    print("Le tournoi a bien été créé.")


def display_confirm_tournament_loaded():
    print("Le tournoi a bien été chargé")


def display_menu_tournament_config():
    """menu to manage a tournament"""
    print("""Que voulez vous faire maintenant? 
            1- Inscrire les joueurs.
            2- Voir les joueurs inscrits
            3- Démarrer le tour suivant.
            4- Voir les matchs en cours.
            5- Entrer des résultats.
            6- Options.
            7- Suspendre le tournoi.
            """)


def ask_national_player_number():
    """asks for National Player Number"""
    players_number = []
    print("Vous pouvez entrer plusieurs numéros, séparés d'une virgule")
    print("")
    add_player_number = input("quel est le numéro du joueur? : ")
    pattern = r'\b[a-zA-Z]{2}\d{5}\b'
    extracted_players_number = re.findall(pattern, add_player_number)
    for number in extracted_players_number:
        players_number.append(validate_national_player_number(number))
    return players_number


def player_in_database(player: Player):
    """displays the player information in the database"""
    print(f"Les informations du joueur N° {player.national_player_number} ont été trouvées")
    display_players_list([player])


def player_not_in_database(player_number: str):
    """asks for player information"""
    print(f"Aucun joueur, portant le N°{player_number} n'a été trouvé dans la base de données")
    print("Veuillez renseigner les informations suivantes:")
    name = validate_name(input("Nom du joueur : "))
    first_name = validate_name(input("Prénom du joueur : "))
    birthday = validate_birthday(input("date de naissance du joueur : "))
    return {"national_player_number": player_number, "name": name, "first_name": first_name, "birthday": birthday}


def display_wrong_players_number_message():
    """display a warning if number of players  is not even"""
    print("le nombre de joueurs inscrits n'est pas pair, veuillez inscrire un autre joueur")
    input("")


def display_no_players_added_warning():
    """displays forbidden to add new player message"""
    print("""Vous ne pouvez pas inscrire de nouveau joueur en cours de tournoi.
        """)
    input("")


def display_add_player_message():
    """displays the title of the add a new player section"""
    print("INSCRIPTION DE NOUVEAU JOUEUR AU TOURNOI")
    print("----------------------------------------")


def display_menu_add_player():
    """Asks if there are other players to register"""
    print("""Voulez vous enregistrer un autre joueur?
            1- oui
            2- non
            """)


def display_menu_saved_data():
    """menu to access data categories"""
    print("""A quelles données voulez-vous accéder? 
            1- Joueurs enregistrés
            2- Anciens tournois
            3- Retour
            """)


def display_menu_saved_data_registered_players():
    """menu to select a sort criterion"""
    print("""veuillez sélectionner un critère de tri:
            1- Par numéro national de joueur
            2- Par nom
            3- Par score
            """)


def display_menu_add_player_to_tournament(player: Player):
    """
    displays a message confirming a player’s registration
    :param player: The `Player` object that has been registered to the tournament.
    :type player: Player
    """
    print(f"le joueur N° {player.national_player_number} a été inscrit au tournoi")


def display_player_already_registered(player: Player):
    """displays a warning message when a player is already registered"""
    print(f"le joueur N° {player.national_player_number} est déjà inscrit au tournoi")


def display_players_list(players: List[Player]):
    """
    displays the player list in column
    :param players: A list of `Player` objects to be displayed.
    :type players: list[Player]
    """
    header = f"{'NPN':<12} {'Nom':<15} {'Prénom':<15} {'Anniversaire':<12} {'Score':<6}"
    print(header)
    print("-" * len(header))
    for player in players:
        print(player)
    print("")
    input("")


def display_warning_no_new_players_will_be_able_to_register():
    """Warning that no new players will be able to register"""
    print("""Une fois le premier round lancé, Vous ne pourrez plus inscrire de nouveaux joueurs""")
    print("""les joueurs ont-ils été tous inscrits? 
                1- Valider
                2- Retour
                """)


def validate_round_creation():
    """shows players registered to start the round"""
    print("""passer au tour suivant? 
            1- Valider
            2- Retour
            """)


def display_finish_round_first_warning():
    """displays the warning that the previous round must be validated"""
    print("Un tour est déjà en cours.")
    print("Vous devez valider les résultats des matchs avant de passer au tour suivant")
    input("")


def display_warning_message_tournament_end():
    """displays a warning that the tournament is over"""
    print("""Le nombre de tour est atteint, le tournoi est terminé""")
    input("")


def display_tournament_creation_message():
    """displays the message confirming that the round is well started """
    print("""Le tour a été généré, la liste des matchs est disponible.""")
    input("")


def display_add_round_first_warning():
    """Warned that the round must be started before watching matches  """
    print("""Les matchs seront générés lorsque vous créerez un tour""")
    input("")


def display_matchs(matchs: List[Match]):
    """
    Displays a list of matches in a formatted columnar view.

    :param matchs: A list of `Match` objects to be displayed.
    :type matchs: list[Match]
    """
    header = f"{'match':<6} {'Nom':<15} {'Prénom':<15} {'Score':<6} {'':<4} {'Nom':<15} {'Prénom':<15} {'Score':<6}"
    print(header)
    print("-" * len(header))

    for match in matchs:
        var = [match.number,
               match.player1.name, match.player1.first_name, match.result[0][1],
               match.player2.name, match.player2.first_name, match.result[1][1]
               ]
        print(f"{var[0]:<6} {var[1]:<15} {var[2]:<15} {var[3]:<6} {'VS':<4} {var[4]:<15} {var[5]:<15} {var[6]:<6}")
    print("")


def display_match_menu(matchs: List[Match]):
    """displays the round list of matches"""
    print("Voici la liste des matchs en cours pour ce tour")
    display_matchs(matchs)
    input("")


def display_validate_result_menu(matchs: List[Match], match_without_result: int):
    """displays menu to choose the match to score"""
    print(f"il reste {match_without_result} matchs en cours")
    display_matchs(matchs)
    print("Pour enregistrer un résultat, entrez un")
    return input("numéro de match (validez vide pour revenir) :")


def display_assign_match_result(match):
    """displays the menu to choose the results of matches"""
    print(f"""Quel est le résultat?
    1- {match.player1.name} {match.player1.first_name} est le gagnant
    2- {match.player2.name} {match.player2.first_name} est le gagnant
    3- Les joueurs ont fait match nul
    4- Retour
    """)


def display_valid_result():
    """displays the menu to validate the entered results and thus the round"""
    print("""Tous les matchs sont terminés. Voulez-vous valider ces résultats ?
        1- Oui
        2- Non
        """)


def display_round_ended_warning():
    """displays a warning that the results cannot be modified"""
    print(""""Les résultats de ce tour ont déjà été validés, ce tour est à présent terminé.
Créez un nouveau tour pour poursuivre le tournoi""")
    input("")


def display_options_menu():
    """displays the editable settings selection menu"""
    print("""quel paramètre voulez vous modifier?
        1- Le nom du tournoi
        2- La localisation du tournoi
        3- La description du tournoi
        4- Le nombre de tour maximum
        5- Retour
        """)


def change_tournament_name():
    """requests a new name"""
    return input("Entrez le nouveau nom : ")


def change_tournament_place():
    """requests a new place"""
    return input("Entrez le nouveau lieu : ")


def change_tournament_description():
    """requests a new description"""
    return input("Entrez la nouvelle description : ")


def change_tournament_max_round():
    """requests a new maximum number of round"""
    return input("entrez le nouveau nombre de tour maximum : ")


def display_tournament_ended(tournament):
    print("Le tournoi est terminé")
    print("voici le classement final")
    display_players_list(sort_players(tournament.players,"score"))


def display_reload_tournament(tournaments):
    print("Voici la liste des tournois disponibles:")
    print("")
    header = (f"{'N°':<4} {'Name':<30} {'Place':<15} {'Start_date':<12} {'Max_round':<11} {'Round_number':<15} "
              f"{'Description':<45}")
    print(header)
    print("-" * len(header))
    for i, tournament in enumerate(tournaments):
        var = [tournament['name'], tournament['place'], tournament['start_date'], tournament['max_round'],
               tournament['round_number'], tournament['description']]
        print(f"{i+1:<4} {var[0]:<30} {var[1]:<15} {var[2]:<12} {var[3]:<11} {var[4]:<15} {var[5]:<45}")
    print("")
    return input("Quel tournoi voulez-vous importer?")


def display_all_tournament(tournament):
    print(f"""Voici les détails du tournoi {tournament.name} qui a eu lieu à {tournament.place}, 
    le {tournament.start_date}
Etait inscrit : """)

    display_players_list(sort_players(tournament.players, "name", False))

    for i in range(len(tournament.rounds)):
        print(f"Round {i+1}")
        display_matchs(tournament.rounds[i].matchs)

    input("")
