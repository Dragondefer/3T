import os
import json

from config import (generation_params,
                    current_character,
                    history,
                    characters,
                    )

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
                            "  !quit                - Quitter le bot"
                        )

def afficher_info():
    print(f"Paramètres de génération:\n  Température: {generation_params['temperature']}\n  Max new tokens: {generation_params['max_new_tokens']}\n  Top p: {generation_params['top_p']}\n  Nombre de réponses: {generation_params['n']}\n  Caractère actuel: {current_character}")

def afficher_model():
    print(f"Nom du modèle: {current_character}")

def afficher_history():
    print("Historique de conversation:")
    for msg in history:
        print(f"{msg['role']}: {msg['content']}")

def changer_caractere(nouveau):
    global current_character
    if nouveau in characters:
        current_character = nouveau
        print(f"Caractère changé en : {current_character}")
    else:
        print(f"Caractère invalide. Choix possibles : {', '.join(characters)}")

def supprimer_dernier():
    if len(history) > 1:
        history.pop()
        print("Dernier message supprimé.")
    else:
        print("Historique insuffisant pour supprimer.")

# ----- Gestion des sauvegardes -----
SAVE_DIR = './saves'
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def save_history(filename="history.json"):
    if not filename.endswith('.json'):
        filename += '.json'
    with open(os.path.join(SAVE_DIR, filename), 'w') as f:
        json.dump(history, f)
    print(f"Historique sauvegardé sous {filename}")

def load_history(filename="history.json"):
    global history
    try:
        with open(os.path.join(SAVE_DIR, filename), 'r') as f:
            history = json.load(f)
        print(f"Historique chargé depuis {filename}")
    except FileNotFoundError:
        print("Fichier non trouvé.")

def clear_history():
    global history
    history = [{"role": "system", "content": characters[current_character]["context"]}]
    print("Historique réinitialisé.")

def list_saves():
    return [f for f in os.listdir(SAVE_DIR) if f.endswith('.json')]