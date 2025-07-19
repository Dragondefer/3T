__version__ = 120

import re # voir regexper.com pour aide visuel
import requests
import datetime
import traceback

from audio_utils import generate_audio
from image_BLIP import process_message
from image_api import (generate_image,
                       open_last_image)
from api_requests import (load_llm, 
                          unload_llm)

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

    for dialogue in dialogues:
        if re.search(':', dialogue):
            print(f'found \':\' in : \'{dialogue}\'')
            dialogues = dialogue.split(":")[1].strip() # retire tout le texte avant ":"
    return dialogues, actions

def handle_message(message: str) -> str:
    """
    Ajoute au message \"user: \" et si besoin des inforamtion system:
        Exemple: `\'(system info... actual time: {now.hour}:{now.minute}...)\'`
    """
    
    # message = f"user: \"{message}\"" # ça fais un peu nimp avec la rep de l'ia

    now = datetime.datetime.now()
    if "time" in message:
        message += f" (system info you may need: actual time {now.day}-{now.month}-{now.year}, hour: {now.hour}:{now.minute})"

    if "!img" in message:
        message = process_message(message)

    return message

def handle_answer(response:str, StS:bool=False, debug:int=0):
    """
    execute les commandes de l'assistant et rafine le texte.

    Commandes :
      - `img(prompt)`: génère une image avec le prompt.
      - `audio(prompt)`: génère un audio avec le prompt.
    """
    match_img = re.search(r"img\((.*?)\)", response) # (.*?) == any str
    if match_img:
        prompt = match_img.group(1)

        try:
            print('DEBUG: Prompt =',prompt)
            unload_llm() # unload le model pour avoir + de ressources
            generate_image(prompt)
            load_llm() # reload le model pour pouvoir continuer le chat
        except (requests.exceptions.HTTPError, Exception) as e:
            print(e, '\nGeneration de l\'image sans unload le model LLM')
            try:
                generate_image(prompt)
                open_last_image()
            except (requests.exceptions.HTTPError, Exception) as e:
                print('erreur lors de la génération de l\'image:', e)
                traceback.print_exc()
    
        response = re.sub(r"img\((.*?)\)", "", response) # suppr la commande img(prompt) de la réponse
    
    
    match_audio = re.search(r"audio\((.*?)\)", response)

    if match_audio and (StS == False):
        prompt = match_audio.group(1)
        try:
            print('DEBUG: Prompt =',prompt)
            unload_llm() # unload le model pour avoir + de ressources
            generate_audio(prompt)
            load_llm() # reload le model pour pouvoir continuer le chat
        except (requests.exceptions.HTTPError, Exception) as e:
            print(e, '\nGeneration de l\'audio sans unload le model LLM')
            try:
                generate_audio(prompt)
            except (requests.exceptions.HTTPError, Exception) as e:
                print('erreur lors de la génération de l\'audio:', e)
    
        response = re.sub(r"audio\((.*?)\)", "", response) # suppr la commande audio(prompt) de la réponse
   
        # response = re.sub(r"(.*?):", "", response) # jsp
    return response


if __name__ == '__main__':
    user_text = '\"dialogue test\", \'what time is it ?\'(action test), *other action* untreated text'
    ia_text = '3T: dialogue1, *action1* img(image prompt)'
    
    print('\nUser text:')
    print(user_text)

    print('\nUser text extract:')
    print(extraire_dialogues_et_actions(user_text))

    print('\nIA text extract:')
    print(extraire_dialogues_et_actions(ia_text))
    
    print('\nHandle user text:')
    print(handle_message(user_text))
    
    print('\nHandle IA text:')
    print(handle_answer(ia_text))

    print('\nIA full refined text')
    print(extraire_dialogues_et_actions(handle_answer(ia_text)))