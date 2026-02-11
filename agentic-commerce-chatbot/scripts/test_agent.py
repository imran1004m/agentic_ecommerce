from backend.agents.supervisor import build_graph

app = build_graph()

user_text = input("Enter your query: ")

response = app.invoke({
    "user_input": user_text,
    "intent": None,
    "results": None,
    "response": None,
    "session_id": "demo-session"
})

print("\nFinal Response:")
print(response["response"])
