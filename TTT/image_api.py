__version__ = 54

import requests
import base64
import json
import os
from datetime import datetime

from config import (IMG_API_URL, OUTPUT_DIR)

# Création du répertoire de sauvegarde des images générées
os.makedirs(OUTPUT_DIR, exist_ok=True)

def timestamp():
    """Renvoie un timestamp formaté pour le nom de fichier."""
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def open_last_image(image_dir:str=OUTPUT_DIR) -> None:
    valid_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}
    # liste les fichiers d'img dans le dossier
    image_files = [
        os.path.join(image_dir, f)
        for f in os.listdir(image_dir)
        if os.path.splitext(f)[1].lower() in valid_extensions
    ]
    
    if not image_files:
        print("Aucune image trouvée dans le dossier.")
        return
    
    latest_image = max(image_files, key=os.path.getmtime)
    print("Ouverture de l'image la plus récente :", latest_image)
    
    os.startfile(latest_image)

def generate_image(prompt: str,
                   steps: int = 20,
                   width: int = 512,
                   height: int = 512,
                   seed: int = None,
                   cfg_scale: float = 7,
                   sampler_name: str = "DPM++ 2M",  # ou "Euler"
                   batch_size: int = 1,
                   n_iter: int = 1,
                   output_dir: str = OUTPUT_DIR,
                   **extra_params) -> list:
    """
    Génère une image à partir d’un prompt en appelant l’API txt2img de Stable Diffusion WebUI.
    
    Paramètres :
      - prompt: La description textuelle de l’image.
      - steps: Nombre d’étapes de diffusion (20 par défaut).
      - width, height: Dimensions de l’image (512x512 par défaut).
      - seed: Graine pour la reproductibilité (optionnel).
      - cfg_scale: Force de la guidance (7 par défaut).
      - sampler_name: Nom du sampler (ex: "Euler").
      - batch_size: Nombre d’images générées par itération.
      - n_iter: Nombre d’itérations (pour changer la seed automatiquement si besoin).
      - output_dir: Répertoire de sauvegarde.
      - extra_params: D’autres paramètres (comme "negative_prompt", "enable_hr", etc.).
      
    Retourne une liste de chemins vers les fichiers images générés.
    """

    payload = {
        "prompt": prompt,
        "steps": steps,
        "width": width,
        "height": height,
        "cfg_scale": cfg_scale,
        "sampler_name": sampler_name,
        "batch_size": batch_size,
        "n_iter": n_iter,
    }

    if seed is not None:
        payload["seed"] = seed

    payload.update(extra_params)

    url = f"{IMG_API_URL}/sdapi/v1/txt2img"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        if response.text:
            result = response.json()
        else:
            print("Réponse vide de l'API.")
            return []
    except requests.exceptions.RequestException as e:
        print("Erreur lors de la requête :", e)
        return []
    except Exception as e:
        print("DEBUG:", e)
        return []

    saved_files = []

    if "images" not in result:
        print("Aucune image retournée par l'API.")
        return saved_files

    # traitement de la liste d'img base64
    for idx, img_str in enumerate(result.get("images", [])):
        try:
            # si "data:image/png;base64," ; alors on récup après la virgule (pour eviter une erreur potentiel)
            img_data = base64.b64decode(img_str.split(",", 1)[-1])
            filename = f"txt2img_{timestamp()}_{idx}.png"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "wb") as f:
                f.write(img_data)
            saved_files.append(filepath)
        except Exception as e:
            print(f"Erreur lors du décodage ou de la sauvegarde de l'image {idx} :", e)
    
    return saved_files

if __name__ == '__main__':
    files = generate_image(prompt="A futuristic cityscape at sunset", negative_prompt="low quality", steps=30)
    print("Images sauvegardées :", files)
    open_last_image()
