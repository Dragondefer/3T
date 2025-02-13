import requests
import base64
import json
import os
from datetime import datetime

# URL du serv WebUI
WEBUI_SERVER_URL = 'http://127.0.0.1:7860'
# fichier de save des images générées
OUTPUT_DIR = 'generated_images'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def timestamp():
    """Renvoie un timestamp formaté pour le nom de fichier."""
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def generate_image(prompt: str,
                   steps: int = 20,
                   width: int = 512,
                   height: int = 512,
                   seed: int = None,
                   cfg_scale: float = 7,
                   sampler_name: str = "DPM++ 2M", # ou "Euler"
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
    # payload avec params de base
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
    # add la seed (si précisée)
    if seed is not None:
        payload["seed"] = seed
    # add tous les params supp
    payload.update(extra_params)

    # appel à l’API txt2img
    url = f"{WEBUI_SERVER_URL}/sdapi/v1/txt2img"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    
    saved_files = []
    # résult contient une liste d’img encodées en base64
    for idx, img_str in enumerate(result.get("images", [])):
        # parfois chaîne est préfixée par "data:image/png;base64," mais on veut que la partie après la virgule
        img_data = base64.b64decode(img_str.split(",", 1)[-1])
        filename = f"txt2img_{timestamp()}_{idx}.png"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "wb") as f:
            f.write(img_data)
        saved_files.append(filepath)
    
    return saved_files


if __name__ == '__main__':
    files = generate_image(prompt="A futuristic cityscape at sunset", negative_prompt="low quality", steps=30)
    print("Images sauvegardées :", files)
