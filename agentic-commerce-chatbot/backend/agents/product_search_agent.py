from backend.services.product_service import hybrid_search
from backend.db.session import SessionLocal


def product_search_agent(state):

    db = SessionLocal()

    results = hybrid_search(
        db,
        query=state["user_input"],
        available_only=True,
        top_k=10
    )

    db.close()

    # 🔥 Always reset results
    state["results"] = []

    # =====================================================
    # 1️⃣ No Results
    # =====================================================

    if not results:
        state["response"] = "I couldn’t find matching products."
        return state

    query_lower = state["user_input"].lower()

    # =====================================================
    # 2️⃣ BRAND FILTERING
    # =====================================================

    brand_filtered = [
        row for row in results
        if row[3].lower() in query_lower
    ]

    if brand_filtered:
        results = brand_filtered

    # =====================================================
    # 3️⃣ PURE SEARCH INTENT → SHOW LIST
    # =====================================================

    if state.get("intent") == "search_product":

        product_list = "\n".join(
            [f"- {row[1]} ({row[4]}) – ₹{row[5]}" for row in results]
        )

        state["response"] = f"Here are the available options:\n{product_list}"
        return state

    # =====================================================
    # 4️⃣ ADD / REMOVE FLOW
    # =====================================================

    state["results"] = results

    # If only one product → skip clarification
    if len(results) == 1:
        return state

    # Multiple results → clarification
    state["original_intent"] = state.get("intent")
    state["intent"] = "clarify"
    state["clarification_options"] = results

    return state