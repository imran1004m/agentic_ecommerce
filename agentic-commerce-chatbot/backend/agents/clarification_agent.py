def clarification_agent(state):
    """
    Triggered when multiple similar products found.
    """

    results = state.get("results")

    if not results:
        state["response"] = "I couldn’t find matching products."
        return state

    product_names = [r[1] for r in results]

    message = "Did you mean:\n"

    for name in product_names:
        message += f"- {name}\n"

    state["response"] = message
    return state
