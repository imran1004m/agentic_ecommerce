from typing import TypedDict, Optional, List, Any


class AgentState(TypedDict):
    """
    Shared state passed between all agents in LangGraph.
    """

    user_input: str
    intent: Optional[str]
    results: Optional[List[Any]]
    response: Optional[str]
    session_id: Optional[str]
