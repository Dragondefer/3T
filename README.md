Voici un exemple de README.md complet pour ton projet :

---

# 3T - Chatbot Interactif Multimodal

3T est un projet de chatbot interactif qui combine plusieurs modalités d'entrée et de sortie (texte et speech), la génération d'images via une API Stable Diffusion, et l'analyse d'images via BLIP. Le projet inclut également une intégration avec Discord pour interagir en temps réel avec un LLM.

---

## Fonctionnalités

- **Multimodalité :**  
  Choix d'entrée et de sortie en mode texte ou speech.

- **Génération de texte :**  
  Interfaçage avec un LLM pour générer des réponses basées sur le contexte et l'historique de conversation.

- **Génération d'image :**  
  Utilisation d'une API (Stable Diffusion WebUI) pour générer des images à partir d'un prompt.

- **Analyse d'image :**  
  Analyse d'images envoyées par l'utilisateur via BLIP afin d'en extraire une description textuelle.

- **Intégration Discord :**  
  Un bot Discord qui permet d'interagir avec le système en envoyant des messages et des images directement dans Discord.

- **Commandes personnalisées :**  
  Gestion de commandes telles que `!img`, `!histo`, etc. pour enrichir la conversation.

- **Tests unitaires :**  
  Suite de tests permettant de valider les fonctionnalités et la performance des différents modules.

---

## Structure du Projet

```plaintext
3T/
├── TTT/
│   ├── __init__.py
│   ├── api_requests.py
│   ├── audio_utils.py
│   ├── commands.py
│   ├── config.py
│   ├── image_api.py       # Génération d'image via API (Stable Diffusion)
│   ├── image_BLIP.py      # Analyse d'image avec BLIP
│   ├── main.py            # Chatbot en mode console
│   ├── stream_handler.py
│   ├── text_processing.py
│   ├── voices/            # Fichiers audio de référence et générés
│   ├── generated_images/  # Images générées par l'API
│   └── voice_temp/        # Fichiers temporaires (ex. basic_config.toml)
├── tests/
│   ├── __init__.py
│   ├── audio_test.py
│   ├── commands_test.py
│   ├── image_test.py
│   ├── textgen_test.py
│   └── text_test.py
├── modules_tests.py       # Script pour lancer tous les tests
├── bot.py                 # Bot Discord (intégrant LLM, analyse et génération d'image)
└── README.md
```

---

## Installation

1. **Cloner le dépôt :**

   ```bash
   git clone https://github.com/ton-utilisateur/3T.git
   cd 3T
   ```

2. **Créer un environnement virtuel (optionnel) :**

   ```bash
   python -m venv venv
   # Sous Windows
   venv\Scripts\activate
   # Sous Linux/macOS
   source venv/bin/activate
   ```

3. **Installer les dépendances :**

   ```bash
   pip install -r requirements.txt
   ```

   *(Le fichier `requirements.txt` doit inclure les bibliothèques nécessaires, telles que `discord.py`, `transformers`, `pydub`, `requests`, `python-dotenv`, etc.)*

---

## Configuration

- **Fichier `config.py` :**  
  Ce fichier contient les chemins vers les répertoires utilisés (images générées, audio, voix, sauvegardes) ainsi que la configuration des personnages.  
  Par exemple, il définit :

  - `OUTPUT_DIR` pour les images générées.
  - `audio_temp_path` pour les fichiers temporaires.
  - `voices_path` pour les fichiers audio de référence.
  - `audio_path_out` pour le fichier audio généré (placé dans `voices`).
  - La configuration des personnages, incluant le chemin vers leur fichier vocal.

- **Token Discord :**  
  Pour le bot Discord, stocke ton token dans une variable d'environnement `DISCORD_BOT_TOKEN` ou dans un fichier `.env` (voir section suivante).

---

## Utilisation

### Mode Console

Pour lancer le chatbot en mode console (texte et/ou speech) :

```bash
python TTT/main.py
```

Le programme vous demandera de choisir le mode d'entrée (texte ou speech), le mode de sortie et le niveau de journalisation.

### Exécution des Tests

Pour lancer l'ensemble des tests unitaires :

```bash
python modules_tests.py
```

Vous pouvez aussi lancer des tests individuels situés dans le dossier `tests/`.

### Bot Discord

Pour lancer le bot Discord, procédez ainsi :

1. **Configurer le token Discord :**  
   Stocke ton token dans la variable d'environnement `DISCORD_BOT_TOKEN` ou dans un fichier `.env`.

2. **Lancer le bot :**

   ```bash
   python bot.py
   ```

Le bot répondra aux messages envoyés sur le serveur Discord :

- **Message texte :**  
  Le bot génère une réponse via le LLM en utilisant ton pipeline de traitement.

- **Envoi d'image en pièce jointe :**  
  Le bot télécharge l'image, la passe à BLIP pour en extraire une description, puis intègre cette description dans le prompt envoyé au LLM.

- **Commande d'image (`img(<prompt>)`) :**  
  Le bot appelle l'API de génération d'image avec le prompt fourni et renvoie l'image générée en pièce jointe.

---

## Envoi et Analyse d'Images

- **Analyse avec BLIP :**  
  Si un utilisateur envoie un message contenant une image en pièce jointe, le bot télécharge l'image dans le dossier défini par `send_image_dir`, la traite avec BLIP via le module `image_BLIP.py` pour obtenir une description, et ajoute cette description au prompt du LLM.

- **Génération d'image :**  
  La commande `img(<prompt>)` permet de générer une image via l'API Stable Diffusion (module `image_api.py`) et d'envoyer le résultat en pièce jointe dans Discord.

---

## Variables d'Environnement

Pour éviter de publier ton token dans le code, stocke-le dans une variable d'environnement ou utilise un fichier `.env`.

### Exemple avec un fichier `.env` :

1. Crée un fichier `.env` à la racine du projet :

   ```
   DISCORD_BOT_TOKEN=ton_token_ici
   ```

2. Dans ton code (par exemple dans `bot.py`), charge le fichier avec :

   ```python
   from dotenv import load_dotenv
   import os

   load_dotenv()
   TOKEN = os.getenv("DISCORD_BOT_TOKEN")
   if not TOKEN:
       raise ValueError("Token Discord non trouvé.")
   ```

---

## Dépendances Principales

- Python 3.x
- [discord.py](https://discordpy.readthedocs.io/)
- [Transformers](https://huggingface.co/transformers/)
- [Pydub](https://github.com/jiaaro/pydub)
- [Requests](https://docs.python-requests.org/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- Autres bibliothèques utilisées dans le projet (voir `requirements.txt`)

---

## Contribution

Les contributions sont les bienvenues !  
- Créez une branche pour vos modifications.
- Soumettez une Pull Request avec une description détaillée de vos changements.

---

## Licence

Ce projet est sous Licence Apache 2.0

---

## Remarques

Ce projet vise à fournir une interface interactive et multimodale pour interagir avec un LLM, analyser des images et générer du contenu visuel.  
N'hésitez pas à signaler les bugs ou proposer des améliorations via [GitHub Issues](https://github.com/ton-utilisateur/3T/issues).

---