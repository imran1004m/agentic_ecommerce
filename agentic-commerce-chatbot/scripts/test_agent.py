from backend.agents.supervisor import build_graph

app = build_graph()

print("Agentic Commerce Chatbot")
print("Type 'exit' to quit.\n")

# 🔥 Persistent state object
state = {
    "session_id": "demo-session",
    "results": None,
    "response": None,
    "intent": None,
    "original_intent": None,
    "clarification_options": None,
    "quantity": 1,
    "quantity_mode": "increment"
}

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    # 🔥 Only update user_input — preserve everything else
    state["user_input"] = user_input

    state = app.invoke(state)

    print("\nBot:")
    print(state.get("response"))
    print("-" * 40)
