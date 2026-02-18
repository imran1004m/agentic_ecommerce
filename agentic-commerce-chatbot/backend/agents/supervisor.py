from langgraph.graph import StateGraph, END

from backend.agents.state import AgentState
from backend.agents.intent_agent import detect_intent
from backend.agents.product_search_agent import product_search_agent
from backend.agents.clarification_agent import clarification_agent
from backend.agents.selection_agent import selection_agent
from backend.agents.cart_agent import cart_agent
from backend.agents.remove_agent import remove_agent
from backend.agents.order_agent import order_agent
from backend.agents.view_cart_agent import view_cart_agent


def build_graph():

    graph = StateGraph(AgentState)

    # 🔹 Nodes
    graph.add_node("intent", detect_intent)
    graph.add_node("search", product_search_agent)
    graph.add_node("clarify", clarification_agent)
    graph.add_node("select", selection_agent)
    graph.add_node("cart", cart_agent)
    graph.add_node("remove", remove_agent)
    graph.add_node("view_cart", view_cart_agent)
    graph.add_node("order", order_agent)

    # 🔹 Entry Point
    graph.set_entry_point("intent")

    # ===============================
    # 🔥 Intent Routing
    # ===============================

    def route_intent(state):

        intent = state.get("intent")

        if intent in ["search_product", "add_to_cart", "remove_from_cart"]:
            return "search"

        if intent == "view_cart":
            return "view_cart"

        if intent == "place_order":
            return "order"

        if intent == "select_option":
            return "select"

        return END

    graph.add_conditional_edges("intent", route_intent)

    # ===============================
    # 🔥 After Search Routing
    # ===============================

    def route_search(state):

        # Clarification flow
        if state.get("intent") == "clarify":
            return "clarify"

        # 🔥 HARD GUARD: No results → stop
        if not state.get("results"):
            return END

        if state.get("intent") == "add_to_cart":
            return "cart"

        if state.get("intent") == "remove_from_cart":
            return "remove"

        return END

    graph.add_conditional_edges("search", route_search)

    # ===============================
    # 🔥 Clarification → END
    # ===============================

    graph.add_edge("clarify", END)

    # ===============================
    # 🔥 Selection Routing
    # ===============================

    def route_selection(state):

        intent = state.get("intent")

        if intent == "add_to_cart":
            return "cart"

        if intent == "remove_from_cart":
            return "remove"

        return END

    graph.add_conditional_edges("select", route_selection)

    # ===============================
    # 🔥 Terminal Nodes
    # ===============================

    graph.add_edge("cart", END)
    graph.add_edge("remove", END)
    graph.add_edge("view_cart", END)
    graph.add_edge("order", END)

    return graph.compile()