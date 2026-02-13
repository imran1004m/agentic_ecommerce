from backend.db.session import SessionLocal
from backend.core.llm_client import get_embedding
from sqlalchemy import text

db = SessionLocal()

products = db.execute(
    text("SELECT id, name, category, brand FROM products WHERE embedding IS NULL")
).fetchall()

for product in products:
    product_id = product[0]
    text_data = f"{product[1]} {product[2]} {product[3]}"

    embedding = get_embedding(text_data)

    db.execute(
        text("UPDATE products SET embedding = :embedding WHERE id = :id"),
        {
            "embedding": embedding,
            "id": product_id
        }
    )

    print(f"Updated embedding for product ID {product_id}")

db.commit()
db.close()

print("All embeddings updated.")
