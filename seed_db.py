from app import create_app
from app.extensions import db
from app.models import User, Category, Product, Coupon, Review, Order, OrderItem


def seed_database(app=None):
    if app is None:
        app = create_app('development')
    with app.app_context():
        print("[*] Seeding KARTMART database...")
        db.create_all()

        # 1. Seed Users
        if not User.query.filter_by(email='admin@kartmart.local').first():
            admin = User(
                name="Store Administrator",
                email="admin@kartmart.local",
                role="admin",
                phone="9876543210",
                address="Admin Plaza, Cyber City",
                city="Hyderabad",
                pincode="500081"
            )
            admin.set_password("Admin@123")
            db.session.add(admin)
            print(" -> Created Demo Admin: admin@kartmart.local / Admin@123")

        if not User.query.filter_by(email='customer@kartmart.local').first():
            customer = User(
                name="Rahul Sharma",
                email="customer@kartmart.local",
                role="customer",
                phone="9812345678",
                address="Flat 402, Green Valley Apartments, Banjara Hills",
                city="Hyderabad",
                pincode="500034"
            )
            customer.set_password("Customer@123")
            db.session.add(customer)
            print(" -> Created Demo Customer: customer@kartmart.local / Customer@123")

        db.session.commit()

        # 2. Seed Categories
        categories_data = [
            {'name': 'Electronics', 'slug': 'electronics', 'icon': 'EL', 'description': 'Mobiles, laptops, earbuds, smart gadgets'},
            {'name': 'Fashion & Clothing', 'slug': 'clothing', 'icon': 'FA', 'description': 'Trendy apparel, jackets, streetwear'},
            {'name': 'Accessories', 'slug': 'accessories', 'icon': 'AC', 'description': 'Smartwatches, luxury sunglasses, leather bags'},
            {'name': 'Home & Kitchen', 'slug': 'home', 'icon': 'HM', 'description': 'Coffee makers, smart lamps, modern decor'},
            {'name': 'Books & Tech', 'slug': 'books', 'icon': 'BK', 'description': 'Software architecture, business & tech bestsellers'}
        ]

        cat_map = {}
        for cdata in categories_data:
            cat = Category.query.filter_by(slug=cdata['slug']).first()
            if not cat:
                cat = Category(**cdata)
                db.session.add(cat)
                db.session.flush()
            cat_map[cdata['slug']] = cat

        db.session.commit()

        # 3. Seed Coupons / Offers
        coupons_data = [
            {'code': 'KART50', 'discount_percent': 50, 'max_discount': 1500.0, 'min_order_amount': 999.0, 'description': 'Flat 50% Mega Discount (Up to Rs.1500 on Rs.999+)'},
            {'code': 'WELCOME20', 'discount_percent': 20, 'max_discount': 500.0, 'min_order_amount': 499.0, 'description': '20% OFF Welcome Bonus for new shoppers'},
            {'code': 'FREESHIP', 'discount_percent': 10, 'max_discount': 250.0, 'min_order_amount': 299.0, 'description': '10% Extra Discount on your order'}
        ]

        for cp in coupons_data:
            if not Coupon.query.filter_by(code=cp['code']).first():
                db.session.add(Coupon(**cp))
        db.session.commit()
        print(" -> Seeded Coupons: KART50, WELCOME20, FREESHIP")

        # 4. Seed Products
        products_data = [
            # Electronics
            {
                'category_slug': 'electronics',
                'name': 'MacBook Pro M3 16-inch',
                'description': '36GB Unified Memory, 512GB SSD, Liquid Retina XDR display with ProMotion technology.',
                'price': 169999.0,
                'original_price': 199999.0,
                'stock': 12,
                'rating': 4.9,
                'reviews_count': 128,
                'badge': 'Deal of the Day',
                'emoji': 'LAPTOP'
            },
            {
                'category_slug': 'electronics',
                'name': 'Sony WH-1000XM5 Wireless Headphones',
                'description': 'Industry-leading noise cancellation, 30-hour battery life, speak-to-chat and ultra-clear hands-free calling.',
                'price': 24990.0,
                'original_price': 34990.0,
                'stock': 25,
                'rating': 4.8,
                'reviews_count': 342,
                'badge': 'Best Seller',
                'emoji': 'HEADPHONE'
            },
            {
                'category_slug': 'electronics',
                'name': 'iPhone 16 Pro Max 256GB',
                'description': 'Titanium design with larger 6.9-inch display, Camera Control, 4K 120 fps Dolby Vision, and A18 Pro chip.',
                'price': 134900.0,
                'original_price': 144900.0,
                'stock': 18,
                'rating': 4.9,
                'reviews_count': 512,
                'badge': 'Top Trending',
                'emoji': 'PHONE'
            },
            {
                'category_slug': 'electronics',
                'name': 'Noise Pulse 4 Smart Watch with AMOLED',
                'description': '1.85-inch AMOLED Display, Bluetooth calling, 7-day battery, 100+ sports modes, 24x7 heart rate tracker.',
                'price': 2499.0,
                'original_price': 5999.0,
                'stock': 40,
                'rating': 4.4,
                'reviews_count': 89,
                'badge': 'Hot Deal 58% Off',
                'emoji': 'WATCH'
            },
            # Fashion
            {
                'category_slug': 'clothing',
                'name': 'Italian Wool Blend Overcoat',
                'description': 'Premium structured tailoring with storm collar and insulated thermal lining for elevated style.',
                'price': 6499.0,
                'original_price': 12999.0,
                'stock': 20,
                'rating': 4.7,
                'reviews_count': 64,
                'badge': '50% Off Special',
                'emoji': 'COAT'
            },
            {
                'category_slug': 'clothing',
                'name': 'Vintage Heavyweight Cotton Hoodie',
                'description': '400 GSM French terry cotton, custom drop-shoulder fit with double-layered hood.',
                'price': 2199.0,
                'original_price': 3999.0,
                'stock': 35,
                'rating': 4.6,
                'reviews_count': 112,
                'badge': 'Amazon Choice',
                'emoji': 'HOODIE'
            },
            {
                'category_slug': 'clothing',
                'name': 'Urban Slim Tapered Denim Jeans',
                'description': 'Stretch selvedge denim in deep indigo wash. Engineered for flexibility and all-day comfort.',
                'price': 1899.0,
                'original_price': 3499.0,
                'stock': 28,
                'rating': 4.5,
                'reviews_count': 78,
                'badge': 'Popular',
                'emoji': 'JEANS'
            },
            # Accessories
            {
                'category_slug': 'accessories',
                'name': 'Seiko Automatic Prospex Diver Watch',
                'description': '200m water resistance, automatic 4R36 movement, Lumibrite hands, sapphire crystal glass.',
                'price': 32500.0,
                'original_price': 39000.0,
                'stock': 8,
                'rating': 4.9,
                'reviews_count': 45,
                'badge': 'Limited Edition',
                'emoji': 'DIVER'
            },
            {
                'category_slug': 'accessories',
                'name': 'Full Grain Leather Messenger Bag',
                'description': 'Handcrafted vintage leather bag with 15.6-inch padded laptop compartment and brass hardware.',
                'price': 4299.0,
                'original_price': 7999.0,
                'stock': 15,
                'rating': 4.7,
                'reviews_count': 93,
                'badge': 'Best Seller',
                'emoji': 'BAG'
            },
            {
                'category_slug': 'accessories',
                'name': 'Aviator Polarized Titanium Sunglasses',
                'description': 'UV400 protection, scratch-resistant polarized lenses with ultra-lightweight titanium frame.',
                'price': 1999.0,
                'original_price': 4499.0,
                'stock': 30,
                'rating': 4.6,
                'reviews_count': 156,
                'badge': 'Summer Sale',
                'emoji': 'GLASSES'
            },
            # Home & Kitchen
            {
                'category_slug': 'home',
                'name': 'Espresso Barista Coffee Machine 15-Bar',
                'description': 'High-pressure Italian pump with steam milk frother wand for cappuccinos, lattes, and rich espresso.',
                'price': 8999.0,
                'original_price': 14999.0,
                'stock': 14,
                'rating': 4.7,
                'reviews_count': 210,
                'badge': 'Top Rated',
                'emoji': 'COFFEE'
            },
            {
                'category_slug': 'home',
                'name': 'Minimalist Nordic Arc Floor Lamp',
                'description': 'Dimmable warm ambient LED lighting with brushed brass finish and heavy marble base.',
                'price': 3499.0,
                'original_price': 6999.0,
                'stock': 16,
                'rating': 4.8,
                'reviews_count': 84,
                'badge': 'Home Trend',
                'emoji': 'LAMP'
            },
            # Books
            {
                'category_slug': 'books',
                'name': 'Designing Data-Intensive Applications',
                'description': 'The definitive guide to distributed systems architecture, reliability, scalability, and data storage by Martin Kleppmann.',
                'price': 1499.0,
                'original_price': 2299.0,
                'stock': 40,
                'rating': 5.0,
                'reviews_count': 840,
                'badge': '#1 Best Seller in Tech',
                'emoji': 'BOOK'
            },
            {
                'category_slug': 'books',
                'name': 'Clean Code: Agile Software Craftsmanship',
                'description': 'Robert C. Martin’s handbook of agile software engineering, refactoring, and quality software.',
                'price': 999.0,
                'original_price': 1899.0,
                'stock': 30,
                'rating': 4.8,
                'reviews_count': 620,
                'badge': 'Classic',
                'emoji': 'BOOK'
            }
        ]

        for pdata in products_data:
            cslug = pdata.pop('category_slug')
            cat = cat_map[cslug]
            existing = Product.query.filter_by(name=pdata['name']).first()
            if not existing:
                prod = Product(category_id=cat.id, **pdata)
                db.session.add(prod)
                db.session.flush()

                # Add sample review
                rev = Review(
                    product_id=prod.id,
                    user_name="Karthik V.",
                    rating=5,
                    title="Amazing purchase on KARTMART!",
                    comment=f"Received the {prod.name} in 2 days. Perfect condition and quality as described!"
                )
                db.session.add(rev)

        db.session.commit()
        print(f" -> Successfully seeded {len(products_data)} products across 5 categories with reviews.")
        print("[+] Database seeding complete!")


if __name__ == '__main__':
    seed_database()
