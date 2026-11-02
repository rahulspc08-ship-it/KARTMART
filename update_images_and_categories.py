import os
import shutil
from app import create_app
from app.extensions import db
from app.models import Category, Product

# Ensure category images directory exists
cat_dir = os.path.join('app', 'static', 'img', 'categories')
prod_dir = os.path.join('app', 'static', 'img', 'products')
os.makedirs(cat_dir, exist_ok=True)

# Copy genuine photograph assets for category covers
category_asset_map = {
    'electronics': 'smartphone.jpg',
    'clothing': 'oxford_shirt.jpg',
    'accessories': 'leather_bag.jpg',
    'home': 'cookware.jpg',
    'books': 'leather_journal.jpg',
    'mens-fashion': 'oxford_shirt.jpg',
    'womens-fashion': 'womens_trench.jpg',
    'kids-fashion': 'kids_hoodie.jpg',
    'footwear': 'sneakers.jpg',
    'toys-games': 'drone.jpg',
    'home-kitchen': 'espresso_machine.jpg',
    'furniture-decor': 'office_chair.jpg',
    'beauty-wellness': 'serum.jpg',
    'sports-fitness': 'dumbbells.jpg',
    'books-stationery': 'leather_journal.jpg',
    'accessories-bags': 'leather_bag.jpg',
    'grocery-essentials': 'coffee_beans.jpg'
}

for slug, src_name in category_asset_map.items():
    src_path = os.path.join(prod_dir, src_name)
    dst_name = f"cat_{slug}.jpg"
    dst_path = os.path.join(cat_dir, dst_name)
    if os.path.exists(src_path):
        shutil.copyfile(src_path, dst_path)
        print(f"Copied {src_name} -> {dst_name}")

# Also copy a fallback for categories
shutil.copyfile(os.path.join(prod_dir, 'headphones.jpg'), os.path.join(cat_dir, 'cat_fallback.jpg'))

# Now update the database
app = create_app('development')
with app.app_context():
    # 1. Update Category image_urls
    categories = Category.query.all()
    for cat in categories:
        img_filename = f"cat_{cat.slug}.jpg"
        if os.path.exists(os.path.join(cat_dir, img_filename)):
            cat.image_url = f"/static/img/categories/{img_filename}"
        else:
            cat.image_url = "/static/img/categories/cat_fallback.jpg"
        print(f"Category '{cat.name}' -> {cat.image_url}")

    # 2. Update Products 1-14 missing image_urls
    product_img_map = {
        1: '/static/img/products/gaming_laptop.jpg',
        2: '/static/img/products/headphones.jpg',
        3: '/static/img/products/smartphone.jpg',
        4: '/static/img/products/smartwatch.jpg',
        5: '/static/img/products/womens_trench.jpg',
        6: '/static/img/products/kids_hoodie.jpg',
        7: '/static/img/products/activewear_set.jpg',
        8: '/static/img/products/smartwatch.jpg',
        9: '/static/img/products/leather_bag.jpg',
        10: '/static/img/products/sunglasses.jpg',
        11: '/static/img/products/espresso_machine.jpg',
        12: '/static/img/products/floor_lamp.jpg',
        13: '/static/img/products/leather_journal.jpg',
        14: '/static/img/products/fountain_pen.jpg'
    }

    for pid, img_path in product_img_map.items():
        prod = Product.query.get(pid)
        if prod:
            prod.image_url = img_path
            print(f"Product {prod.id} '{prod.name}' -> {prod.image_url}")

    # Mark some products as Most Loved / Featured if needed
    db.session.commit()
    print("Database updated successfully!")
