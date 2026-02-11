from backend.core.llm_client import chat_completion

VALID_INTENTS = {
    "search_product",
    "add_to_cart",
    "place_order",
    "track_order",
    "view_cart",
    "unknown"
}


def detect_intent(state):
    prompt = """
You are an ecommerce intent classifier.

Strictly classify the user input into exactly ONE of these labels:

- search_product  → user is searching or asking about a product
- add_to_cart     → user wants to add an item to cart
- place_order     → user wants to confirm or place order
- track_order     → user wants order status
- view_cart       → user wants to see cart contents
- unknown         → anything else

Rules:
- If user says "show my cart", "view cart", or "what is in my cart", return view_cart.
- If user says "place order" or "checkout", return place_order.
- If user says "add", return add_to_cart.
- If user is asking about a product, return search_product.

Return ONLY the label. No explanation.
"""


    intent = chat_completion(prompt, state["user_input"]).strip().lower()

    if intent not in VALID_INTENTS:
        intent = "unknown"

    state["intent"] = intent
    return state
