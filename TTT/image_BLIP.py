import os
import time
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

from config import send_image_dir

device = "cuda" if torch.cuda.is_available() else "cpu"
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)


def get_latest_image(directory):
    """ Trouve l'image la plus récente dans le dossier donné. """
    valid_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}
    image_files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in valid_extensions]

    if not image_files:
        return None

    return max(image_files, key=os.path.getmtime)

def describe_image(image_path):
    """ Génère une description de l'image avec BLIP. """
    from PIL import Image
    image = Image.open(image_path).convert("RGB")
    
    inputs = processor(image, return_tensors="pt").to(device)
    caption = model.generate(**inputs)
    description = processor.batch_decode(caption, skip_special_tokens=True)[0]
    
    return description

def process_message(message):
    """ Vérifie si le message contient !img et ajoute la description de l'image. """
    if "!img" in message:
        latest_image = get_latest_image(send_image_dir)
        if latest_image:
            description = describe_image(latest_image)
            return f"{message.replace('!img', '')} (image desc: {description})"
        else:
            return message + " (Aucune image trouvée.)"
    return message

if __name__ == '__main__':
    user_input = "yo watch this !img"
    processed_message = process_message(user_input)
    print("Message final pour le LLM:", processed_message)
