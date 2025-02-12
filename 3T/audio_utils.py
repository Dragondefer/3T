import os
import time
from pydub import AudioSegment
from pydub.playback import play

from config import audio_path

def generate_audio(dialogue: str) -> None:
    """
    /!\ utilise une commande cli avec `os.system` et non api donc lent.\n
      - problem principal = doit load le model a chaque commande\n
    Génère un audio .wav dans `audio_path` à partire d'un texte\n
      - langues supportées : anglais ; chinois
    """
    from config import characters, current_character
    dialogue_text = " ".join(dialogue).replace('"', '')
    character_config = characters[current_character]

    config_content = f"""
model = "F5-TTS"
ref_audio = "{character_config['voice']}"
gen_text = "{dialogue_text}"
ref_text = "{character_config['reference_text']}"
gen_file = ""
remove_silence = false
output_dir = "voice_temp"
"""
    with open("basic_config.toml", "w") as f:
        f.write(config_content)
    os.system("f5-tts_infer-cli -c basic_config.toml")


def play_audio(audio_path: int = audio_path, 
               max_try: int = 30):
    """
    Joue l'audio `audio_path`:\n
        - Si audio : le joue puis le supprime
        - Sinon : attends `1` sec puis retry `max_try` fois puis `break`
    """
    while (audio_try:=0) != max_try:
        if os.path.exists(audio_path):
            audio = AudioSegment.from_wav(audio_path)
            play(audio)
            os.remove(audio_path)
            break
        print('waiting for audio')
        time.sleep(1)
        audio_try+=1


if __name__ == '__main__':
    generate_audio(dialogue='this is a test')
    play_audio()