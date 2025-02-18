import logging
import time
from colorama import Fore, init
from voice_assistant.audio import record_audio, play_audio
from voice_assistant.transcription import transcribe_audio
from voice_assistant.response_generation import generate_response
from voice_assistant.text_to_speech import text_to_speech
from voice_assistant.config import Config
from voice_assistant.api_key_manager import get_transcription_api_key, get_response_api_key, get_tts_api_key
from voice_assistant.prompts.core import PromptSystem
from voice_assistant.prompts.intent_handler import IntentHandler
from voice_assistant.data.menu_data import MenuData

# Configure logging and init colorama
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
init(autoreset=True)

def main():
    """Main function to run the voice assistant."""
    current_intent = "general"
    chat_history = [{"role": "system", "content": PromptSystem.BASE_PROMPT}]

    while True:
        try:
            # Record and transcribe audio
            record_audio(Config.INPUT_AUDIO)
            transcription_api_key = get_transcription_api_key()
            user_input = transcribe_audio(Config.TRANSCRIPTION_MODEL,
                                        transcription_api_key,
                                        Config.INPUT_AUDIO,
                                        Config.LOCAL_MODEL_PATH)

            if not user_input:
                logging.info("No transcription detected. Starting recording again.")
                continue

            logging.info(Fore.GREEN + "User: " + user_input + Fore.RESET)

            if "goodbye" in user_input.lower():
                break

            # Update intent and prompt if needed
            new_intent = IntentHandler.detect_intent(user_input)
            if new_intent != current_intent:
                current_intent = new_intent
                base_prompt = IntentHandler.get_prompt_for_intent(current_intent)
                if current_intent == "order":
                    menu_prompt = PromptSystem.get_order_prompt(MenuData)
                    full_prompt = f"{base_prompt}\n\n{menu_prompt}"
                else:
                    full_prompt = base_prompt

                chat_history = [{"role": "system", "content": full_prompt}]

            # Add menu context for order-related queries
            if current_intent == "order":
                menu_items = MenuData.get_all_menu_items()
                item_names = [item["name"].lower() for item in menu_items]
                for item_name in item_names:
                    if item_name in user_input.lower():
                        matching_item = next((item for item in menu_items if item["name"].lower() == item_name), None)
                        if matching_item:
                            chat_history.append({
                                "role": "system",
                                "content": f"Customer mentioned {matching_item['name']} (Price: {MenuData.format_price(matching_item['price'])})"
                            })

            # Add user input to chat history
            chat_history.append({"role": "user", "content": user_input})

            # Generate and process response
            response_api_key = get_response_api_key()
            response_text = generate_response(Config.RESPONSE_MODEL,
                                           response_api_key,
                                           chat_history,
                                           Config.LOCAL_MODEL_PATH)

            logging.info(Fore.CYAN + "Nsuna: " + response_text + Fore.RESET)
            chat_history.append({"role": "assistant", "content": response_text})

            # Handle text-to-speech
            output_file = 'output.mp3' if Config.TTS_MODEL in ['openai', 'elevenlabs', 'melotts', 'cartesia'] else 'output.wav'
            tts_api_key = get_tts_api_key()
            text_to_speech(Config.TTS_MODEL, tts_api_key, response_text, output_file, Config.LOCAL_MODEL_PATH)

            if Config.TTS_MODEL != "cartesia":
                play_audio(output_file)

        except Exception as e:
            logging.error(Fore.RED + f"An error occurred: {e}" + Fore.RESET)
            time.sleep(1)

if __name__ == "__main__":
    main()
