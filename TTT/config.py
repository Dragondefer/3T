import os

# Config globale
API_URL : str  = 'http://127.0.0.1:5000/v1/chat/completions'
IMG_API_URL : str = 'http://127.0.0.1:7860'

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OUTPUT_DIR: str = os.path.join(project_root, "TTT", "generated_images")
send_image_dir: str = os.path.join(project_root, "TTT", "send_images")
audio_temp_path: str = os.path.join(project_root, "TTT", "voice_temp")
voices_path: str = os.path.join(project_root, "TTT", "voices")
audio_path_out: str = os.path.join(voices_path, "infer_cli_out.wav")
SAVE_DIR: str = os.path.join(project_root, "TTT", "saves")

characters: dict[str, dict[str, str]] = {
    "2B": {
        "context": r"(context: You are 2B. You meet Dragon, your commander and creator. Important: Answer shortly.)",
        "voice": os.path.join(voices_path, "2B.wav"),
        "reference_text": "Thank you for uploading my data to the bunker. I see. I'm fine, 9S. There's something about your voice that..."
    },
    "3t": {
        "context": r"(context: You meet your creator. Answer shortly.)",
        "voice": os.path.join(voices_path, "2B.wav"),
        "reference_text": "Thank you for uploading my data to the bunker. I see. I'm fine, 9S. There's something about your voice that..."
    }
}


# Perso actif par défaut
current_character : str = "3t"

def get_current_character():
    """
    Retourne la vaiable current_character update (2B, Melina, PDA...)
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

# Headers et params pour l'API
headers : dict[str] = {"Content-Type": "application/json"}
history : list[dict[str, str]] = [{"role": "system", "content": characters[current_character]["context"]}]
generation_params : dict[str, int | float] = {"temperature": 0.7, "max_new_tokens": 100, "top_p": 0.9, "n": 1}

# Params audio
Model : str = 'small'
English : bool = False
Translate : bool = False
SampleRate : int = 16000
BlockSize : int = 50
Threshold : float = 0.01
Vocals : list[int] = [50, 1000]
EndBlocks : int = 40
