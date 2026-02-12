def selection_agent(state):

    user_input = state["user_input"].strip()

    if not user_input.isdigit():
        state["response"] = "Please reply with a valid option number."
        return state

    index = int(user_input) - 1
    options = state.get("clarification_options", [])

    if index < 0 or index >= len(options):
        state["response"] = "Invalid selection. Please try again."
        return state

    selected_product = options[index]

    # 🔥 Preserve quantity data BEFORE modifying state
    preserved_quantity = state.get("quantity")
    preserved_mode = state.get("quantity_mode")
    preserved_unit = state.get("requested_unit")

    # 🔥 Set selected result
    state["results"] = [selected_product]

    # 🔥 Restore original intent
    state["intent"] = state.get("original_intent")

    # 🔥 Restore quantity data
    state["quantity"] = preserved_quantity
    state["quantity_mode"] = preserved_mode
    state["requested_unit"] = preserved_unit

    return state
