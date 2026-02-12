from backend.db.session import SessionLocal
from sqlalchemy import text
from backend.utils.unit_handler import calculate_units


def remove_agent(state):

    results = state.get("results")
    session_id = state.get("session_id", "demo-session")
    requested_quantity = state.get("quantity", 1)

    if not results:
        state["response"] = "No matching product found in cart."
        return state

    selected_product = results[0]
    product_id = selected_product[0]
    pack_size = selected_product[4]

    final_units = calculate_units(
        state["user_input"],
        requested_quantity,
        pack_size
    )

    db = SessionLocal()

    # Reduce quantity safely
    db.execute(
        text("""
            UPDATE carts
            SET quantity = GREATEST(quantity - :quantity, 0)
            WHERE session_id = :session_id
            AND product_id = :product_id
        """),
        {
            "session_id": session_id,
            "product_id": product_id,
            "quantity": final_units
        }
    )

    # Remove row if quantity becomes 0
    db.execute(
        text("""
            DELETE FROM carts
            WHERE session_id = :session_id
            AND product_id = :product_id
            AND quantity <= 0
        """),
        {
            "session_id": session_id,
            "product_id": product_id
        }
    )

    db.commit()
    db.close()

    state["response"] = f"Removed {final_units} item(s) from cart."
    return state
