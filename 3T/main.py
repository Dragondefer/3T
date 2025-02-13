from stream_handler import StreamHandler
from api_requests import request_textgen
from text_processing import (extraire_dialogues_et_actions, 
                             handle_message,
                             handle_answer)
from audio_utils import (generate_audio, 
                         play_audio)
from config import (characters, 
                    change_character, 
                    get_current_character)
from commands import (print_help,
                      afficher_info,
                      afficher_model,
                      afficher_history,
                      changer_caractere,
                      supprimer_dernier,
                      save_history,
                      load_history,
                      clear_history,
                      list_saves)


def chat() -> None:
    while (char := input('character: ')) not in characters:
        print("Choix invalide, réessayez.")
    change_character(char)
    character_config = characters[get_current_character()]
    print(character_config)
    
    while (answ:=input('1: TtT\n2: StS\nchois: ')) != ('1','2'):
        print('invalid input')
    
    if answ == '1':
        while True:
            try:
                message = input("\n> ").strip()
                if not message:
                    continue
                if message.startswith("!"):
                    if message.startswith("!help"):
                        print_help()
                    elif message.startswith("!info"):
                        afficher_info()
                    elif message.startswith("!model"):
                        afficher_model()
                    elif message.startswith("!save"):
                        parts = message.split(maxsplit=1)
                        if len(parts) == 2:
                            save_history(parts[1])
                        else:
                            print("Usage: !save <filename>")
                    elif message.startswith("!load"):
                        parts = message.split(maxsplit=1)
                        if len(parts) == 2:
                            load_history(parts[1])
                        else:
                            print("Usage: !load <filename>")
                    elif message.startswith("!clear"):
                        clear_history()
                    elif message.startswith("!back"):
                        supprimer_dernier()
                    elif message.startswith("!histo"):
                        afficher_history()
                    elif message.startswith("!list"):
                        saves = list_saves()
                        print("Sauvegardes disponibles :", ', '.join(saves))
                    elif message.startswith("!character"):
                        parts = message.split(maxsplit=1)
                        if len(parts) == 2:
                            changer_caractere(parts[1])
                        else:
                            print("Usage: !character <name>")
                    elif message.startswith("!quit"):
                        print("Fermeture du bot.")
                        break
                    else:
                        print("Commande inconnue. Tapez !help pour la liste des commandes.")
                else:
                    assistant_message = request_textgen(message)
                    #dialogue, action = extraire_dialogues_et_actions(assistant_message)
                    assistant_message = handle_answer(assistant_message)
                    print(assistant_message)
            except KeyboardInterrupt:
                print("\n3T s'éteind.")
                break

    elif answ == '2':
        handler = StreamHandler()
        while True:
            try:
                user_message = handler.listen()
                if user_message:
                    print("Message utilisateur capté :", user_message)
                    user_message = handle_message(user_message)
                    print("Message utilisateur traité :", user_message)

                    assistant_message = request_textgen(user_message)
                    print("\nRéponse de l'ia :", assistant_message)
                    assistant_message = handle_answer(assistant_message)
                    dialogue, action = extraire_dialogues_et_actions(assistant_message)
                    
                    generate_audio(dialogue=dialogue)
                    play_audio()

            except (KeyboardInterrupt, SystemExit):
                print("\nArrêt de l'application...")
                break

if __name__ == '__main__':
    chat()
