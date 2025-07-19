__version__ = 101

import os
import re
import time
from pydub import AudioSegment
from pydub.playback import play

from config import audio_path_out, voices_path

def generate_audio(dialogue: str, name: str = None, del_flag: bool = False, sub_fol: str | None = None, debug: int = 0) -> None:
    """
    Génère un fichier audio .wav à partir d'un texte via f5-tts.
    Le fichier généré (initialement infer_cli_out.wav) est renommé avec le nom fourni ou dérivé du dialogue.
    Si sub_fol est renseigné, le fichier sera placé dans voices/sub_fol sinon dans voices.
    Le paramètre del_flag (default False) pourra servir plus tard à gérer le nettoyage.
    """
    from config import characters, current_character

    # Si dialogue est une liste, on concatène
    if isinstance(dialogue, list):
        dialogue = " ".join(dialogue)

    # Nettoyage du dialogue pour le TOML et pour le nom de fichier (on enlève les guillemets et échappe les backslashes)
    dialogue_text = dialogue.replace('"', '').replace("\\", "\\\\")
    
    # Détermine le répertoire de sortie
    base_dir = "voices" if sub_fol is None else os.path.join("voices", sub_fol)
    os.makedirs(base_dir, exist_ok=True)

    # Détermine le nom de fichier de sortie
    # Si name n'est pas fourni, on se base sur le dialogue (on garde 20 caractères maximum et remplace les espaces par _)
    if not name:
        name = re.sub(r'\s+', '_', dialogue_text[:20])
    # Ajoute l'extension .wav si nécessaire
    if not name.endswith(".wav"):
        name += ".wav"
    audio_path_out = os.path.join(base_dir, name)

    # On prépare la configuration pour f5-tts
    character_config = characters[current_character]
    voice = character_config['voice'].replace("\\", "\\\\")
    ref_text = character_config['reference_text'].replace("\\", "\\\\")

    # Pour que f5-tts génère le fichier dans le dossier voulu, on va utiliser un chemin temporaire
    # Le fichier généré par f5-tts sera nommé infer_cli_out.wav dans output_dir
    output_dir_toml = os.path.abspath(base_dir).replace("\\", "/")
    config_content = f"""
model = "F5-TTS"
ref_audio = "{voice}"
gen_text = "{dialogue_text}"
ref_text = "{ref_text}"
gen_file = ""
remove_silence = false
output_dir = "{output_dir_toml}"
"""
    if debug >= 3:
        print("config_content:", config_content)

    # Le fichier TOML temporaire est placé dans voices remplacé par voice_temp
    toml_dir = os.path.join(os.path.dirname(base_dir).replace("voices", "voice_temp"))
    os.makedirs(toml_dir, exist_ok=True)
    toml_path = os.path.join(toml_dir, "basic_config.toml")
    
    with open(toml_path, "w", encoding="utf-8") as f:
        f.write(config_content)
    
    if debug >= 3:
        print("toml_path:", toml_path)
        print("Lancement de la commande f5-tts_infer-cli")

    # Lancer la commande (celle-ci génèrera "infer_cli_out.wav" dans base_dir)
    os.system(f'f5-tts_infer-cli -c "{toml_path}"')

    if debug >= 3:
        print("Fichier généré (par défaut):", os.path.join(base_dir, "infer_cli_out.wav"))

    # Une fois le fichier généré, on le renomme selon 'name'
    default_audio = os.path.join(base_dir, "infer_cli_out.wav")
    if os.path.exists(default_audio):
        os.replace(default_audio, audio_path_out)
        if debug >= 1:
            print("Audio renommé en :", audio_path_out)
    else:
        if debug >= 1:
            print("Le fichier généré n'a pas été trouvé :", default_audio)
    
    # Si nécessaire, gérer le nettoyage (ici on ne supprime rien si del_flag est False)
    if del_flag:
        try:
            os.remove(toml_path)
            if debug >= 3:
                print("Fichier TOML supprimé :", toml_path)
        except Exception as e:
            if debug >= 1:
                print("Erreur lors de la suppression du TOML :", e)

"""
def play_audio(audio_path_out: str = audio_path_out) -> None:
    Joue l'audio spécifié par audio_path_out.
    `play()` attends la génération et la fin de l'audio pour continuer le code
    print(f'playing audio')
    if os.path.exists(audio_path_out):
        #import tempfile
        #tempfile.tempdir = voices_path
        audio = AudioSegment.from_wav(audio_path_out)
        play(audio)
        os.remove(audio_path_out)
    time.sleep(1)
"""

def play_audio(audio_path_out: str = audio_path_out) -> None:
    """
    Joue l'audio spécifié par audio_path_out.
    `play()` attends la génération et la fin de l'audio pour continuer le code
    """
    print(f'playing audio')
    if os.path.exists(audio_path_out):
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            temp_path = tmp_file.name
        
        try:
            audio = AudioSegment.from_wav(audio_path_out)
            # Export to our controlled temp file
            audio.export(temp_path, format="wav")
            
            # Play using simpler method to avoid pydub's internal temp file creation
            import subprocess
            subprocess.call(["ffplay", "-nodisp", "-autoexit", temp_path], 
                          stdout=subprocess.DEVNULL, 
                          stderr=subprocess.DEVNULL)
            
            # Clean up original file if needed
            os.remove(audio_path_out)
        finally:
            # Always clean up our temp file
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass
    time.sleep(1)

if __name__ == '__main__':
    generate_audio(dialogue='this is a test')
    play_audio()
