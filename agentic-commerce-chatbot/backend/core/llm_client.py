import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DEFAULT_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"


# =====================================================
# 🔹 Chat Completion
# =====================================================

def chat_completion(system_prompt: str, user_input: str, temperature: float = 0):
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=temperature
    )

    return response.choices[0].message.content.strip()


# =====================================================
# 🔹 Embedding Generator (NEW — REQUIRED)
# =====================================================

def get_embedding(text: str):
    """
    Generate vector embedding for product text or search query.
    """

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.data[0].embedding
