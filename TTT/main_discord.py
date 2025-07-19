__version__ = 36

import os
import re
import discord
import asyncio
import traceback

from discord.ext import commands

from stream_handler import StreamHandler
from api_requests import request_textgen
from text_processing import extraire_dialogues_et_actions, handle_message, handle_answer
from audio_utils import generate_audio, play_audio
from config import characters, change_character, get_current_character, send_image_dir, debug_mode
from commands import handle_commands

from image_BLIP import describe_image
from image_api import generate_image

"""
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    raise ValueError("Token Discord non trouvé.")
    input(votre token discord: )
"""


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"3T connecté en tant que {bot.user}")
    character_config = characters[get_current_character()]
    print("Personnage courant:", character_config)

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    if message.content.startswith("!"):
        try:
            handle_commands(message.content)
            await message.channel.send("Commande exécutée.")
        except Exception as e:
            await message.channel.send(f"Erreur lors de l'exécution de la commande: {e}")
            traceback.print_exc()

        return

    full_prompt = message.content.strip()

    if message.attachments:
        valid_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}
        image_attachments = [att for att in message.attachments if os.path.splitext(att.filename)[1].lower() in valid_extensions]
        if image_attachments:
            attachment = image_attachments[0]
            local_filepath = os.path.join(send_image_dir, attachment.filename)
            try:
                await attachment.save(local_filepath)
                description = describe_image(local_filepath)
                if full_prompt:
                    full_prompt = f"{full_prompt} (image description: {description})"
                else:
                    full_prompt = f"(image description: {description})"
                os.remove(local_filepath)
            except Exception as e:
                await message.channel.send(f"Erreur lors de l'analyse de l'image: {e}")
                traceback.print_exc()

    if full_prompt.lower().startswith("img("):
        match = re.search(r"img\((.*?)\)", full_prompt, re.IGNORECASE)
        if match:
            prompt_text = match.group(1).strip()
            await message.channel.send("Génération de l'image en cours...")
            loop = asyncio.get_event_loop()
            image_files = await loop.run_in_executor(None, generate_image, prompt_text)
            if image_files:
                await message.channel.send("Image générée :", file=discord.File(image_files[0]))
            else:
                await message.channel.send("Erreur lors de la génération de l'image.")
        return

    try:
        if debug_mode >= 2: print("DEBUG: Message utilisateur capté:", full_prompt)

        processed_message = handle_message(full_prompt)

        if debug_mode >= 2: print("DEBUG: Message traité:", processed_message)

        loop = asyncio.get_event_loop()
        assistant_message = await loop.run_in_executor(None, request_textgen, processed_message, debug_mode)

        if debug_mode >= 2: print("DEBUG: Message assistant généré:", assistant_message)

        assistant_message = handle_answer(response=assistant_message, StS=False)

        if debug_mode >= 2: print("DEBUG: Message assistant traité:", assistant_message)

        await message.channel.send(assistant_message)
        
    except Exception as e:
        error_text = f"Erreur: {str(e)}"
        await message.channel.send(error_text)
        traceback.print_exc()


from token import TOKEN

bot.run(TOKEN)
