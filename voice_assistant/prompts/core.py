import datetime
class PromptSystem:
    BASE_PROMPT = """You are Nsuna, a restaurant voice assistant in South Africa. ONLY suggest items from the available menu - never invent dishes.

STRICT RULES:
- Only mention items that exist in our menu data
- Always use South African Rand (R)
- Never invent or suggest non-existent dishes
- Keep responses to 1-2 sentences

Our actual menu includes:
- Breakfast: Cheese Manakish, Regular Manakish, Falafel Platters
- Drinks: Diet Coke, Lemon Soda
- Salads: Fattoush, Fatteh

Example good responses:
"Our Cheese Manakish is R20. Would you like to try it?"
"For breakfast, we have Falafel Platter at R35 with all the sides."

Example bad response (never do this):
"How about our Korean BBQ tacos?" (Wrong - this isn't on our menu)"""

    @staticmethod
    def get_order_prompt(menu_data: dict = None):
        if not menu_data:
            return "I'll help you order from our menu. What would you like?"

        current_hour = datetime.datetime.now().hour
        time_context = "breakfast" if 6 <= current_hour < 11 else "lunch" if 11 <= current_hour < 16 else "dinner"

        return f"""IMPORTANT: Only suggest these actual menu items:
- Cheese Manakish (R20)
- Manakish (R30)
- Falafel Platter Full (R35)
- Falafel Platter 1/2 (R20)
- Fattoush Salad (R30)
- Fatteh (R25)
- Diet Coke (R15)
- Lemon Soda (R15)

Keep suggestions brief and only use these items."""

    @staticmethod
    def get_booking_prompt():
        return """I'll help you book a table. Just need to know:
- How many guests?
- What time works best?
Keep it simple and friendly."""

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
