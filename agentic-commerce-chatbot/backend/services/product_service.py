from sqlalchemy import text
from backend.core.llm_client import get_embedding
import math
import json


# =====================================================
# Cosine Similarity
# =====================================================

def cosine_similarity(vec1, vec2):
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    return dot / (norm1 * norm2) if norm1 and norm2 else 0


# =====================================================
# Hybrid Search (Production Safe)
# =====================================================

def hybrid_search(db, query: str, available_only: bool = True, top_k: int = 5):

    query_lower = query.lower().strip()

    # =====================================================
    # 0️⃣ HANDLE "SHOW ALL PRODUCTS"
    # =====================================================

    if any(phrase in query_lower for phrase in [
        "show products",
        "show all products",
        "list products",
        "available products",
        "show items"
    ]):

        if available_only:
            result = db.execute(
                text("""
                    SELECT id, name, category, brand, pack_size, price, availability, embedding
                    FROM products
                    WHERE availability = true
                """)
            )
        else:
            result = db.execute(
                text("""
                    SELECT id, name, category, brand, pack_size, price, availability, embedding
                    FROM products
                """)
            )

        rows = result.fetchall()
        return [(*row, 1.0) for row in rows]

    # =====================================================
    # 1️⃣ CATEGORY SEARCH
    # =====================================================

    category_result = db.execute(
        text("SELECT DISTINCT category FROM products")
    )

    categories = [row[0].lower() for row in category_result.fetchall()]

    for category in categories:
        if category in query_lower:

            if available_only:
                result = db.execute(
                    text("""
                        SELECT id, name, category, brand, pack_size, price, availability, embedding
                        FROM products
                        WHERE LOWER(category) = :category
                        AND availability = true
                    """),
                    {"category": category}
                )
            else:
                result = db.execute(
                    text("""
                        SELECT id, name, category, brand, pack_size, price, availability, embedding
                        FROM products
                        WHERE LOWER(category) = :category
                    """),
                    {"category": category}
                )

            rows = result.fetchall()
            return [(*row, 1.0) for row in rows]

    # =====================================================
    # 2️⃣ EMBEDDING SEARCH (FALLBACK)
    # =====================================================

    query_embedding = get_embedding(query)

    if available_only:
        result = db.execute(
            text("""
                SELECT id, name, category, brand, pack_size, price, availability, embedding
                FROM products
                WHERE availability = true
            """)
        )
    else:
        result = db.execute(
            text("""
                SELECT id, name, category, brand, pack_size, price, availability, embedding
                FROM products
            """)
        )

    rows = result.fetchall()

    scored_results = []

    for row in rows:

        product_embedding = row[7]

        if product_embedding is None:
            continue

        if isinstance(product_embedding, str):
            product_embedding = json.loads(product_embedding)

        similarity = cosine_similarity(query_embedding, product_embedding)

        scored_results.append((*row, similarity))

    if not scored_results:
        return []

    scored_results.sort(key=lambda x: x[-1], reverse=True)

    # =====================================================
    # 🔥 STRICT RELEVANCE GUARD
    # =====================================================

    SIMILARITY_THRESHOLD = 0.80

    best_match = scored_results[0]

    if best_match[-1] < SIMILARITY_THRESHOLD:
        return []

    # Word overlap validation
    query_words = set(query_lower.split())
    product_text = f"{best_match[1]} {best_match[2]} {best_match[3]}".lower()
    product_words = set(product_text.split())

    if not query_words.intersection(product_words):
        return []

    return scored_results[:top_k]