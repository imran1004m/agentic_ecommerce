from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.core.embeddings import generate_embedding


def hybrid_search(
    db: Session,
    query: str,
    max_price: float = None,
    category: str = None,
    available_only: bool = True,
    top_k: int = 5
):
    """
    Hybrid search:
    - Structured filters (price, category, availability)
    - Vector similarity ranking
    - Returns similarity distance for threshold filtering
    """

    query_embedding = generate_embedding(query)

    sql = """
        SELECT *,
               embedding <-> (:embedding)::vector AS distance
        FROM products
        WHERE 1=1
    """

    params = {
        "embedding": query_embedding,
        "limit": top_k
    }

    # Structured filters
    if available_only:
        sql += " AND availability = true"

    if max_price is not None:
        sql += " AND price <= :max_price"
        params["max_price"] = max_price

    if category is not None:
        sql += " AND category = :category"
        params["category"] = category

    # Order by similarity (smaller distance = better match)
    sql += """
        ORDER BY embedding <-> (:embedding)::vector
        LIMIT :limit
    """

    result = db.execute(text(sql), params)

    return result.fetchall()
