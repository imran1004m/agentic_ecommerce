from sqlalchemy import text
from backend.db.session import SessionLocal
from backend.core.llm_client import get_embedding


def build_product_text(row):
    """
    Build rich semantic text for embedding.
    """
    return f"{row['brand']} {row['name']} {row['pack_size']} in category {row['category']}"


def backfill_embeddings():

    db = SessionLocal()

    # 🔥 1️⃣ Fetch products without embedding
    result = db.execute(
        text("""
            SELECT id, name, brand, category, pack_size
            FROM products
            WHERE embedding IS NULL
        """)
    )

    rows = result.mappings().all()

    if not rows:
        print("✅ All products already have embeddings.")
        db.close()
        return

    print(f"🔄 Generating embeddings for {len(rows)} products...\n")

    for row in rows:
        product_text = build_product_text(row)

        embedding = get_embedding(product_text)

        db.execute(
            text("""
                UPDATE products
                SET embedding = :embedding
                WHERE id = :id
            """),
            {
                "embedding": embedding,
                "id": row["id"]
            }
        )

        print(f"✔ Embedded: {row['brand']} {row['name']}")

    db.commit()
    db.close()

    print("\n🎉 Backfill completed successfully!")


if __name__ == "__main__":
    backfill_embeddings()
