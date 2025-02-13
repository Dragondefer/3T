import requests
from config import API_URL, headers, generation_params, characters

def unload_llm():
    """Décharge le modèle via l'API."""
    r = requests.post(f"{API_URL}/unload_model")
    if r.ok:
        print("Modèle déchargé avec succès")
    else:
        print("Erreur lors du déchargement du modèle")

def load_llm():
    """Charge le modèle via l'API."""
    r = requests.post(f"{API_URL}/load_model")
    if r.ok:
        print("Modèle chargé avec succès")
    else:
        print("Erreur lors du chargement du modèle")

def request_textgen(user_message: str) -> str:
    """
    Ajoute le message de l'utilisateur a l'historique puis envoie la requête au textgen puis obtien la réponce sous forme de texte `str`.
    """
    from config import history, current_character
    if not user_message:
        print("Aucun message utilisateur détecté.")
        return
    
    # update le contexte basé sur le perso actif
    history[0]["content"] = characters[current_character]["context"]
    history.append({"role": "user", "content": user_message})

    data = {
        "mode": "chat",
        "messages": history,
        "temperature": generation_params["temperature"],
        "max_new_tokens": generation_params["max_new_tokens"],
        "top_p": generation_params["top_p"],
        "n": generation_params["n"]
    }

    try:
        print("Envoi de la requête de génération de texte à l'API...")
        response = requests.post(API_URL, headers=headers, json=data, verify=False)
        response.raise_for_status()

        assistant_message: str = response.json()['choices'][0]['message']['content']
        history.append({"role": current_character, "content": assistant_message})

        return assistant_message
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la génération du texte : {e}")
