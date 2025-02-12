# Configuration globale
API_URL : str  = 'http://127.0.0.1:5000/v1/chat/completions'
audio_path : str  = r"C:\Users\evnnl\OneDrive - Conseil régional Grand Est - Numérique Educatif\Documents\android project\Code\interaction\3T\3T\voice_temp\infer_cli_out.wav"

# Définir les personnages et leurs voix associées
characters: dict[str, str] = {
    "2B": {
        "context": r"*context: You are 2B. You meet Dragon, your commander and creator. Important: Answer shortly.*",
        "voice": "2B.wav",
        "reference_text": "Thank you for uploading my data to the bunker. I see. I'm fine, 9S. There's something about your voice that..."
    },
}

# Personnage actif par défaut
current_character : str = "2B"

def get_current_character():
    """
    Retourne la vaiable current_character update (2B, Melina, PDA, Dr.Moon, Evelyn)
    """
    return current_character

def change_character(new_character: str):
    """
    Change la variable current_character (2B, Melina, PDA, Dr.Moon, Evelyn)
    """
    global current_character
    if new_character in characters:
        current_character = new_character
        print(f"Personnage changé en : {new_character}")
    else:
        print(f"Le personnage {new_character} n'existe pas. Choisissez parmi : {list(characters.keys())}")

# Headers et paramètres pour l'API
headers : dict[str] = {"Content-Type": "application/json"}
history : list[dict[str, str]] = [{"role": "system", "content": characters[current_character]["context"]}]
generation_params = {"temperature": 0.7, "max_new_tokens": 100, "top_p": 0.9, "n": 1}

# Paramètres audio
Model : str = 'small'
English : bool = False
Translate : bool = False
SampleRate : int = 16000
BlockSize : int = 50
Threshold : float = 0.01
Vocals : list[int] = [50, 1000]
EndBlocks : int = 40
