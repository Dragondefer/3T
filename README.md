![Star](https://img.shields.io/github/stars/dragondefer/3T) 
![Issues](https://img.shields.io/github/issues/dragondefer/3T)
![Stars](https://img.shields.io/github/stars/dragondefer/3T)
![Forks](https://img.shields.io/github/forks/dragondefer/3T)
![Repo Size](https://img.shields.io/github/repo-size/dragondefer/3T)
![Last Commit](https://img.shields.io/github/last-commit/dragondefer/3T)
![Language](https://img.shields.io/github/languages/top/dragondefer/3T)

---

# 3T - Chatbot Multimodal - ver 3.3.2
Official web-site: https://dragondefer.github.io/3T/

3T est un projet de chatbot, étant de base seulement Text-To-Text, contenant des modules interactif qui ajoute plusieurs modalités d'entrée et de sortie (texte et speech), la génération d'images via une API Stable Diffusion, et l'analyse d'images via BLIP. Le projet inclut également d'autres intégration comme avec Discord pour interagir en temps réel avec un LLM.

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
  Gestion de commandes telles que `!help`, `!img`, `!histo`, etc. pour enrichir la conversation.

- **Tests unitaires :**  
  Suite de tests permettant de valider les fonctionnalités et la performance des différents modules.

---

## Structure du Projet (simplifié)

```plaintext
3T/
├── log_3.3.1.txt
├── modules_tests.py
├── README.md
└── TTT/
    ├── __init__.py
    ├── api_requests.py       # Gestion des requets avec text-generation-webui (Text to Text)
    ├── audio_utils.py        # Génération d'audio via F5-TTS (Text to Speech)
    ├── commands.py           # Commandes (`!help`...)
    ├── config.py
    ├── dataset_cmd_img.json  # Dataset pour LoRA (Low Rank Adaptation) pour la génération d'images
    ├── image_api.py          # Génération d'images via API (Stable Diffusion)
    ├── image_BLIP.py         # Analyse d'images avec BLIP
    ├── main.py               # Chatbot en mode console
    ├── main_discord.py       # Bot Discord
    ├── stream_handler.py     # Module Whisper (Speech to Text)
    ├── text_processing.py
    ├── generated_images/     # Images générées par l'API
    │   ├── txt2img_20250220-194859_0.png
    │   └── txt2img_20250220-202032_0.png
    ├── saves/                # Sauvegardes du chat (en json avec la commande `!save <nom>`)
    │   └── test.json
    ├── send_images/          # Images destinées à être envoyées/analyées (séléctionne l'image la plus récente)
    │   ├── txt2img_20250220-194859_0.png
    │   └── txt2img_20250220-202422_0.png
    ├── tests/                # Tests unitaires avec la librairie unittest
    │   ├── __init__.py
    │   ├── audio_test.py
    │   ├── base.py
    │   ├── commands_test.py
    │   ├── image_test.py
    │   ├── textgen_test.py
    │   └── text_test.py
    ├── voices/               # Fichiers audio de référence
    │   └── 2B.wav
    └── voice_temp/           # Fichiers temporaires (ex. basic_config.toml et infer_cli_out.wav)
        └── basic_config.toml
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
python 3T/TTT/main.py
```

Le programme vous demandera de choisir le mode d'entrée (texte ou speech), le mode de sortie et le niveau de journalisation.

### Exécution des Tests

Pour lancer l'ensemble des tests unitaires (chois des modules intégré):

```bash
python 3T/modules_tests.py
```

Vous pouvez aussi lancer les tests individuels situés dans le dossier `3T/TTT/tests/`.

### Bot Discord

Pour lancer le bot Discord, procédez ainsi :

1. **Configurer le token Discord :**  
   Stocke ton token dans la variable d'environnement `DISCORD_BOT_TOKEN` ou dans un fichier `.env`.
   Ou remplacer directement le `DISCORD_BOT_TOKEN` par le token du bot discord.

2. **Lancer le bot :**

   ```bash
   python 3T/TTT/main_discord.py
   ```

Le bot répondra aux messages envoyés en mp.

- **Message texte :**  
  Le bot génère une réponse via le LLM en utilisant l'API de text-generation-webui.

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

## Dépendances Principales

- Python utilsé : 3.10.6
- [discord.py](https://discordpy.readthedocs.io/)
- [Transformers](https://huggingface.co/transformers/)
- [Pydub](https://github.com/jiaaro/pydub)
- [Requests](https://docs.python-requests.org/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- Autres bibliothèques utilisées dans le projet (voir `requirements.txt`)
Si une erreure de dépendance apparait, rechercher `<lib-name> pypi` pour l'installer avec pip facilement

---

## TOKEN Discord

Pour utiliser le module discord, il faut mettre son TOKEN discord (du bot) dans le fichier 3T/TTT/token.py (remplacer le "YOUR_DISCORD_TOKEN" par le token)

---

## Contribution

Les contributions sont les bienvenues !  
- Créez une branche pour vos modifications.
- Soumettez une Pull Request avec une description détaillée de vos changements.

---

## Licence

Ce projet est open-source et publié sous la licence MIT.
Auteur : Dragondefer

En cas de réutilisation du code, merci de citer l'auteur (Dragondefer) et d'y ajouter le lien du répertoire (https://github.com/Dragondefer/3T)

Certains composants s'appuient sur des outils et API externes tels que :
- Stable Diffusion WebUI
- Text Generation WebUI

Ces outils ne sont pas inclus dans ce dépôt et restent sous leurs propres licences. Veuillez vous référer à leurs référentiels respectifs pour les détails de licence et d'utilisation.

---

## Remarques

Ce projet vise à fournir une interface interactive et multimodale pour interagir avec un LLM, analyser des images et générer du contenu visuel.  
N'hésitez pas à signaler les bugs ou proposer des améliorations via [GitHub Issues](https://github.com/dragondefer/3T/issues).

---