import os
import time
from pydub import AudioSegment
from pydub.playback import play

from config import audio_path_out

def generate_audio(dialogue: str, debug:str='0') -> None:
    """
    Génère un fichier audio .wav à partir d'un texte via f5-tts.
    Le fichier TOML est créé avec un output_dir pointant vers le dossier 'voices'
    afin que le fichier généré (infer_cli_out.wav) soit placé dans TTT/voices.
    """
    from config import characters, current_character
    # Nettoyage du dialogue et échappement des backslashes si nécessaire
    dialogue_text = dialogue.replace('"', '').replace("\\", "\\\\")
    character_config = characters[current_character]
    
    voice = character_config['voice'].replace("\\", "\\\\")
    ref_text = character_config['reference_text'].replace("\\", "\\\\")
    
    # On souhaite que le fichier audio soit généré dans le dossier contenant audio_path_out
    output_dir = os.path.dirname(audio_path_out)
    # Pour éviter les problèmes d'échappement dans le TOML, on utilise des slashs
    output_dir_toml = os.path.abspath(output_dir).replace("\\", "/")
    
    config_content = f"""
model = "F5-TTS"
ref_audio = "{voice}"
gen_text = "{dialogue_text}"
ref_text = "{ref_text}"
gen_file = ""
remove_silence = false
output_dir = "{output_dir_toml}"
"""
    if debug >= '3':
        print("config_content:",config_content)

    # Enregistrer le fichier TOML dans le dossier temporaire (par exemple, TTT/voice_temp)
    toml_path = os.path.join(os.path.dirname(audio_path_out).replace("voices", "voice_temp"), "basic_config.toml")
    os.makedirs(os.path.dirname(toml_path), exist_ok=True)
    
    with open(toml_path, "w", encoding="utf-8") as f:
        f.write(config_content)

    if debug >= '3':
        print("toml_path:", toml_path)
        print('lancement de la commande f5-tts_inver-cli')

    os.system(f'f5-tts_infer-cli -c "{toml_path}"')

    if debug >= '3':
        print('fichier généré:', audio_path_out)


def play_audio(audio_path_out: str = audio_path_out, max_try: int = 10) -> None:
    """
    Joue l'audio spécifié par audio_path_out.
    Si le fichier n'existe pas encore, attend et réessaie jusqu'à max_try fois.
    """
    audio_try = 0
    while audio_try != max_try:
        print(f'waiting for audio ({audio_try}/{max_try})')
        if os.path.exists(audio_path_out):
            audio = AudioSegment.from_wav(audio_path_out)
            play(audio)
            os.remove(audio_path_out)
            break
        time.sleep(1)
        audio_try += 1


if __name__ == '__main__':
    generate_audio(dialogue='this is a test')
    play_audio()
