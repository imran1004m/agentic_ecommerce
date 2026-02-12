from typing import TypedDict, Optional, List, Any


class AgentState(TypedDict, total=False):

    user_input: str
    intent: str
    results: List[Any]
    response: str

    quantity: int
    quantity_mode: str

    requested_unit: Optional[str]   # 🔥 ADD THIS LINE

    clarification_options: List[Any]
    original_intent: str

    session_id: str
