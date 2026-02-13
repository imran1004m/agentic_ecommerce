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

    # =====================================================
    # 1️⃣ Selection Handling
    # =====================================================
    if user_input.isdigit():
        state["intent"] = "select_option"
        return state

    # =====================================================
    # 2️⃣ Small Talk Handling
    # =====================================================
    greetings = ["hi", "hello", "hey", "good morning", "good evening"]

    if user_input in greetings:
        state["intent"] = "small_talk"
        state["response"] = "Hello! How can I help you with your shopping today?"
        return state

    if any(word in user_input for word in ["thank", "thanks"]):
        state["intent"] = "small_talk"
        state["response"] = "You're welcome! Happy shopping 😊"
        return state

    # =====================================================
    # 3️⃣ Quantity Mode Detection
    # =====================================================
    if "total" in user_input:
        state["quantity_mode"] = "set_total"
    else:
        state["quantity_mode"] = "increment"

    # =====================================================
    # 4️⃣ Quantity + Unit Extraction
    # =====================================================
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

    # =====================================================
    # 5️⃣ RULE-BASED INTENT DETECTION (ORDER MATTERS)
    # =====================================================

    # 🔴 Order is critical here

        # =====================================================
    # 5️⃣ RULE-BASED INTENT DETECTION (FINAL FIX)
    # =====================================================

    # ADD
    if any(word in user_input for word in ["add", "buy", "purchase"]):
        state["intent"] = "add_to_cart"

    # REMOVE
    elif any(word in user_input for word in ["remove", "delete", "reduce"]):
        state["intent"] = "remove_from_cart"

    # VIEW CART
    elif any(phrase in user_input for phrase in ["show cart", "view cart"]):
        state["intent"] = "view_cart"

    # 🔥 PLACE ORDER (STRONG FIX)
    elif any(phrase in user_input for phrase in ["place order", "place the order", "checkout", "confirm order"]):
        state["intent"] = "place_order"

    # 🔥 SEARCH / SHOW PRODUCTS
    elif any(word in user_input for word in ["show", "list", "display", "available", "brand"]):
        state["intent"] = "search_product"

    else:
        state["intent"] = "search_product"


    return state
