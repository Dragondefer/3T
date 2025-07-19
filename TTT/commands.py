__version__ = 83

import os
import json

from config import (generation_params,
                    characters,
                    SAVE_DIR,
                    change_character,
                    clear_history,
                    )

from api_requests import (load_llm,
                          unload_llm)

def print_help():
    print(
                            "Commandes disponibles:\n"
                            "  !info                - Afficher les paramètres\n"
                            "  !model               - Afficher le nom du modèle\n"
                            "  !save <filename>     - Sauvegarder l'historique\n"
                            "  !load <filename>     - Charger un historique\n"
                            "  !clear               - Réinitialiser l'historique\n"
                            "  !back                - Supprimer le dernier message\n"
                            "  !histo               - Afficher l'historique\n"
                            "  !list                - Lister les sauvegardes\n"
                            "  !character <name>    - Changer de caractère\n"
                            "  !debug <int>         - Changer le niveau de debug\n"
                            "  !load_llm            - Charge le model LLM\n"
                            "  !unload_llm          - Décharge le model LLM\n"
                            "  !quit                - Quitter le bot\n"
                        )

def afficher_info():
    from config import current_character
    print(f"Paramètres de génération:\n  Température: {generation_params['temperature']}\n  Max new tokens: {generation_params['max_new_tokens']}\n  Top p: {generation_params['top_p']}\n  Nombre de réponses: {generation_params['n']}\n  Caractère actuel: {current_character}")

def afficher_model():
    from config import current_character
    print(f"Nom du modèle: {current_character}")

def afficher_history():
    from config import history
    print("Historique de conversation:")
    for msg in history:
        print(f"{msg['role']}: {msg['content']}")

def supprimer_dernier():
    from config import history
    if len(history) > 1:
        history.pop()
        print("Dernier message supprimé.")
    else:
        print("Historique insuffisant pour supprimer.")

# ----- Gestion des sauvegardes -----

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def save_history(filename="history.json"):
    from config import history
    if not filename.endswith('.json'):
        filename += '.json'
    with open(os.path.join(SAVE_DIR, filename), 'w') as f:
        json.dump(history, f)
    print(f"Historique sauvegardé sous {filename}")

def load_history(filename="history.json"):
    from config import history
    try:
        with open(os.path.join(SAVE_DIR, filename), 'r') as f:
            history = json.load(f)
        print(f"Historique chargé depuis {filename}")
    except FileNotFoundError:
        print("Fichier non trouvé.")

def list_saves():
    return [f for f in os.listdir(SAVE_DIR) if f.endswith('.json')]

def img_prompt():
    from config import history
    history.append({"role": "system", "content": "When I ask for an image, please respond using the command img(prompt). The prompt must be a highly detailed description of the requested image. It should include phrases like \"high quality\" and \"realistic\", and provide a thorough depiction of the scene. For example, if I ask \"take a pic of your room\", do not simply output \"dream bedroom\". Instead, describe in detail how your room would look—include elements like the layout, lighting, furniture, colors, textures, and any unique features. The more specific the description, the more accurately the image will match the request."})

def change_debug_mode(level:int=0) -> None:
    from config import debug_mode
    debug_mode = level
    return debug_mode

commandes = {
    '!help': lambda args: print_help(),
    '!info': lambda args: afficher_info(),
    '!model': lambda args: afficher_model(),
    '!save': lambda args: save_history(args[0]) if args else print("Usage: !save <filename>"),
    '!load': lambda args: load_history(args[0]) if args else print("Usage: !load <filename>"),
    '!clear': lambda args: clear_history(),
    '!back': lambda args: supprimer_dernier(),
    '!histo': lambda args: afficher_history(),
    '!list': lambda args: print("Sauvegardes disponibles :", ', '.join(list_saves())),
    '!character': lambda args: change_character(args[0]) if args else print("Usage: !character <name>"),
    '!prompt_img': lambda args: img_prompt(),
    '!debug': lambda args: change_debug_mode(args[0]) if args else print('Usage: !debug <int>'),
    '!load_llm': lambda args: load_llm(),
    '!unload_llm': lambda args: unload_llm(),
    '!quit': lambda args: exit(print("3T s'éteind..")),
}

def handle_commands(text:str) -> None:
    parts = text.split(maxsplit=1)
    cmd = parts[0]
    args = parts[1].split() if len(parts) > 1 else []
    if cmd in commandes:
        commandes[cmd](args)
    else:
        print("Commande inconnue. Tapez !help pour la liste des commandes.")

if __name__ == '__main__':
    cmds: tuple = ('help', 'clear', 'list')
    for cmd in cmds:
        test_input = '!' + cmd
        handle_commands(test_input)