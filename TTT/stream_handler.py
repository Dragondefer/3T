__version__ = 10

import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd
import whisper

from config import (Model, 
                    SampleRate, 
                    BlockSize, 
                    Threshold, 
                    EndBlocks)

class StreamHandler:
    """
    Gère le streaming audio, l'enregistrement et la transcription en utilisant le modèle Whisper.

    Cette classe gère l'entrée audio en temps réel, détecte la parole en fonction d'un seuil,
    met en mémoire tampon les données audio, écrit l'audio dans un fichier WAV lorsque l'enregistrement est terminé,
    et transcrit l'audio en utilisant le modèle de reconnaissance vocale Whisper.

    Attributs :
        asst : Un objet assistant avec les attributs 'running', 'talking' et 'analyze'.
               Si None, un FakeAssistant par défaut est utilisé.
        running (bool) : Indicateur pour contrôler la boucle d'écoute.
        padding (int) : Compteur pour gérer les blocs audio en fin de parole.
        prevblock (np.ndarray) : Mémoire tampon du bloc audio précédent.
        buffer (np.ndarray) : Mémoire tampon actuelle accumulant les données audio.
        fileready (bool) : Indicateur si le fichier audio est prêt pour la transcription.
        model : Modèle Whisper chargé pour la transcription.
    """
    def __init__(self, assist=None):
        """
        Initialise le StreamHandler.

        Args:
            assist : Objet assistant optionnel avec les attributs 'running', 'talking' et 'analyze'.
                     Si None, un FakeAssistant par défaut est créé.

        Initialise les tampons, charge le modèle Whisper et définit les états initiaux.
        """
        if assist is None:
            class FakeAssistant:
                running, talking, analyze = True, False, None
            self.asst = FakeAssistant()

        else:
            self.asst = assist
        self.running = True
        self.padding = 0
        self.prevblock = self.buffer = np.zeros((0, 1))
        self.fileready = False

        print("Chargement du modèle Whisper... ", end='', flush=True)
        self.model = whisper.load_model(Model)
        print("Terminé.")

    def callback(self, indata, frames, time, status):
        """
        Fonction de rappel pour le flux d'entrée audio.

        Cette fonction est appelée périodiquement par le flux d'entrée audio. Elle traite
        les données audio entrantes, détecte la parole en fonction du seuil RMS, gère la mise en mémoire tampon,
        et détermine quand finaliser l'enregistrement.

        Args:
            indata (np.ndarray) : Bloc de données audio entrant.
            frames (int) : Nombre de frames dans ce bloc.
            time : Informations temporelles pour le bloc.
            status : Statut du flux d'entrée audio.

        Comportement :
            - Affiche les messages de statut s'il y en a.
            - Détecte le silence et affiche un message.
            - Si le niveau audio dépasse le seuil et que l'assistant ne parle pas,
              met en mémoire tampon l'audio et réinitialise le compteur de padding.
            - Si en dessous du seuil, diminue le compteur de padding et continue la mise en mémoire tampon
              ou finalise l'enregistrement si le padding expire et que le tampon est suffisamment long.
            - Écrit l'audio mis en mémoire tampon dans 'dictate.wav' lorsque l'enregistrement se termine.
        """
        if status:
            print(f"[Status] {status}")

        if not any(indata):
            print("Silence détecté", end='', flush=True)
            return
        
        if np.sqrt(np.mean(indata**2)) > Threshold and not self.asst.talking:
            print(".", end='', flush=True)
            if self.padding < 1:
                self.buffer = self.prevblock.copy()

            self.buffer = np.concatenate((self.buffer, indata))
            self.padding = EndBlocks

        else:
            self.padding -= 1
            if self.padding > 1:
                self.buffer = np.concatenate((self.buffer, indata))

            elif self.padding < 1 < self.buffer.shape[0] > SampleRate:
                self.fileready = True
                print("\nEnregistrement terminé. Préparation pour la transcription.")
                write('dictate.wav', SampleRate, self.buffer)
                self.buffer = np.zeros((0, 1))

            elif self.padding < 1 < self.buffer.shape[0] < SampleRate:
                self.buffer = np.zeros((0, 1))
                print("Enregistrement ignoré (trop court)")

            else:
                self.prevblock = indata.copy()

    def process(self):
        """
        Traite le fichier audio enregistré pour la transcription.

        Si un fichier audio enregistré est prêt, cette méthode transcrit l'audio en utilisant
        le modèle Whisper, affiche le texte transcrit, et transmet éventuellement le
        texte à la méthode d'analyse de l'assistant.

        Returns:
            str ou None : Le texte transcrit si disponible, sinon None.
        """
        if self.fileready:
            print("Transcription en cours...")
            result = self.model.transcribe('dictate.wav', fp16=False, language='en', task='transcribe')
            transcribed_text = result['text']
            print(f"Texte transcrit: {transcribed_text}")

            if self.asst.analyze is not None:
                self.asst.analyze(transcribed_text)
                
            self.fileready = False
            return transcribed_text

    def listen(self):
        """
        Commence l'écoute du flux d'entrée audio et traite la parole.

        Cette méthode ouvre un flux audio d'entrée et écoute continuellement la parole.
        Lorsque la parole est détectée et enregistrée, elle traite l'audio pour la transcription.
        La boucle d'écoute continue tant que le gestionnaire et l'assistant fonctionnent.

        Returns:
            str ou None : Le texte transcrit provenant de l'entrée audio si disponible.
        """
        print("Écoute activée... (appuyez sur Ctrl+C pour quitter)")
        with sd.InputStream(channels=1, callback=self.callback, blocksize=int(SampleRate * BlockSize / 1000), samplerate=SampleRate):
            while self.running and self.asst.running:
                transcribed_text = self.process()
                if transcribed_text:
                    return transcribed_text
