from backend.db.session import SessionLocal
from backend.db.models import Cart


def cart_agent(state):
    """
    Adds first search result to cart.
    In real system, you would extract product ID properly.
    """

    if not state.get("results"):
        state["response"] = "No product found to add to cart."
        return state

    product = state["results"][0]
    product_id = product[0]  # id column

    session_id = "demo-session"  # Later we make dynamic

    db = SessionLocal()

    cart_item = Cart(
        session_id=session_id,
        product_id=product_id,
        quantity=1
    )

    db.merge(cart_item)  # avoids duplicate key error
    db.commit()
    db.close()

    state["response"] = "Product added to cart successfully."

    return state
