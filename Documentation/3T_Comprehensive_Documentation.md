# 3T - Chatbot Multimodal - Comprehensive Detailed Documentation

## 1. Project Overview

3T is an advanced multimodal chatbot system designed to interact with users through multiple input and output modalities, primarily text and speech. It integrates state-of-the-art AI models and APIs to provide rich conversational experiences enhanced with image generation and analysis capabilities. The project is modular, extensible, and supports real-time interaction via a Discord bot.

## 2. Core Features and Capabilities

- **Multimodal Interaction:**  
  Users can interact via text or speech input, and receive responses in text or synthesized speech, enabling flexible communication modes.

- **Text Generation:**  
  Utilizes a large language model (LLM) accessed through a text-generation API to generate context-aware, character-driven responses.

- **Image Generation:**  
  Integrates with Stable Diffusion WebUI API to generate high-quality images from textual prompts, enriching the conversational experience.

- **Image Analysis:**  
  Employs the BLIP model to analyze user-sent images, extracting descriptive captions that are incorporated into the conversation context.

- **Discord Bot Integration:**  
  Provides a Discord bot interface allowing users to chat, send images, and receive generated images directly within Discord channels or private messages.

- **Custom Commands:**  
  Supports a rich set of commands for managing conversation history, switching characters, controlling debug levels, and interacting with the LLM lifecycle.

- **Speech Processing:**  
  Uses Whisper for speech-to-text transcription and f5-tts for text-to-speech synthesis, enabling natural voice interactions.

- **Testing Suite:**  
  Includes unit tests covering core modules to ensure reliability and facilitate maintenance.

## 3. Architecture and Module Details

### 3.1 Main Application Modules

- **TTT/main.py:**  
  The console-based chatbot application. It manages user input (text or speech), processes messages, sends requests to the LLM API, and outputs responses in the chosen mode. It handles command inputs and supports debug logging.

- **TTT/main_discord.py:**  
  Implements the Discord bot using discord.py. It listens for messages and attachments, processes commands, handles image uploads by saving and analyzing them, and generates images on demand. It asynchronously communicates with the LLM API and sends responses back to Discord.

### 3.2 AI and API Integration

- **TTT/api_requests.py:**  
  Manages communication with the text generation API. Maintains conversation history, handles model loading/unloading, and sends chat messages with context and character information.

- **TTT/image_api.py:**  
  Interfaces with the Stable Diffusion WebUI API to generate images from prompts. Handles API requests, decodes base64 image data, saves images locally, and provides utilities to open the latest generated image.

- **TTT/image_BLIP.py:**  
  Uses the BLIP model from Hugging Face transformers to generate captions describing images. It processes images saved locally and returns textual descriptions to enrich conversation prompts.

### 3.3 Speech Processing

- **TTT/stream_handler.py:**  
  Handles real-time audio input streaming, voice activity detection, recording, and transcription using the Whisper model. It buffers audio, detects speech segments, writes WAV files, and transcribes them to text.

- **TTT/audio_utils.py:**  
  Generates speech audio from text using the f5-tts tool. It creates configuration files, runs the external TTS command, renames output files, and plays audio responses using ffplay.

### 3.4 Command Handling

- **TTT/commands.py:**  
  Implements a suite of commands for user interaction, including saving/loading conversation history, switching characters, adjusting debug levels, and managing the LLM lifecycle. Commands can be invoked in both console and Discord modes.

### 3.5 Configuration

- **config.py:**  
  Centralizes configuration parameters such as API URLs, file paths, character definitions, generation parameters, and debug settings. It also manages conversation history and current character state.

## 4. Installation and Setup

- Clone the repository and optionally create a Python virtual environment.
- Install dependencies listed in `requirements.txt`.
- Configure Discord bot token in `3T/TTT/token.py` or environment variables.
- Adjust paths and character settings in `config.py` as needed.

## 5. Usage Scenarios

- **Console Chatbot:**  
  Run `python 3T/TTT/main.py` to start the chatbot in console mode. Choose input/output modes and interact via text or speech.

- **Discord Bot:**  
  Run `python 3T/TTT/main_discord.py` to start the Discord bot. Use Discord to chat, send images for analysis, or generate images with commands.

- **Image Generation:**  
  Use `img(<prompt>)` commands to generate images via Stable Diffusion API.

- **Image Analysis:**  
  Send images to the Discord bot to receive descriptive captions generated by BLIP.

- **Speech Interaction:**  
  Speak to the console chatbot for transcription and receive spoken responses.

## 6. Testing

- Run all unit tests with `python 3T/modules_tests.py`.
- Tests cover audio processing, commands, image generation and analysis, and text generation modules.
- Recommended to test all interaction modes and commands for robustness.

## 7. Future Directions and Potential

- **Android Implementation:**  
  Develop an Android application integrating speech input/output and chatbot features for mobile use, enabling natural voice conversations on the go.

- **Enhanced Speech Capabilities:**  
  Improve speech recognition accuracy and naturalness of synthesized speech for more fluid interactions.

- **Additional Modalities:**  
  Explore adding video, gesture, or other input/output modalities to expand interaction possibilities.

- **User Interface Improvements:**  
  Create web or mobile user interfaces for richer and more accessible user experiences.

- **Extended Integrations:**  
  Integrate with other platforms and APIs to broaden the chatbot's applicability and reach.

## 8. Contribution and Licensing

- Contributions are welcome via pull requests with clear descriptions.
- The project is open-source under the MIT License.
- Please cite the author (Dragondefer) and repository link when reusing code.

---

This documentation synthesizes the current state and future potential of the 3T multimodal chatbot project, providing a comprehensive guide for users and developers.
