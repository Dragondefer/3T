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
    def __init__(self, assist=None):
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
        print("Écoute activée... (appuyez sur Ctrl+C pour quitter)")
        with sd.InputStream(channels=1, callback=self.callback, blocksize=int(SampleRate * BlockSize / 1000), samplerate=SampleRate):
            while self.running and self.asst.running:
                transcribed_text = self.process()
                if transcribed_text:
                    return transcribed_text
