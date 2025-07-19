import traceback
import curses
import re
from stream_handler import StreamHandler
from api_requests import request_textgen
from text_processing import (extraire_dialogues_et_actions, 
                             handle_message,
                             handle_answer)
from audio_utils import (generate_audio, 
                         play_audio)
from config import (characters, 
                    get_current_character,
                    debug_mode)
from commands import handle_commands

# Couleurs ANSI pour affichage en console
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"

def interactive_choice(assistant_message):
    """
    Extrait les lignes contenant "[chois]" et lance une interface curses
    pour permettre à l'utilisateur de sélectionner une option avec les flèches.
    """
    # On cherche les lignes contenant "[chois" (insensible à la casse)
    lines = assistant_message.splitlines()
    options = []
    for line in lines:
        if re.search(r'\[.*chois.*\]', line, re.IGNORECASE):
            # On supprime le marqueur "->" s'il existe et on nettoie la ligne
            option = line.replace("->", "").strip()
            options.append(option)
    if not options:
        return None

    def curses_choice(stdscr):
        curses.curs_set(0)  # cache le curseur
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        current_index = 0
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Utilisez les flèches pour sélectionner, Entrée pour confirmer:\n", curses.color_pair(1))
            for idx, option in enumerate(options):
                if idx == current_index:
                    stdscr.addstr(idx + 2, 0, "-> " + option, curses.A_REVERSE)
                else:
                    stdscr.addstr(idx + 2, 0, "   " + option)
            key = stdscr.getch()
            if key == curses.KEY_UP and current_index > 0:
                current_index -= 1
            elif key == curses.KEY_DOWN and current_index < len(options) - 1:
                current_index += 1
            elif key in [10, 13]:  # touche Entrée
                return options[current_index]
    return curses.wrapper(curses_choice)

def chat() -> None:
    character_config = characters[get_current_character()]
    print(character_config)
    
    # Choix des modes d'entrée et de sortie
    while (input_mode := input(YELLOW + "Choisissez le type d'entrée:\n1: Texte\n2: Speech\nchoix: " + RESET)) not in ("1", "2"):
        print(RED + "Choix invalide" + RESET)
    while (output_mode := input(YELLOW + "Choisissez le type de sortie:\n1: Texte\n2: Speech\nchoix: " + RESET)) not in ("1", "2"):
        print(RED + "Choix invalide" + RESET)

    handler = StreamHandler() if input_mode == '2' else None

    if debug_mode >= 2:
        print(BLUE + f"DEBUG: input_mode: {input_mode}, output_mode: {output_mode}, debug_mode: {debug_mode}" + RESET)

    next_input = None  # permet de relayer directement un choix interactif

    while True:
        try:
            # PART 1 : récupération de l'entrée utilisateur
            if next_input is None:
                if input_mode == '1':
                    user_input = input("\n> ").strip() 
                else:
                    user_input = handler.listen()
            else:
                user_input = next_input
                next_input = None

            if user_input and debug_mode >= 2:
                print(BLUE + "DEBUG: Message utilisateur: " + RESET, user_input)
            elif not user_input:
                continue

            if input_mode == '1' and user_input.startswith("!"):
                handle_commands(user_input)
                continue

            processed_message = handle_message(user_input)
            if debug_mode >= 2:
                print(BLUE + "DEBUG: Message traité: " + RESET, processed_message)

            # PART 2 : envoi de la requête à l'IA
            assistant_message = request_textgen(processed_message, debug=debug_mode)
            if debug_mode >= 2:
                print(BLUE + "DEBUG: Réponse brute de l'assistant: " + RESET, assistant_message)

            assistant_message = handle_answer(response=assistant_message, StS=(input_mode=='2'))
            if debug_mode >= 2:
                print(BLUE + "DEBUG: Message assistant traité: " + RESET, assistant_message)
            
            # PART 3 : affichage de la réponse
            if output_mode == '1':
                print(GREEN + assistant_message + RESET)
            else:
                dialogue, action = extraire_dialogues_et_actions(assistant_message)
                if debug_mode >= 2:
                    print(BLUE + "DEBUG: Dialogue et action: " + RESET, dialogue, action)
                generate_audio(dialogue=dialogue, debug=debug_mode)
                play_audio()

            # Si des choix interactifs sont présents dans le message, on lance l'interface de sélection
            if re.search(r'\[.*chois.*\]', assistant_message, re.IGNORECASE):
                selected = interactive_choice(assistant_message)
                print(GREEN + "Vous avez choisi: -> " + selected + RESET)
                next_input = selected  # ce choix sera envoyé lors de la prochaine itération

        except KeyboardInterrupt:
            print(YELLOW + "\nFin du programme." + RESET)
            break
        except Exception as e:
            print(RED + "Erreur: " + str(e) + RESET)
            traceback.print_exc()

if __name__ == '__main__':
    chat()
