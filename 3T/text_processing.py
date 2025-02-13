import re
import requests
import datetime

from api_requests import (load_llm, 
                          unload_llm)
from image_api import generate_image

def extraire_dialogues_et_actions(texte: str) -> tuple[list, list]:
    """
    Raffine le texte en le classant dans un tupple contenant:
        dialogues: \"dialogue\"  \'dialogue\' 
        actions: \*action\* \(action\)
    """

    dialogues = []
    actions = []
    pattern = re.compile(r'''
        (\*[^*]+\*|\([^()]+\)) |   
        ("[^"]+"|'.+?') |          
        ([^*"()\n]+)               
    ''', re.VERBOSE)

    segments = re.findall(pattern, texte)
    for segment in segments:
        action_marked, dialogue, action_unmarked = segment
        if action_marked:
            actions.append(action_marked.strip())
        elif dialogue:
            dialogues.append(dialogue.strip())
        elif action_unmarked and action_unmarked.strip():
            phrases = re.split(r'(?<=\.|\?|!)\s+', action_unmarked.strip())
            for phrase in phrases:
                if phrase and not ('"' or "'" in phrase):
                    actions.append(phrase.strip())
                else:
                    dialogues.append(phrase.strip())
    if ":" in dialogues:
        dialogues = dialogue.split(":")[1].strip() # retire tout le texte avant ":"
    return dialogues, actions

def handle_message(message: str) -> str:
    """
    Ajoute au message \"user: \" et si besoin des inforamtion system:
        Exemple: `\'(system info... actual time: {now.hour}:{now.minute}...)\'`
    """
    
    message = f"user: \"{message}\""

    now = datetime.datetime.now()
    if "time" in message:
        message += f" (system info you may need: actual time {now.day}-{now.month}-{now.year}, hour: {now.hour}:{now.minute})"
    return message

def handle_answer(response:str):
    """
    execute les commandes de l'assistant et rafine le texte
    """
    match = re.search(r"img\((.*?)\)", response)
    if match:
        prompt = match.group(1)

        unload_llm() # unload le model pour avoir + de ressources
        generate_image(prompt)
        load_llm() # reload le model pour pouvoir continuer le chat
        
        response = re.sub(r"img\((.*?)\)", "", response) # suppr la commande img(prompt) de la réponse
    
    return response
