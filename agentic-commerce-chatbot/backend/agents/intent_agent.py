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

    # ======================================
    # 1️⃣ Selection Handling
    # ======================================
    if user_input.isdigit():
        state["intent"] = "select_option"
        return state

    # ======================================
    # 2️⃣ Small Talk
    # ======================================
    if user_input in ["hi", "hello", "hey"]:
        state["intent"] = "small_talk"
        state["response"] = "Hello! How can I help you with your shopping today?"
        return state

    if "thank" in user_input:
        state["intent"] = "small_talk"
        state["response"] = "You're welcome! Happy shopping 😊"
        return state

    # ======================================
    # 3️⃣ Quantity Mode
    # ======================================
    state["quantity_mode"] = "set_total" if "total" in user_input else "increment"

    # ======================================
    # 4️⃣ STRONG Quantity + Unit Extraction (RESTORED)
    # ======================================

    quantity_unit_match = re.search(
        r'(\d+)\s*(kg|kgs|kilogram|kilograms|'
        r'l|ltr|litre|litres|liter|liters|'
        r'packet|packets|unit|units)\b',
        user_input
    )

    if quantity_unit_match:
        state["quantity"] = int(quantity_unit_match.group(1))
        unit = quantity_unit_match.group(2).lower()

        if unit in ["kg", "kgs", "kilogram", "kilograms"]:
            state["requested_unit"] = "kg"

        elif unit in ["l", "ltr", "litre", "litres", "liter", "liters"]:
            state["requested_unit"] = "l"

        elif unit in ["packet", "packets", "unit", "units"]:
            state["requested_unit"] = "packet"

        else:
            state["requested_unit"] = None

    else:
        quantity_only_match = re.search(r'\b(\d+)\b', user_input)

        if quantity_only_match:
            state["quantity"] = int(quantity_only_match.group(1))
        else:
            state["quantity"] = 1

        state["requested_unit"] = None

    # ======================================
    # 5️⃣ CONTEXT: "add to cart"
    # ======================================
    if user_input in ["add to cart", "add"]:
        if state.get("results"):
            state["intent"] = "add_to_cart"
            return state

    # ======================================
    # 6️⃣ Rule-Based Intent Detection
    # ======================================

    if any(word in user_input for word in ["add", "buy", "purchase"]):
        state["intent"] = "add_to_cart"

    elif any(word in user_input for word in ["remove", "delete"]):
        state["intent"] = "remove_from_cart"

    elif "show cart" in user_input:
        state["intent"] = "view_cart"

    elif any(phrase in user_input for phrase in [
    "place order",
    "place the order",
    "checkout",
    "complete order",
    "confirm order"
]):
        state["intent"] = "place_order"

    elif any(word in user_input for word in ["show", "list", "display", "available", "brand"]):
        state["intent"] = "search_product"

    else:
        state["intent"] = "search_product"

    return state