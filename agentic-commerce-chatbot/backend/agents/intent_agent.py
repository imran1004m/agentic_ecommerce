from backend.core.llm_client import chat_completion
import re


VALID_INTENTS = {
    "search_product",
    "add_to_cart",
    "remove_from_cart",
    "place_order",
    "track_order",
    "view_cart",
    "select_option",
    "small_talk",
    "unknown"
}


def detect_intent(state):

    user_input = state["user_input"].strip().lower()

    # 1️⃣ Selection handling
    if user_input.isdigit():
        state["intent"] = "select_option"
        return state

    # 2️⃣ Small talk
    greetings = ["hi", "hello", "hey", "good morning", "good evening"]
    if user_input in greetings:
        state["intent"] = "small_talk"
        state["response"] = "Hello! How can I help you with your shopping today?"
        return state

    if any(word in user_input for word in ["thank", "thanks"]):
        state["intent"] = "small_talk"
        state["response"] = "You're welcome! Happy shopping 😊"
        return state

    # 3️⃣ Quantity mode
    if "total" in user_input:
        state["quantity_mode"] = "set_total"
    else:
        state["quantity_mode"] = "increment"

    # 4️⃣ Extract quantity + unit
    quantity_match = re.search(
        r'\b(\d+)\s*(kg|kgs|kilogram|kilograms|l|ltr|litre|litres|liter|liters|packet|packets|unit|units)?\b',
        user_input
    )

    if quantity_match:
        state["quantity"] = int(quantity_match.group(1))
        unit = quantity_match.group(2)

        if unit:
            unit = unit.lower()
            if unit in ["kg", "kgs", "kilogram", "kilograms"]:
                state["requested_unit"] = "kg"
            elif unit in ["l", "ltr", "litre", "litres", "liter", "liters"]:
                state["requested_unit"] = "l"
            elif unit in ["packet", "packets", "unit", "units"]:
                state["requested_unit"] = "packet"
            else:
                state["requested_unit"] = None
        else:
            state["requested_unit"] = None
    else:
        state["quantity"] = 1
        state["requested_unit"] = None

    # 5️⃣ LLM Intent classification
    prompt = """
You are an ecommerce intent classifier.

Strictly classify the user input into exactly ONE of these labels:

- search_product
- add_to_cart
- remove_from_cart
- place_order
- track_order
- view_cart
- unknown

Rules:
- If user says "remove", "delete", "reduce" → remove_from_cart
- If user says "show cart", "view cart" → view_cart
- If user says "place order", "checkout" → place_order
- If user says "add", "put in cart" → add_to_cart
- If asking product info → search_product

Return ONLY the label.
"""

    intent = chat_completion(prompt, state["user_input"]).strip().lower()

    if intent not in VALID_INTENTS:
        intent = "unknown"

    state["intent"] = intent
    return state
