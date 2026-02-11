from langgraph.graph import StateGraph, END
from backend.agents.state import AgentState

from backend.agents.intent_agent import detect_intent
from backend.agents.product_search_agent import product_search_agent
from backend.agents.cart_agent import cart_agent
from backend.agents.clarification_agent import clarification_agent
from backend.agents.order_agent import order_agent
from backend.agents.view_cart_agent import view_cart_agent


def build_graph():

    workflow = StateGraph(AgentState)

    # -------------------------
    # Add Nodes
    # -------------------------

    workflow.add_node("intent", detect_intent)
    workflow.add_node("search", product_search_agent)
    workflow.add_node("cart", cart_agent)
    workflow.add_node("clarify", clarification_agent)
    workflow.add_node("order", order_agent)
    workflow.add_node("view_cart", view_cart_agent)

    workflow.set_entry_point("intent")

    # -------------------------
    # Routing From Intent
    # -------------------------

    def route_from_intent(state):

        intent = state.get("intent")

        if intent == "search_product":
            return "search"

        if intent == "add_to_cart":
            return "search"  # search first, then cart

        if intent == "place_order":
            return "order"

        if intent == "view_cart":
            return "view_cart"

        return "search"

    workflow.add_conditional_edges("intent", route_from_intent)

    # -------------------------
    # Routing After Search
    # -------------------------

    def route_after_search(state):

        if state.get("intent") == "clarify":
            return "clarify"

        if state.get("intent") == "add_to_cart":
            return "cart"

        # Normal search ends here
        return END

    workflow.add_conditional_edges("search", route_after_search)

    # -------------------------
    # Finish Points
    # -------------------------

    workflow.add_edge("clarify", END)
    workflow.add_edge("cart", END)
    workflow.add_edge("order", END)
    workflow.add_edge("view_cart", END)

    return workflow.compile()
