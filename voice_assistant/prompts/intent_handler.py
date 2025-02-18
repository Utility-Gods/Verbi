
from voice_assistant.prompts.core import PromptSystem


class IntentHandler:
    INTENTS = {
        'order': {
            'keywords': ['order', 'food', 'eat', 'menu', 'drink', 'hungry'],
            'base_prompt': "Let me tell you about our available dishes."
        },
        'booking': {
            'keywords': ['book', 'reserve', 'table', 'seat', 'reservation'],
            'base_prompt': "I'll help you book a table."
        }
    }

    @staticmethod
    def detect_intent(user_input: str) -> str:
        user_input = user_input.lower()
        for intent, data in IntentHandler.INTENTS.items():
            if any(keyword in user_input for keyword in data['keywords']):
                return intent
        return "general"

    @staticmethod
    def get_prompt_for_intent(intent: str) -> str:
        if intent in IntentHandler.INTENTS:
            return IntentHandler.INTENTS[intent]['base_prompt']
        return PromptSystem.BASE_PROMPT
