import re
import math


def extract_pack_value(pack_size: str) -> int:
    """
    Extract numeric value from pack_size like '5kg', '1L'
    """
    match = re.search(r'(\d+)', pack_size.lower())
    if match:
        return int(match.group(1))
    return 1


def calculate_units(user_input: str, requested_quantity: int, pack_size: str) -> int:
    """
    Convert user requested quantity into number of product packs.
    """

    user_input = user_input.lower()
    pack_value = extract_pack_value(pack_size)

    # 🔹 Weight based logic (kg)
    if any(unit in user_input for unit in ["kg", "kilo"]):
        return max(1, math.ceil(requested_quantity / pack_value))

    # 🔹 Volume based logic (litre)
    if any(unit in user_input for unit in ["l", "litre", "litres", "ltr"]):
        return max(1, math.ceil(requested_quantity / pack_value))

    # 🔹 Default: packet-based logic
    return requested_quantity
