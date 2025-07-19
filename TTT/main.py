__version__ = 163

import traceback
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

# Définition des couleurs ANSI
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"

def chat() -> None:
    character_config = characters[get_current_character()]
    print(character_config)
    
    while (input_mode := input(YELLOW + "Choisissez le type d'entrée:\n1: Texte\n2: Speech\nchoix: " + RESET)) not in (str(opt) for opt in range(1,3)):
        print(RED + "invalid input choice" + RESET)
    while (output_mode := input(YELLOW + "Choisissez le type de sortie:\n1: Texte\n2: Speech\nchoix: " + RESET)) not in (str(opt) for opt in range(1, 3)):
        print(RED + "invalide output choice" + RESET)

    handler = StreamHandler() if input_mode == '2' else None

    if debug_mode >= 2:
        print('input_mode:',input_mode, '\noutput_mode:',output_mode, '\ndebug_mode:',debug_mode)

    while True:
        try:
            # PART 1 : récupération de l'entrée utilisateur
            if input_mode == '1':
                user_input = input("\n> ").strip() 
            else:
                user_input = handler.listen()

            if user_input and debug_mode >= 2:
                print(BLUE + "DEBUG: Message utilisateur capté :" + RESET, user_input)
            elif not user_input:
                continue

            # Traitement de l'entrée utilisateur
            if input_mode == '1' and user_input.startswith("!"):
                handle_commands(user_input)
                continue

            processed_message = handle_message(user_input)
            if debug_mode >= 2:
                print(BLUE + "DEBUG: Message traité :" + RESET, processed_message)

            # PART 2 : envoi de la requête
            assistant_message = request_textgen(processed_message, debug=debug_mode)
            if debug_mode >= 2:
                print(BLUE + "DEBUG: Message assistant généré :" + RESET, assistant_message)

            # Traitement du message de l'assistant    
            assistant_message = handle_answer(response=assistant_message, StS=(input_mode=='2'))
            if debug_mode >= 2:
                print(BLUE + "DEBUG: Message assistant traité :" + RESET, assistant_message)
            
            # PART 3 : affichage de la réponse
            if output_mode == '1':
                print(GREEN + assistant_message + RESET)

            elif output_mode == '2': # OUTPUT = Speech
                dialogue, action = extraire_dialogues_et_actions(assistant_message)
                if debug_mode >= 2:
                    print(BLUE + "DEBUG: Dialogue et action extraits :" + RESET, dialogue, action)
                generate_audio(dialogue=dialogue, debug=debug_mode)
                play_audio()
            
            else: # Pas possible normalement
                print('??? output_mode:',output_mode)

        except KeyboardInterrupt:
            print(YELLOW + "\n3T s'éteint." + RESET)
            break
        except Exception as e:
            print(RED + "erreur " + str(e) + "\n" + RESET)
            traceback.print_exc()

if __name__ == '__main__':
    chat()
