def clarification_agent(state):

    results = state.get("results")

    if not results:
        state["response"] = "I couldn’t find matching products."
        return state

    # Store options for next turn
    state["clarification_options"] = results

    message = "Did you mean:\n"

    for idx, row in enumerate(results, start=1):
        message += f"{idx}. {row[1]}\n"

    message += "\nPlease reply with the option number."

    state["response"] = message
    return state
