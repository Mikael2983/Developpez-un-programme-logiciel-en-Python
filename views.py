import os
import re
from typing import List, Union
from rich import print
from rich.console import Console
from rich.table import Table

from models import Player, Match, Round, DataBase
from settings import (TITLE_STYLE,
                      LINE_STYLE,
                      ERROR_STYLE,
                      SUCCESS_STYLE,
                      TEXT_STYLE,
                      REQUEST_STYLE,
                      INFORMATION_STYLE)


class TournamentView:

    def __init__(self):
        self.data_base_view = DataBaseView()
        self.application_view = ApplicationView()
        self.data_base = DataBase()
        self.console = Console()

    @staticmethod
    def display_menu_tournament():
        """menu to organize tournaments"""
        header = "  GERER UN TOURNOI  "
        request = "Sélectionnez une option?"
        text = ["1- Démarrer un nouveau tournoi",
                "2- Reprendre un tournoi",
                "3- Retour"]
        display_styled_menu(header, request, text)

    def display_tournament_start(self) -> dict:
        """
        Prompts the user to input the information of the tournament

        :return: A dictionary containing the tournament's details:
                    name, place, description, and max_round_number.
        :rtype: dict
        """
        header = "  CREER UN NOUVEAU TOURNOI  "
        request = "Veuillez renseigner les informations suivantes:"
        display_styled_menu(header, request, [])
        name = self.console.input(
            apply_rich_style("Nom du tournoi :", TEXT_STYLE))
        place = self.console.input(
            apply_rich_style("Lieu du tournoi :", TEXT_STYLE))
        description = self.console.input(
            apply_rich_style(
                "Description (facultatif) :",
                TEXT_STYLE))
        while True:
            max_round_number = self.console.input(
                apply_rich_style(
                    "Nombre de tour (4 par défault) :",
                    TEXT_STYLE))
            if max_round_number.isdigit() or max_round_number == '':
                break

        return {"name": name,
                "place": place,
                "description": description,
                "max_round_number": max_round_number
                }

    def display_confirm_tournament_creation(self):
        print(apply_rich_style("Le tournoi a bien été créé.", SUCCESS_STYLE))
        self.application_view.break_point()

    @staticmethod
    def display_confirm_tournament_loaded():
        print(apply_rich_style("Le tournoi a bien été chargé", SUCCESS_STYLE))

    @staticmethod
    def display_wrong_players_number_message():
        """display a warning if number of players  is not even"""
        print(apply_rich_style(
            "Le nombre de joueurs inscrits n'est pas pair.",
            ERROR_STYLE
        )
        )
        print(apply_rich_style(
            "Veuillez inscrire un autre joueur.",
            REQUEST_STYLE
        )
        )
        input("")

    @staticmethod
    def display_add_player_message():
        """displays the title of the add a new player section"""
        header = " INSCRIPTION DE NOUVEAUX JOUEURS AU TOURNOI "
        display_styled_menu(header, None, [])

    @staticmethod
    def display_menu_add_player():
        """Asks if there are other players to register"""
        request = "Sélectionnez une option :"
        text = ["1- Ajouter des joueurs", "2- Commencer le 1er Tour"]
        display_styled_menu(None, request, text)

    @staticmethod
    def display_player_already_registered(player: Player):
        """displays a warning message when a player is already registered"""
        colored_text = apply_rich_style(
            player.national_player_number,
            REQUEST_STYLE)
        print(apply_rich_style(
            f"le joueur N°{colored_text} est déjà inscrit au tournoi",
            ERROR_STYLE
        )
        )

    @staticmethod
    def display_assign_match_result(match: Match):
        """
        Displays a menu for assigning the result of a match.

        The user can select:
        - The winner (player 1 or player 2),
        - A draw,
        - Or return to the previous menu.

        :param match: The match for which the result is being assigned.
        :type match: Match
        :return: The user's choice as a string (1, 2, 3, or 4).
        :rtype: str
        """
        request = "Quel est le résultat?"
        text = [f"1- {apply_rich_style(
            f"{match.player1.name} {match.player1.first_name}",
            SUCCESS_STYLE)} est le gagnant.",
                f"2- {apply_rich_style(
                    f"{match.player2.name} {match.player2.first_name}",
                    SUCCESS_STYLE)} est le gagnant.",
                "3- Les joueurs ont fait match nul.",
                "4- Retour."]
        display_styled_menu(None, request, text)

    def display_validate_result_menu(self,
                                     current_round: Round,
                                     match_without_score: int) \
            -> str:
        """
        Displays a menu for selecting a match to record its result.

        :param current_round: The current round whose matches are being scored.
        :type current_round: Round
        :param match_without_score: The number of matches without score.
        :type match_without_score: int
        :return: The match number entered by the user, or an empty string.
        :rtype: str
        """
        colored_text = apply_rich_style(
            f"{current_round.round_number}",
            REQUEST_STYLE
        )
        print(apply_rich_style(
            f"TOUR N° {colored_text}.",
            TITLE_STYLE
        )
        )
        colored_text = apply_rich_style(
            f"{match_without_score}",
            REQUEST_STYLE
        )
        print(apply_rich_style(
            f"Il reste {colored_text} matchs en cours",
            TEXT_STYLE
        )
        )
        self.data_base_view.display_matchs(
            current_round.matchs,
            "listes des matchs en cours"
        )
        print(apply_rich_style(
            "Pour enregistrer un résultat,",
            REQUEST_STYLE
        )
        )
        return self.console.input(apply_rich_style(
            "entrez un numéro de match: ",
            REQUEST_STYLE
        )
        )

    def display_match_menu(self, current_round: Round):
        """
        Displays the list of matches for the given round.

        :param current_round: The current round whose matches are
                                being displayed.
        :type current_round: Round
        """

        colored_text = f"{current_round.round_number}"
        print(apply_rich_style(
            f"Voici la liste des matchs pour le tour {colored_text}.",
            TEXT_STYLE))
        self.data_base_view.display_matchs(
            current_round.matchs,
            f"liste des matchs pour le tour {current_round.round_number}"
        )

    @staticmethod
    def display_valid_result():
        """displays the menu to validate the entered results
            and thus the round"""
        print(apply_rich_style(
            "Tous les matchs sont terminés.",
            SUCCESS_STYLE
            )
        )
        request = "Voulez-vous valider ces résultats ?"
        text = ["1- Oui.", "2- Non."]
        display_styled_menu(None, request, text)

    def display_tournament_ended(self, tournament):
        """
        Displays the final standings and round details for a completed
        tournament.

        The function includes:
        - A message indicating the tournament is finished.
        - A final ranking of players, sorted by their score in descending
            order.
        - Details of all rounds played during the tournament.

        :param tournament: The tournament to display, which must include
                            players and rounds.
        :type tournament: Tournament
        """
        print(apply_rich_style(
            "Le tournoi est terminé",
            SUCCESS_STYLE
        ))
        print(apply_rich_style(
            "Voici le classement final",
            TEXT_STYLE
        ))
        self.data_base_view.display_players_score(
            self.data_base.sort_players(
                tournament.players,
                "score",
                True
            ),
            "liste des joueurs classée par score"
        )
        print(apply_rich_style(
            "voici le détail des tours joués",
            TEXT_STYLE
        ))
        self.data_base_view.display_all_round(tournament)


