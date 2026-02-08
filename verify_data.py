from db_queries import get_all_products, get_categories

products = get_all_products()
categories = get_categories()

print(f"Total Products: {len(products)}")
print(f"Total Categories: {len(categories)}")

cat_counts = {}
for p in products:
    cid = p['category_id']
    cat_counts[cid] = cat_counts.get(cid, 0) + 1

print("\nProduct Counts per Category:")
for cid, count in cat_counts.items():
    cname = next((c['name'] for c in categories if c['category_id'] == cid), "Unknown")
    print(f"Category {cid} ({cname}): {count}")
