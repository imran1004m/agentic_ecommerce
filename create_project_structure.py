import os

PROJECT_NAME = "agentic-commerce-chatbot"

folders = [
    "frontend/components",
    "frontend/utils",
    "backend/api/routes",
    "backend/core",
    "backend/agents",
    "backend/orchestration",
    "backend/services",
    "backend/tools",
    "backend/db",
    "backend/schemas",
    "backend/tests",
    "scripts",
]

files = [
    "README.md",
    "requirements.txt",
    ".env",
    ".gitignore",

    "frontend/app.py",
    "frontend/components/chat_ui.py",
    "frontend/components/image_upload.py",
    "frontend/components/order_summary.py",
    "frontend/utils/api_client.py",

    "backend/main.py",
    "backend/api/deps.py",
    "backend/api/routes/chat.py",
    "backend/api/routes/cart.py",
    "backend/api/routes/order.py",
    "backend/api/routes/health.py",

    "backend/core/config.py",
    "backend/core/llm_client.py",
    "backend/core/embeddings.py",
    "backend/core/logger.py",

    "backend/agents/supervisor.py",
    "backend/agents/intent_agent.py",
    "backend/agents/list_parser_agent.py",
    "backend/agents/ocr_agent.py",
    "backend/agents/product_search_agent.py",
    "backend/agents/clarification_agent.py",
    "backend/agents/cart_agent.py",
    "backend/agents/order_agent.py",

    "backend/orchestration/graph.py",

    "backend/services/product_service.py",
    "backend/services/cart_service.py",
    "backend/services/order_service.py",
    "backend/services/ocr_service.py",

    "backend/tools/product_tools.py",
    "backend/tools/cart_tools.py",
    "backend/tools/order_tools.py",

    "backend/db/session.py",
    "backend/db/models.py",
    "backend/db/crud.py",
    "backend/db/schema.sql",

    "backend/schemas/chat.py",
    "backend/schemas/product.py",
    "backend/schemas/cart.py",
    "backend/schemas/order.py",

    "backend/tests/test_agents.py",
    "backend/tests/test_tools.py",
    "backend/tests/test_api.py",

    "scripts/load_products.py",
    "scripts/generate_embeddings.py",
    "scripts/seed_data.py",
]

def create_structure():
    os.makedirs(PROJECT_NAME, exist_ok=True)

    for folder in folders:
        os.makedirs(os.path.join(PROJECT_NAME, folder), exist_ok=True)

    for file in files:
        file_path = os.path.join(PROJECT_NAME, file)
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write("")

    print(f"✅ Project structure '{PROJECT_NAME}' created successfully!")

if __name__ == "__main__":
    create_structure()