class DataBaseView:

    def __init__(self):
        self.console = Console()
        self.data_base = DataBase()

    def ask_national_player_number(self) -> list[str]:
        """
        Prompts the user to input one or more National Player Numbers.

        Users can enter multiple player numbers separated by commas.
        The function validates each number against the pattern
        `r"[a-zA-Z]{2}\\d{5}"` and returns a list of valid
        player numbers after applying further validation.

        :return: A list of valid National Player Numbers.
        :rtype: list[str]
        """
        players_number = []
        print(apply_rich_style(
            "Vous pouvez entrer plusieurs numéros, séparés d'une virgule",
            INFORMATION_STYLE
        ))
        print("")
        add_player_number = self.console.input(
            apply_rich_style(
                "quel est le numéro du joueur? : ",
                REQUEST_STYLE
            )
        )
        pattern = r'\b[a-zA-Z]{2}\d{5}\b'
        extracted_players_number = re.findall(pattern, add_player_number)
        for number in extracted_players_number:
            players_number.append(self.validate_national_player_number(number))
        return players_number

    def player_in_database(self, player: Player):
        """
        displays the player's information in the database

        :param player: one instance of player
        :type player:  Player
        """
        colored_text = apply_rich_style(
            f"{player.national_player_number}",
            REQUEST_STYLE
        )
        print(apply_rich_style(
            f"Les informations du joueur N°{colored_text} ont été trouvées",
            SUCCESS_STYLE
        ))
        self.display_players_list(
            [player],
            "informations du joueur"
        )

    def player_not_in_database(self, player_number: str) -> dict:
        """
        Prompts the user to input information for a player not found in
        the database.

        :param player_number: The national player number of the player.
        :type player_number: str
        :return: A dictionary containing the player's details:
                    - national player number,
                    - name,
                    - first name,
                    - and birthday.
        :rtype: dict
        """
        colored_text = apply_rich_style(f"{player_number}", SUCCESS_STYLE)
        print(apply_rich_style(
            f"Aucun joueur, portant le N°{colored_text} n'a été trouvé "
            f"dans la base de données",
            ERROR_STYLE
        ))
        print(apply_rich_style(
            "Veuillez renseigner les informations suivantes:",
            REQUEST_STYLE
        ))
        name = self.validate_name(self.console.input(
            apply_rich_style(
                "Nom du joueur : ",
                TEXT_STYLE
            )
        ))
        first_name = self.validate_name(self.console.input(
            apply_rich_style(
                "Prénom du joueur : ",
                TEXT_STYLE
            )
        ))
        birthday = self.validate_birthday(self.console.input(
            apply_rich_style(
                "Date de naissance du joueur : ",
                TEXT_STYLE
            )
        ))

        return {
            "national_player_number": player_number,
            "name": name,
            "first_name": first_name,
            "birthday": birthday
        }

    def validate_name(self, name: str) -> str:
        """
        Validates and formats a given name or surname. Automatically corrects
        formatting errors when possible (e.g., 'dupont' -> 'Dupont').

        :param name: The name or surname to validate.
        :type name: str
        :raises ValueError: If the name contains invalid characters.
        :return: The validated and formatted name with the first letter
                capitalized.
        :rtype: str
        """
        try:
            if re.match(r"^[a-zA-ZÀ-ÖØ-öø-ÿ-]+$", name, re.UNICODE):
                return name.title()  # Corrige en "Majuscule initiale"
            raise ValueError(
                f"Le nom {apply_rich_style(name, TEXT_STYLE)} "
                f"contient des caractères non valides."
            )
        except ValueError as e:
            print(apply_rich_style(str(e), ERROR_STYLE))
            corrected = self.console.input(
                apply_rich_style(
                    "Veuillez entrer un nom valide:",
                    REQUEST_STYLE
                )
            )
            return self.validate_name(corrected)  # Revalide la nouvelle entrée

    def validate_national_player_number(self,
                                        national_player_number: str) \
            -> str:
        """
        Validates the national player number format. Prompts the user for a
        correction if the input is invalid.

        :param national_player_number: The national player number to validate,
                                        expected in the format 'aa11111'.
        :type national_player_number: str
        :raises ValueError: If the input does not match the expected format
                            (two lowercase letters followed by five digits).
        :return: The validated national player number in lowercase format.
        :rtype: str
        """
        player_number = national_player_number.lower()
        try:
            if re.match(r"^[a-z]{2}\d{5}$", player_number):
                return player_number
            raise ValueError(
                f"Le numéro {apply_rich_style(national_player_number,
                                              TEXT_STYLE)}"
                f" n'est pas valide."
                "Il doit être sous la forme de deux lettres minuscules "
                "suivies de 5 chiffres."
            )
        except ValueError as e:
            print(apply_rich_style(str(e), ERROR_STYLE))
            corrected = self.console.input(
                apply_rich_style(
                    "Veuillez entrer un numéro valide. ex: aa11111 :",
                    REQUEST_STYLE
                )
            )
            return self.validate_national_player_number(corrected)

    def validate_birthday(self, birthday: str) -> str | None:
        """
        Validate and format a birthday string. Corrects the format if necessary
        and prompts the user for input in case of an error.

        :param birthday: The birthday string to validate, expected in the
                            format 'dd-mm-yyyy' or 'dd/mm/yyyy'.
        :type birthday: str
        :raises ValueError: If the input birthday cannot be parsed or
                            corrected.
        :return: The validated and formatted birthday string, in the format
                'dd/mm/yyyy'.
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
            print(apply_rich_style(str(e), ERROR_STYLE))
            corrected = self.console.input(
                apply_rich_style(
                    "Veuillez entrer une date valide. ex: dd/mm/aaaa : ",
                    REQUEST_STYLE
                )
            )
            return self.validate_birthday(corrected)

    @staticmethod
    def display_title_add_player_to_database():
        header = " AJOUTER UN JOUEUR A LA BASE DE DONNEES "
        display_styled_menu(header, None, [])

    @staticmethod
    def display_menu_add_player_to_database():
        request = "Sélectionnez une option :"
        text = ["1- Ajouter un autre joueur", "2- Retour"]
        display_styled_menu(None, request, text)

    @staticmethod
    def display_menu_saved_data():
        """menu to access data categories"""
        header = " DONNEES ENREGISTREES "
        request = "A quelles données voulez-vous accéder?"
        text = ["1- Joueurs enregistrés", "2- Anciens tournois", "3- Retour"]
        display_styled_menu(header, request, text)

    @staticmethod
    def display_menu_registered_players():
        """menu to select a sort criterion"""
        header = " JOUEURS ENREGISTRES "
        request = "Veuillez sélectionner un critère de tri:"
        text = ["1- Par numéro national de joueur",
                "2- Par nom"]
        display_styled_menu(header, request, text)

    def display_players_score(self, players: List[Player], title: str):
        """
        displays the player list in column
        :param players: A list of `Player` objects to be displayed.
        :type players: list[Player]
        :param title:  table title to display
        :type title: string
        """
        table = Table(title=title,
                      title_style=TITLE_STYLE,
                      header_style=REQUEST_STYLE
                      )

        table.add_column(
            "N.P.N.",
            justify="center",
            style=TEXT_STYLE,
            max_width=10
        )
        table.add_column(
            "Nom",
            justify="center",
            style=SUCCESS_STYLE,
            max_width=15
        )
        table.add_column(
            "Prénom",
            justify="center",
            style=SUCCESS_STYLE,
            max_width=15
        )
        table.add_column(
            "Score",
            justify="center",
            style=TEXT_STYLE,
            max_width=12)

        for player in players:
            table.add_row(
                player.national_player_number,
                player.name,
                player.first_name,
                str(player.score)
            )

        self.console.print(table)

    def display_players_list(self, players: List[Player], title: str):
        """
        displays the player list in column
        :param players: A list of `Player` objects to be displayed.
        :type players: list[Player]
        :param title:  table title to display
        :type title: string
        """
        table = Table(title=title,
                      title_style=TITLE_STYLE,
                      header_style=REQUEST_STYLE
                      )

        table.add_column(
            "N.P.N.",
            justify="center",
            style=TEXT_STYLE,
            max_width=10
        )
        table.add_column(
            "Nom",
            justify="center",
            style=SUCCESS_STYLE,
            max_width=15
        )
        table.add_column(
            "Prénom",
            justify="center",
            style=SUCCESS_STYLE,
            max_width=15
        )
        table.add_column(
            "Date de naissance",
            justify="center",
            style=TEXT_STYLE,
            max_width=12)

        for player in players:
            table.add_row(
                player.national_player_number,
                player.name,
                player.first_name,
                player.birthday
            )

        self.console.print(table)

    def display_matchs(self, matchs: List[Match], title: str):
        """
        Displays a list of matches in a formatted columnar view.

        :param matchs: A list of `Match` objects to be displayed.
        :type matchs: list[Match]
        :param title:  table title to display
        :type title: string
        """
        table = Table(title=title,
                      title_style=TITLE_STYLE,
                      header_style=REQUEST_STYLE
                      )
        table.add_column(
            "match", justify="center", style=TEXT_STYLE, max_width=6)
        table.add_column(
            "Nom", justify="center", style=SUCCESS_STYLE, max_width=15)
        table.add_column(
            "Prénom", justify="center", style=SUCCESS_STYLE, max_width=15)
        table.add_column(
            "Score", justify="center", style=TEXT_STYLE, max_width=6)
        table.add_column(
            "VS", justify="center", style=ERROR_STYLE, max_width=4)
        table.add_column(
            "Nom", justify="center", style=SUCCESS_STYLE, max_width=15)
        table.add_column(
            "Prénom", justify="center", style=SUCCESS_STYLE, max_width=15)
        table.add_column(
            "Score", justify="center", style=TEXT_STYLE, max_width=6)

        for match in matchs:
            table.add_row(str(match.number),
                          match.player1.name,
                          match.player1.first_name,
                          str(match.result[0][1]),
                          "",
                          match.player2.name,
                          match.player2.first_name,
                          str(match.result[1][1])
                          )

        self.console.print(table)

    def display_reload_tournament(self, tournaments) -> str:
        """
            Displays a list of available tournaments and prompts the user to
            select one.

            Each tournament's details are displayed in a tabular format with
            the following columns:
            - Index number
            - Tournament name
            - Location
            - Start date
            - Maximum number of rounds
            - Current round number
            - Description

            :param tournaments: A list of dictionaries representing
                                tournaments.
             Each dictionary should have the keys:
                    - 'name',
                    - 'place',
                    - 'start_date',
                    - 'max_round',
                    - 'round_number',
                    - 'description'.
            :type tournaments: list[dict]
            :return: The user-selected tournament index as a string.
            :rtype: str
            """
        table = Table(title="listes des tournois disponibles",
                      title_style=TITLE_STYLE,
                      header_style=TEXT_STYLE
                      )
        table.add_column(
            "N°", justify="center", style=TEXT_STYLE, max_width=6)
        table.add_column(
            "Nom", justify="center", style=TEXT_STYLE, max_width=30)
        table.add_column(
            "Lieu", justify="center", style=TEXT_STYLE, max_width=15)
        table.add_column(
            "date de début", justify="center", style=TEXT_STYLE, max_width=12)
        table.add_column(
            "Ronde", justify="center", style=TEXT_STYLE, max_width=7)
        table.add_column(
            "Statut", justify="center", max_width=15)
        table.add_column(
            "description",
            justify="center",
            style=TEXT_STYLE,
            max_width=45,
            overflow="fold")

        for i, tournament in enumerate(tournaments):
            if tournament["end_date"]:
                statut = "[red]ENDED[/red]"
            else:
                statut = "[green]IN PROGRESS[/green]"
            tournament_number = str(i + 1)
            table.add_row(tournament_number,
                          tournament['name'],
                          tournament['place'],
                          tournament['start_date'],
                          str(tournament['max_round']),
                          statut,
                          tournament['description'])
        self.console.print(table)
        return self.console.input(apply_rich_style(
            "Quel tournoi voulez-vous importer?",
            REQUEST_STYLE
        ))

    def display_all_tournament(self, tournament):
        """
        Displays the details of a tournament, including its name, location,
        start date, list of players, and all rounds with their matches.

        :param tournament: The tournament whose details are to be displayed.
        :type tournament: Tournament
        """
        data = [apply_rich_style(
                    f"{tournament.name}",
                    REQUEST_STYLE
                ),
                apply_rich_style(
                    f"{tournament.place}",
                    REQUEST_STYLE
                ),
                apply_rich_style(
                    f"{tournament.start_date}",
                    REQUEST_STYLE
                )]
        print(apply_rich_style(
            f"Voici les détails du tournoi {data[0]} "
            f"qui a eu lieu à {data[1]}, le {data[2]}",
            TEXT_STYLE
        ))

        self.display_players_score(
            self.data_base.sort_players(
                tournament.players,
                "score",
                False
            ),
            "listes des joueurs participants"
        )
        self.display_all_round(tournament)

    def display_all_round(self, tournament):
        """
        Displays all the rounds of a tournament along with their matches.

        For each round, the matches are displayed in a formatted list.
        The user can pause after each round to review the information.

        :param tournament: The tournament whose rounds are to be displayed.
        :type tournament: Tournament
        """

        for i in range(len(tournament.rounds)):
            print(apply_rich_style(
                f"Round {apply_rich_style(f"{i+1}",
                                          REQUEST_STYLE)}",
                TEXT_STYLE
            ))
            self.display_matchs(
                tournament.rounds[i].matchs,
                f"liste des matchs du tour "
                f"{tournament.rounds[i].round_number}"
            )

        input("")


class ApplicationView:
    @staticmethod
    def display_menu():
        """welcome menu"""
        header = "Bienvenue dans votre outil de gestion de tournoi"
        request = "Que souhaitez vous faire?"
        text = ["1- Gérer un tournoi.",
                "2- Ajouter des joueurs à la base de donnée.",
                "3- Données enregistrées.",
                "4- Quitter le programme."
                ]
        display_styled_menu(header, request, text)

    @staticmethod
    def choose_option() -> str:
        """select one option"""
        console = Console()

        return console.input(apply_rich_style(
            "Sélectionnez une option?",
            REQUEST_STYLE
        ))

    @staticmethod
    def clear_console():
        if os.name == 'nt':  # Pour Windows
            os.system('cls')
        else:  # Pour macOS et Linux
            os.system('clear')

    @staticmethod
    def break_point():
        input()


def apply_rich_style(message: str, style: str) -> str:
    """
    Applies a Rich style to a message.

    This function wraps a given message with Rich markup tags to apply
    a specific style.

    :param message: The message to which the style will be applied.
    :type message: str
    :param style: The Rich style to apply (e.g., "bold", "italic", "red").
    :type style: str
    :return: The message wrapped with the specified Rich style tags.
    :rtype: str
    """
    return f"[{style}]{message}[/{style}]"


def display_styled_menu(
        header: Union[str, None],
        request: Union[str, None],
        text: list[str]):
    """
    Displays a stylized menu with a header, a request, and a list
    of text items.

    The function uses a `rich_style` function to apply styles to
    the header, request, and text.
    The header is displayed with an underline, and each text item
    is indented.

    :param header: The header text to display at the top of the menu.
                    If None, no header is displayed.
    :type header: str or None
    :param request: A request or prompt to display below the header.
                    If None, no request is displayed.
    :type request: str or None
    :param text: A list of strings to display as the body of the menu.
    :type text: list[str]
    """

    if header is not None:
        print(apply_rich_style(header, TITLE_STYLE))
        print(apply_rich_style("-" * len(header), LINE_STYLE))
    if request is not None:
        print(apply_rich_style(request, REQUEST_STYLE))
    for string in text:
        print(apply_rich_style(f"    {string}", TEXT_STYLE))
