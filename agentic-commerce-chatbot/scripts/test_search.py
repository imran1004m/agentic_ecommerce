from backend.db.session import SessionLocal
from backend.services.product_service import hybrid_search

db = SessionLocal()

results = hybrid_search(
    db,
    query="1 litre milk",
    max_price=100,
    available_only=True
)

print("Number of results:", len(results))

for r in results:
    print(r)

db.close()
