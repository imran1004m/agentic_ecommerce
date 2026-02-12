from typing import TypedDict, Optional, List, Any


class AgentState(TypedDict):
    user_input: str
    intent: Optional[str]
    original_intent: Optional[str]
    results: Optional[List[Any]]
    response: Optional[str]
    session_id: Optional[str]
    clarification_options: Optional[List[Any]]
    quantity: Optional[int]
    quantity_mode: Optional[str]  # 🔥 NEW ("increment" or "set_total")
