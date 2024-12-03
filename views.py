import os
import re
from models import validate_national_player_number, validate_name, validate_birthday


def clear_console():
    # Vérifie le système d'exploitation
    if os.name == 'nt':  # Pour Windows
        os.system('cls')
    else:  # Pour macOS et Linux
        os.system('clear')


def display_menu():
    """welcome menu"""
    print("""Bienvenue dans votre outil de gestion de tournoi
          Que souhaitez vous faire?
          1- Gérer un tournoi. 
          2- Ajouter des joueurs à la base de donnée.
          3- données enregistrées         
          4- Quitter le programme
          """)


def choose_option():
    """select one option"""
    return input("Sélectionnez une option:")


def display_menu_tournament():
    """menu to organize tournaments"""
    print(""" Veuillez sélectionner une option
          1- Démarrer un nouveau tournoi
          2- Reprendre un tournoi
          3- Retour
          """)


def display_tournament_start():
    """request information to create a tournament"""
    print("""Créer un nouveau tournoi: """)
    name = input("Nom du tournoi :")
    place = input("Lieu du tournoi :")
    description = input("Description :")
    round_number = input("Nombre de tour :")
    return {"name": name, "place": place, "description": description, "round_number": round_number}


def display_confirm_tournament_creation():
    print("le tournoi à bien été créé.")


def display_menu_tournament_config():
    """menu to manage a tournament"""
    print("""Que voulez vous faire maintenant? 
            1- inscrire les joueurs.
            2- Voir les joueurs inscrits
            3- Démarrer le tour suivant.
            4- Voir les matchs en cours.
            5- Entrer des résultats.
            6- Suspendre le tournoi.
            """)


def ask_national_player_number():
    """asks for National Player Number"""
    players_number = []
    print("Vous pouvez entrer plusieurs numéros séparés d'une virgule")
    add_player_number = input("quel est le numéro du joueur? : ")
    pattern = r'\b[a-zA-Z]{2}\d{5}\b'
    extracted_players_number = re.findall(pattern, add_player_number)
    for number in extracted_players_number:
        players_number.append(validate_national_player_number(number))
    return players_number


def player_in_database(player):
    """displays the player information in the database"""
    print(f"Les informations du joueur N° {player.national_player_number} ont été trouvées")
    display_players_list([player])


def player_not_in_database(player_number):
    """asks for player information"""
    print(f"Aucun joueur, portant le N°{player_number} n'a été trouvé dans la base de données")
    print("Veuillez renseigner les informations suivantes:")
    name = validate_name(input("Nom du joueur : "))
    first_name = validate_name(input("Prénom du joueur : "))
    birthday = validate_birthday(input("date de naissance du joueur : "))
    return {"national_player_number": player_number, "name": name, "first_name": first_name, "birthday": birthday}


def display_no_players_added():
    """displays forbidden to add new player message"""
    print("""Vous ne pouvez pas inscrire de nouveau joueur en cours de tournoi.
        """)


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


def display_menu_add_player_to_tournament(player):
    """display """
    print(f"le joueur N° {player.national_player_number} a été inscrit au tournoi")


def display_players_list(players):
    """displays the player list in column"""
    header = f"{'NPN':<12} {'Nom':<15} {'Prénom':<15} {'Anniversaire':<12} {'Score':<6}"
    print(header)
    print("-" * len(header))

    for player in players:
        print(player)
    print("")


def display_warning_no_new_players_will_be_able_to_register():
    print("""Une fois le premier round lancé, Vous ne pourrez plus inscrire de nouveaux joueurs""")


def validate_round_creation():
    """shows players registered to start the round"""
    print("""Vous allez passer au round suivant.
            êtes vous sûr?
            1- Valider
            2- Retour
            """)


def display_tournament_end():
    print("""Le nombre de tour est atteint, le tournoi est terminé""")


def display_tournament_creation_message():
    print(""" Le tour a été généré, 
la liste des matchs est disponible.""")


def display_add_round_first():
    print("""Les matchs seront générer lorsque vous créerez un tour""")


def display_match(matchs):
    """displays the match list in column"""
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


def display_choose_match():
    return input ("Entrez un numéro de match (validez vide pour revenir) :")


def display_assign_match_result(match):
    print(f"""Quel est le résultat?
    1- {match.player1.name} {match.player1.first_name} est le gagnant
    2- {match.player2.name} {match.player2.first_name} est le gagnant
    3- Les joueurs ont fait match nul
    4- Retour
    """)


def display_valid_result():
    print("""Tous les matchs sont terminés. Voulez-vous valider ces résultats ?
        1- Oui
        2- Non
        """)


def display_round_ended_message():
    print(""""Les résultats de ce tour ont déjà été validés, ce tour est à présent terminé.
Créez un nouveau tour pour poursuivre le tournoi""")

