from backend.db.session import SessionLocal
from sqlalchemy import text
import re
import math


def extract_pack_size(pack_size_str):
    """
    Extract numeric value and normalized unit from product pack size.
    Example:
    '5kg' -> (5, 'kg')
    '1L'  -> (1, 'l')
    """

    match = re.match(r'(\d+)\s*(kg|g|l|ltr|litre|litres)?', pack_size_str.lower())

    if match:
        value = int(match.group(1))
        unit = match.group(2)

        if unit:
            unit = unit.lower()

            if unit in ["ltr", "litre", "litres"]:
                unit = "l"

        return value, unit

    return 1, None


def cart_agent(state):

    results = state.get("results")
    session_id = state.get("session_id", "demo-session")
    requested_qty = state.get("quantity", 1)
    quantity_mode = state.get("quantity_mode", "increment")
    requested_unit = state.get("requested_unit")

    if not results:
        state["response"] = "No product found to add to cart."
        return state

    selected_product = results[0]

    product_id = selected_product[0]
    pack_size = selected_product[4]  # e.g. 2kg, 1L

    pack_value, pack_unit = extract_pack_size(pack_size)

    # 🔥 DEBUG PRINTS (ADD HERE)
    # print("Requested quantity:", requested_qty)
    # print("Requested unit:", requested_unit)
    # print("Pack size:", pack_size)
    # print("Pack value:", pack_value)
    # print("Pack unit:", pack_unit)

    final_qty = requested_qty

    # =====================================================
    # 🔥 CORRECT UNIT-AWARE CONVERSION
    # =====================================================
    if requested_unit and pack_unit and requested_unit == pack_unit:

        if pack_value > 0:
            # Example:
            # 10kg requested
            # 2kg pack
            # → ceil(10 / 2) = 5 packs
            final_qty = math.ceil(requested_qty / pack_value)

    print("Final quantity (packs):", final_qty)

    # =====================================================
    # DB OPERATION
    # =====================================================
    db = SessionLocal()

    if quantity_mode == "set_total":

        db.execute(
            text("""
                INSERT INTO carts (session_id, product_id, quantity)
                VALUES (:session_id, :product_id, :quantity)
                ON CONFLICT (session_id, product_id)
                DO UPDATE SET quantity = :quantity
            """),
            {
                "session_id": session_id,
                "product_id": product_id,
                "quantity": final_qty
            }
        )

        state["response"] = f"Product quantity set to {final_qty}."

    else:  # increment mode

        db.execute(
            text("""
                INSERT INTO carts (session_id, product_id, quantity)
                VALUES (:session_id, :product_id, :quantity)
                ON CONFLICT (session_id, product_id)
                DO UPDATE SET quantity = carts.quantity + :quantity
            """),
            {
                "session_id": session_id,
                "product_id": product_id,
                "quantity": final_qty
            }
        )

        state["response"] = f"Product added to cart successfully (x{final_qty})."

    db.commit()
    db.close()

    return state
