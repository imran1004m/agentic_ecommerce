from backend.db.session import SessionLocal
from backend.db.models import Product
from backend.core.embeddings import generate_embedding

sample_products = [
    {
        "name": "Amul Toned Milk 1L",
        "category": "milk",
        "brand": "Amul",
        "pack_size": "1L",
        "price": 78
    },
    {
        "name": "India Gate Basmati Rice 2kg",
        "category": "rice",
        "brand": "India Gate",
        "pack_size": "2kg",
        "price": 210
    },
    {
        "name": "Aashirvaad Atta 5kg",
        "category": "flour",
        "brand": "Aashirvaad",
        "pack_size": "5kg",
        "price": 320
    }
]

db = SessionLocal()

print("Connected to DB")

for item in sample_products:
    print(f"Processing: {item['name']}")

    embedding = generate_embedding(item["name"])

    product = Product(
        name=item["name"],
        category=item["category"],
        brand=item["brand"],
        pack_size=item["pack_size"],
        price=item["price"],
        embedding=embedding
    )

    db.add(product)

db.commit()
print("Committed to DB")

db.close()
print("Done.")
