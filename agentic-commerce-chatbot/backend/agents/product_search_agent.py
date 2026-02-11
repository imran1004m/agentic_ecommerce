from backend.services.product_service import hybrid_search
from backend.db.session import SessionLocal


SIMILARITY_THRESHOLD = 1.0


def product_search_agent(state):

    db = SessionLocal()

    results = hybrid_search(
        db,
        query=state["user_input"],
        available_only=True,
        top_k=5
    )

    db.close()

    if not results:
        state["response"] = "No matching products found."
        return state

    strong_matches = []

    for row in results:
        distance = row[-1]
        print("Distance:", distance)
        if distance <= SIMILARITY_THRESHOLD:
            strong_matches.append(row)

    if not strong_matches:
        state["response"] = "No closely matching products found."
        return state

    state["results"] = strong_matches

    # 🔥 AUTO ROUTING LOGIC

    # Case 1: Single strong match + add_to_cart intent
    if len(strong_matches) == 1 and state.get("intent") == "add_to_cart":
        # Do NOT change intent — supervisor will route to cart
        return state

    # Case 2: Multiple strong matches
    if len(strong_matches) > 1:
        state["intent"] = "clarify"
        return state

    # Case 3: Single strong match + search only
    state["response"] = f"Found product: {strong_matches[0][1]}"
    return state
