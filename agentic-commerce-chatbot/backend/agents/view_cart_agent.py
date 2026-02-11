from backend.db.session import SessionLocal
from sqlalchemy import text


def view_cart_agent(state):

    session_id = state.get("session_id", "demo-session")

    db = SessionLocal()

    query = text("""
        SELECT p.name, p.price, c.quantity
        FROM carts c
        JOIN products p ON c.product_id = p.id
        WHERE c.session_id = :session_id
    """)

    result = db.execute(query, {"session_id": session_id})
    items = result.fetchall()

    db.close()

    if not items:
        state["response"] = "Your cart is empty."
        return state

    message = "Your cart contains:\n"
    total = 0

    for name, price, quantity in items:
        subtotal = float(price) * quantity
        total += subtotal
        message += f"- {name} (x{quantity}) = ₹{subtotal}\n"

    message += f"\nTotal: ₹{total}"

    state["response"] = message
    return state
