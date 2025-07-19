import asyncio
import traceback

from stream_handler import StreamHandler
from api_requests import request_textgen
from text_processing import extraire_dialogues_et_actions, handle_message, handle_answer
from audio_utils import generate_audio, play_audio
from config import characters, get_current_character, debug_mode
from commands import handle_commands

# Pour simplifier, ici nous considérons uniquement le mode texte.
# Vous pouvez étendre cette version pour supporter le mode "speech" si besoin.
async def chat_session(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    # Envoi de la configuration initiale
    character_config = characters[get_current_character()]
    writer.write(f"Configuration du personnage: {character_config}\n".encode())
    writer.write(b"Bienvenue sur le chat interactif (mode texte).\n")
    writer.write(b"Tapez vos messages pour converser.\n")
    await writer.drain()

    # Pour ce serveur, nous fixons par défaut input_mode et output_mode à "1" (texte)
    input_mode = "1"
    output_mode = "1"
    client_debug_mode = debug_mode  # niveau de debug (par exemple "1" ou "2")
    
    while True:
        try:
            writer.write(b"> ")
            await writer.drain()
            data = await reader.readline()
            if not data:
                break  # fin de la connexion
            user_input = data.decode().strip()
            if not user_input:
                continue

            # Si c'est une commande (commence par "!")
            if input_mode == "1" and user_input.startswith("!"):
                try:
                    handle_commands(user_input)
                    writer.write(b"Commande exécutée.\n")
                    await writer.drain()
                except Exception as e:
                    writer.write(f"Erreur lors de la commande: {e}\n".encode())
                    await writer.drain()
                continue

            # PART 1 : Traitement du message utilisateur
            processed_message = handle_message(user_input)
            if client_debug_mode >= "2":
                writer.write(f"DEBUG: Message traité: {processed_message}\n".encode())
                await writer.drain()

            # PART 2 : Envoi de la requête à l'API
            assistant_message = request_textgen(processed_message, debug=client_debug_mode)
            if client_debug_mode >= "2":
                writer.write(f"DEBUG: Message assistant généré: {assistant_message}\n".encode())
                await writer.drain()

            # Traitement de la réponse
            assistant_message = handle_answer(response=assistant_message, StS=(input_mode == "2"))
            if client_debug_mode >= "2":
                writer.write(f"DEBUG: Message assistant traité: {assistant_message}\n".encode())
                await writer.drain()

            # PART 3 : Envoi de la réponse (mode texte)
            if output_mode == "1":
                writer.write((assistant_message + "\n").encode())
                await writer.drain()
            else:
                # Option audio (non testé dans ce serveur)
                dialogue, action = extraire_dialogues_et_actions(assistant_message)
                generate_audio(dialogue=dialogue, debug=client_debug_mode)
                play_audio()
                writer.write(b"Audio généré et joué sur le serveur.\n")
                await writer.drain()

        except Exception as e:
            writer.write(f"Erreur: {e}\n".encode())
            await writer.drain()
            traceback.print_exc()
    writer.write(b"Fin de la session.\n")
    await writer.drain()
    writer.close()

async def main():
    # Lance le serveur sur toutes les interfaces du gros PC, port 8888 (modifiable)
    server = await asyncio.start_server(chat_session, "0.0.0.0", 8888)
    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"Serveur lancé sur {addrs}")
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
