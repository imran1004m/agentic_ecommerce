from backend.db.session import SessionLocal
from backend.db.models import Order
from sqlalchemy import text


def order_agent(state):

    session_id = state.get("session_id", "demo-session")

    db = SessionLocal()

    # Calculate total
    total_query = text("""
        SELECT SUM(p.price * c.quantity)
        FROM carts c
        JOIN products p ON c.product_id = p.id
        WHERE c.session_id = :session_id
    """)

    result = db.execute(total_query, {"session_id": session_id})
    total = result.scalar()

    if not total:
        state["response"] = "Your cart is empty. Cannot place order."
        db.close()
        return state

    # Create order
    order = Order(
        session_id=session_id,
        status="confirmed",
        total=total
    )

    db.add(order)

    # Clear cart after order
    clear_query = text("""
        DELETE FROM carts
        WHERE session_id = :session_id
    """)
    db.execute(clear_query, {"session_id": session_id})

    db.commit()
    db.close()

    state["response"] = f"Order placed successfully! Total: ₹{total}"

    return state
