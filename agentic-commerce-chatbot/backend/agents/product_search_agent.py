from backend.services.product_service import hybrid_search
from backend.db.session import SessionLocal


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

    query_lower = state["user_input"].lower()

    # 🔥 1️⃣ Exact keyword containment boost (true hybrid behavior)
    exact_matches = [
        row for row in results
        if any(word in row[1].lower() for word in query_lower.split())
    ]

    if exact_matches:
        # Take best exact match
        state["results"] = [exact_matches[0]]
        return state

    # 🔥 2️⃣ Semantic filtering (fallback)

    best_distance = results[0][-1]

    # Hard rejection threshold
    MAX_ALLOWED_DISTANCE = 1.15

    if best_distance > MAX_ALLOWED_DISTANCE:
        state["response"] = "Sorry, we couldn't find that product."
        return state

    # Adaptive tolerance
    tolerance = 0.25

    strong_matches = [
        row for row in results
        if row[-1] <= best_distance + tolerance
    ]

    # Debug
    for row in strong_matches:
        print("Accepted Distance:", row[-1])

    if not strong_matches:
        state["response"] = "No closely matching products found."
        return state

    state["results"] = strong_matches

    # 🔥 3️⃣ Clarification logic

    if len(strong_matches) > 1:
        state["original_intent"] = state.get("intent")
        state["intent"] = "clarify"
        state["clarification_options"] = strong_matches
        return state

    # 🔥 4️⃣ Single match
    return state
