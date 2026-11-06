"""
Comprehensive Catalog & Campaign Seeding for KARTMART Upgrade
Seeds 13 diverse categories, 30+ photorealistic products, variants, Diwali campaigns, and coupons.
"""
from datetime import datetime, timedelta
from app import create_app
from app.extensions import db
from app.models import (
    User, Category, Product, ProductVariant,
    Coupon, Campaign, Address
)


def seed_expanded_catalog(app=None):
    if app is None:
        app = create_app()
    with app.app_context():
        print("[*] Seeding expanded KARTMART 13-category catalog and campaigns...")

        # ---------------------------------------------------------
        # 1. Seed Categories (13 Major Categories)
        # ---------------------------------------------------------
        categories_data = [
            {'slug': 'electronics', 'name': 'Electronics & Gadgets', 'icon': '⚡', 'description': 'Smartphones, noise-cancelling headphones, OLED screens & smart tech'},
            {'slug': 'mens-fashion', 'name': "Men's Fashion", 'icon': '👔', 'description': 'Premium outerwear, jackets, tailored shirts & modern urban style'},
            {'slug': 'womens-fashion', 'name': "Women's Fashion", 'icon': '👗', 'description': 'Designer coats, silk dresses, cashmere knitwear & chic apparel'},
            {'slug': 'kids-fashion', 'name': "Kids & Baby", 'icon': '🧸', 'description': 'Organic cotton apparel, warm hoodies, footwear & accessories'},
            {'slug': 'footwear', 'name': 'Shoes & Footwear', 'icon': '👟', 'description': 'Handcrafted Italian oxfords, running performance shoes & sleek sneakers'},
            {'slug': 'toys-games', 'name': 'Toys & Games', 'icon': '🎮', 'description': 'Camera drones, STEM engineering robots, board games & mechanical kits'},
            {'slug': 'home-kitchen', 'name': 'Home & Kitchen', 'icon': '☕', 'description': 'Italian espresso machines, smart air fryers, cast-iron cookware & appliances'},
            {'slug': 'furniture-decor', 'name': 'Furniture & Living', 'icon': '🪑', 'description': 'Ergonomic mesh chairs, solid oak study desks & ambient lighting'},
            {'slug': 'beauty-wellness', 'name': 'Beauty & Skincare', 'icon': '✨', 'description': 'Organic botanical serums, luxury perfumes, grooming & skincare'},
            {'slug': 'sports-fitness', 'name': 'Sports & Fitness', 'icon': '🏋️', 'description': 'Smart adjustable dumbbells, alignment yoga mats & outdoor gear'},
            {'slug': 'books-stationery', 'name': 'Books & Stationery', 'icon': '📚', 'description': 'Architecture hardcovers, brass fountain pens & leather notebooks'},
            {'slug': 'accessories-bags', 'name': 'Bags & Accessories', 'icon': '👜', 'description': 'Full-grain leather messenger bags, polarized aviators & chronograph watches'},
            {'slug': 'grocery-essentials', 'name': 'Gourmet & Essentials', 'icon': '🌿', 'description': 'Single-origin roasted coffee beans, artisanal cold-pressed oils & festive treats'}
        ]

        cat_objs = {}
        for cdata in categories_data:
            cat = Category.query.filter_by(slug=cdata['slug']).first()
            if not cat:
                cat = Category(**cdata)
                db.session.add(cat)
                db.session.flush()
            else:
                cat.name = cdata['name']
                cat.icon = cdata['icon']
                cat.description = cdata['description']
            cat_objs[cdata['slug']] = cat

        print(f"[+] Ensured {len(cat_objs)} main categories.")

        # ---------------------------------------------------------
        # 2. Seed Diwali Campaign & Festive Promotions
        # ---------------------------------------------------------
        now = datetime.utcnow()
        diwali_campaign = Campaign.query.filter_by(slug='diwali-mega-dhamaka').first()
        if not diwali_campaign:
            diwali_campaign = Campaign(
                title="Diwali Mega Dhamaka 2026",
                slug="diwali-mega-dhamaka",
                badge="🪔 DIWALI GRAND SALE",
                headline="Light Up Your Life with Up to 50% OFF Festive Steals",
                description="Celebrate the festival of lights with exclusive Diwali discounts on electronics, luxury apparel, festive sweets, and home decor.",
                banner_image="/static/img/products/diwali_banner.jpg",
                discount_text="Flat 50% Festive Discount",
                start_date=now - timedelta(days=1),
                end_date=now + timedelta(days=15),
                is_active=True
            )
            db.session.add(diwali_campaign)
            db.session.flush()
            print(" -> Created Campaign: Diwali Mega Dhamaka 2026")

        # ---------------------------------------------------------
        # 3. Seed Promotional Coupons (With Expiry Dates)
        # ---------------------------------------------------------
        coupons_data = [
            {
                'code': 'DIWALI50',
                'discount_type': 'percentage',
                'discount_percent': 50,
                'max_discount': 2500.0,
                'min_order_amount': 999.0,
                'description': 'Flat 50% discount on Diwali festive shopping (Max ₹2,500 off)',
                'start_date': now - timedelta(days=1),
                'end_date': now + timedelta(days=15),
                'is_active': True,
                'campaign_id': diwali_campaign.id
            },
            {
                'code': 'DIWALIDHOOM',
                'discount_type': 'flat',
                'discount_percent': 0,
                'max_discount': 1000.0,
                'min_order_amount': 4999.0,
                'description': 'Flat ₹1,000 instant festive cashback on orders above ₹4,999',
                'start_date': now - timedelta(days=1),
                'end_date': now + timedelta(days=15),
                'is_active': True,
                'campaign_id': diwali_campaign.id
            },
            {
                'code': 'FESTIVEGOLD',
                'discount_type': 'percentage',
                'discount_percent': 25,
                'max_discount': 1500.0,
                'min_order_amount': 1499.0,
                'description': '25% festive celebration discount on fashion, beauty & home items',
                'start_date': now - timedelta(days=1),
                'end_date': now + timedelta(days=20),
                'is_active': True,
                'campaign_id': diwali_campaign.id
            },
            {
                'code': 'KART50',
                'discount_type': 'percentage',
                'discount_percent': 50,
                'max_discount': 1500.0,
                'min_order_amount': 999.0,
                'description': 'Flat 50% off on first qualifying order above ₹999',
                'start_date': now - timedelta(days=30),
                'end_date': now + timedelta(days=60),
                'is_active': True
            },
            {
                'code': 'WELCOME20',
                'discount_type': 'percentage',
                'discount_percent': 20,
                'max_discount': 800.0,
                'min_order_amount': 499.0,
                'description': '20% instant welcome voucher for new customers',
                'start_date': now - timedelta(days=30),
                'end_date': now + timedelta(days=90),
                'is_active': True
            },
            {
                'code': 'EXPIREDTEST',
                'discount_type': 'percentage',
                'discount_percent': 30,
                'max_discount': 500.0,
                'min_order_amount': 100.0,
                'description': 'Historical expired flash sale voucher',
                'start_date': now - timedelta(days=30),
                'end_date': now - timedelta(days=2),  # Expired 2 days ago
                'is_active': True
            }
        ]

        for cp in coupons_data:
            existing_c = Coupon.query.filter_by(code=cp['code']).first()
            if not existing_c:
                c_obj = Coupon(**cp)
                db.session.add(c_obj)
            else:
                for k, v in cp.items():
                    setattr(existing_c, k, v)
        print(" -> Seeded Diwali and promotional coupons.")

        # ---------------------------------------------------------
        # 4. Seed Products with Realistic Local Images Across 13 Categories
        # ---------------------------------------------------------
        products_data = [
            # Electronics & Gadgets
            {
                'name': 'AeroSound Pro Wireless ANC Headphones',
                'category_slug': 'electronics',
                'brand': 'AeroSound',
                'price': 14999.00,
                'original_price': 24999.00,
                'stock': 28,
                'rating': 4.9,
                'reviews_count': 342,
                'badge': 'Bestseller',
                'emoji': '🎧',
                'image_url': '/static/img/products/headphones.jpg',
                'is_diwali_deal': True,
                'is_featured': True,
                'description': 'Studio-grade acoustic drivers with 42dB hybrid Active Noise Cancellation, 60-hour marathon battery life, and ultra-plush memory foam earcups.',
                'variants': [
                    {'type': 'Color', 'value': 'Matte Obsidian Black', 'adj': 0.0, 'stock': 15},
                    {'type': 'Color', 'value': 'Champagne Gold', 'adj': 500.0, 'stock': 13}
                ]
            },
            {
                'name': 'Titanium V9 Ultra 5G Flagship Smartphone',
                'category_slug': 'electronics',
                'brand': 'Titanium',
                'price': 69999.00,
                'original_price': 84999.00,
                'stock': 18,
                'rating': 4.8,
                'reviews_count': 512,
                'badge': 'Diwali Dhamaka',
                'emoji': '📱',
                'image_url': '/static/img/products/smartphone.jpg',
                'is_diwali_deal': True,
                'is_featured': True,
                'description': 'Sculpted aerospace-grade titanium frame housing a 6.8" 144Hz AMOLED dynamic display, 200MP periscope zoom lens, and lightning fast 120W charging.',
                'variants': [
                    {'type': 'Storage', 'value': '256GB / 12GB RAM', 'adj': 0.0, 'stock': 10},
                    {'type': 'Storage', 'value': '512GB / 16GB RAM', 'adj': 6000.0, 'stock': 8}
                ]
            },
            {
                'name': 'Chronos Horizon Sapphire Smartwatch',
                'category_slug': 'electronics',
                'brand': 'Chronos',
                'price': 18499.00,
                'original_price': 26999.00,
                'stock': 35,
                'rating': 4.7,
                'reviews_count': 188,
                'badge': 'Top Rated',
                'emoji': '⌚',
                'image_url': '/static/img/products/smartwatch.jpg',
                'is_diwali_deal': True,
                'is_featured': True,
                'description': 'Sapphire crystal touchscreen with ECG, SpO2 sensor, dual-frequency GPS, titanium bezel, and water-resistance up to 100 meters.',
                'variants': [
                    {'type': 'Strap', 'value': 'Fluorocarbon Sport Band', 'adj': 0.0, 'stock': 20},
                    {'type': 'Strap', 'value': 'Milanese Titanium Loop', 'adj': 1500.0, 'stock': 15}
                ]
            },
            {
                'name': 'Apex Blade 16 Ultra Slim Gaming Laptop',
                'category_slug': 'electronics',
                'brand': 'Apex',
                'price': 124999.00,
                'original_price': 149999.00,
                'stock': 12,
                'rating': 4.9,
                'reviews_count': 94,
                'badge': 'Pro Tech',
                'emoji': '💻',
                'image_url': '/static/img/products/gaming_laptop.jpg',
                'is_diwali_deal': False,
                'is_featured': True,
                'description': 'Powered by next-gen 14-core processor and dedicated RTX graphics, 240Hz QHD display, vapor chamber liquid cooling, and all-metal CNC chassis.'
            },

            # Men's Fashion
            {
                'name': 'Vanguard Full-Grain Leather Bomber Jacket',
                'category_slug': 'mens-fashion',
                'brand': 'Vanguard Heritage',
                'price': 8999.00,
                'original_price': 15999.00,
                'stock': 22,
                'rating': 4.8,
                'reviews_count': 140,
                'badge': 'Handcrafted',
                'emoji': '🧥',
                'image_url': '/static/img/products/leather_jacket.jpg',
                'is_diwali_deal': True,
                'is_featured': True,
                'description': '100% genuine supple lambskin leather jacket with antique brass YKK zippers, ribbed storm cuffs, and quilted thermal satin lining.',
                'variants': [
                    {'type': 'Size', 'value': 'M', 'adj': 0.0, 'stock': 8},
                    {'type': 'Size', 'value': 'L', 'adj': 0.0, 'stock': 8},
                    {'type': 'Size', 'value': 'XL', 'adj': 0.0, 'stock': 6}
                ]
            },
            {
                'name': 'Sartorial Classic Oxford Cotton Shirt',
                'category_slug': 'mens-fashion',
                'brand': 'Sartorial Tailors',
                'price': 2499.00,
                'original_price': 3999.00,
                'stock': 45,
                'rating': 4.6,
                'reviews_count': 88,
                'badge': 'Essential',
                'emoji': '👔',
                'image_url': '/static/img/products/oxford_shirt.jpg',
                'is_diwali_deal': False,
                'is_featured': True,
                'description': 'Breathable two-ply Egyptian cotton weave with mother-of-pearl buttons, tailored slim cut, and reinforced button-down collar.'
            },

            # Women's Fashion
            {
                'name': 'Atelier Belted Wool-Blend Trench Coat',
                'category_slug': 'womens-fashion',
                'brand': 'Atelier Paris',
                'price': 9499.00,
                'original_price': 16999.00,
                'stock': 19,
                'rating': 4.9,
                'reviews_count': 112,
                'badge': 'Autumn Edit',
                'emoji': '🧥',
                'image_url': '/static/img/products/womens_trench.jpg',
                'is_diwali_deal': True,
                'is_featured': True,
                'description': 'Water-repellent structured wool trench coat with double-breasted horn buttons, storm flaps, and a waist-cinching matching belt.',
                'variants': [
                    {'type': 'Size', 'value': 'S', 'adj': 0.0, 'stock': 6},
                    {'type': 'Size', 'value': 'M', 'adj': 0.0, 'stock': 7},
                    {'type': 'Size', 'value': 'L', 'adj': 0.0, 'stock': 6}
                ]
            },
            {
                'name': 'LuxeMove Sculpt High-Rise Activewear Set',
                'category_slug': 'womens-fashion',
                'brand': 'LuxeMove',
                'price': 3299.00,
                'original_price': 4999.00,
                'stock': 38,
                'rating': 4.7,
                'reviews_count': 76,
                'badge': 'Trending',
                'emoji': '🧘‍♀️',
                'image_url': '/static/img/products/activewear_set.jpg',
                'is_diwali_deal': False,
                'is_featured': True,
                'description': 'Four-way stretch seamless ribbed sports bra and matching high-waist compression leggings designed for yoga, running, and Pilates.'
            },

            # Kids & Baby
            {
                'name': 'LittleExplorer Organic Cotton Fleece Hoodie',
                'category_slug': 'kids-fashion',
                'brand': 'LittleExplorer',
                'price': 1499.00,
                'original_price': 2499.00,
                'stock': 40,
                'rating': 4.8,
                'reviews_count': 64,
                'badge': '100% Organic',
                'emoji': '🧸',
                'image_url': '/static/img/products/kids_hoodie.jpg',
                'is_diwali_deal': False,
                'is_featured': True,
                'description': 'GOTS-certified organic combed cotton with super-soft brushed interior fleece, kangaroo pocket, and non-toxic hypoallergenic dyes.'
            },

            # Footwear
            {
                'name': 'Modena Handcrafted Leather Brogues',
                'category_slug': 'footwear',
                'brand': 'Modena Italia',
                'price': 6499.00,
                'original_price': 11999.00,
                'stock': 24,
                'rating': 4.8,
                'reviews_count': 92,
                'badge': 'Luxury',
                'emoji': '👞',
                'image_url': '/static/img/products/leather_shoes.jpg',
                'is_diwali_deal': True,
                'is_featured': True,
                'description': 'Goodyear welted European leather shoes with intricate perforated wingtip brogue detailing and cushioned leather insoles.',
                'variants': [
                    {'type': 'UK Size', 'value': '8', 'adj': 0.0, 'stock': 8},
                    {'type': 'UK Size', 'value': '9', 'adj': 0.0, 'stock': 9},
                    {'type': 'UK Size', 'value': '10', 'adj': 0.0, 'stock': 7}
                ]
            },
            {
                'name': 'Velocity Stratus Carbon Performance Runners',
                'category_slug': 'footwear',
                'brand': 'Velocity Pro',
                'price': 7999.00,
                'original_price': 12499.00,
                'stock': 30,
                'rating': 4.9,
                'reviews_count': 210,
                'badge': 'Pro Runner',
                'emoji': '👟',
                'image_url': '/static/img/products/sneakers.jpg',
                'is_diwali_deal': True,
                'is_featured': True,
                'description': 'Engineered with a full-length carbon fiber propulsion plate, supercritical nitrogen-infused foam midsole, and ultralight knit mesh upper.'
            },

            # Toys & Games
            {
                'name': 'SkyHawk 4K HDR Foldable Camera Drone',
                'category_slug': 'toys-games',
                'brand': 'SkyHawk Dynamics',
                'price': 22999.00,
                'original_price': 34999.00,
                'stock': 16,
                'rating': 4.7,
                'reviews_count': 84,
                'badge': 'Diwali Special',
                'emoji': '🛸',
                'image_url': '/static/img/products/drone.jpg',
                'is_diwali_deal': True,
                'is_featured': True,
                'description': '3-axis stabilized brushless gimbal camera with 4K 60fps recording, 35-minute flight time, GPS return-to-home, and omnidirectional obstacle sensing.'
            },
            {
                'name': 'CyberMech STEM Programmable Robotics Kit',
                'category_slug': 'toys-games',
                'brand': 'CyberMech',
                'price': 4999.00,
                'original_price': 7999.00,
                'stock': 25,
                'rating': 4.8,
                'reviews_count': 58,
                'badge': 'STEM Certified',
                'emoji': '🤖',
                'image_url': '/static/img/products/robot_toy.jpg',
                'is_diwali_deal': False,
                'is_featured': True,
                'description': 'Build and code 5 distinct walking robot models with ultrasonic sensors, servo motors, and drag-and-drop Python/Blockly programming.'
            },

            # Home & Kitchen
            {
                'name': 'Barista Touch Espresso & Cappuccino Machine',
                'category_slug': 'home-kitchen',
                'brand': 'Barista Craft',
                'price': 34999.00,
                'original_price': 48999.00,
                'stock': 14,
                'rating': 4.9,
                'reviews_count': 125,
                'badge': 'Kitchen Luxe',
                'emoji': '☕',
                'image_url': '/static/img/products/espresso_machine.jpg',
                'is_diwali_deal': True,
                'is_featured': True,
                'description': '19-bar Italian precision pump with integrated conical burr grinder, digital PID temperature control, and micro-foam steam wand.'
            },
            {
                'name': 'AeroCrisp Smart Dual-Zone Air Fryer (8.5L)',
                'category_slug': 'home-kitchen',
                'brand': 'AeroCrisp',
                'price': 6999.00,
                'original_price': 11999.00,
                'stock': 32,
                'rating': 4.7,
                'reviews_count': 190,
                'badge': 'Diwali Deal',
                'emoji': '🍗',
                'image_url': '/static/img/products/air_fryer.jpg',
                'is_diwali_deal': True,
                'is_featured': True,
                'description': 'Dual independent cooking baskets with synchronized finish, 360-degree rapid air circulation, 8 preset cooking modes, and non-stick dishwasher safe trays.'
            },
            {
                'name': 'Heritage Enamelled Cast-Iron Dutch Oven (5.5 Qt)',
                'category_slug': 'home-kitchen',
                'brand': 'Heritage Cookware',
                'price': 5499.00,
                'original_price': 8999.00,
                'stock': 20,
                'rating': 4.8,
                'reviews_count': 110,
                'badge': 'Chef Choice',
                'emoji': '🍲',
                'image_url': '/static/img/products/cookware.jpg',
                'is_diwali_deal': False,
                'is_featured': True,
                'description': 'Heavy cast iron construction with porcelain enamel interior, solid brass lid knob, and superior heat retention for slow roasts and sourdough bread.'
            },

            # Furniture & Living
            {
                'name': 'ErgoPosture Pro Ergonomic Executive Chair',
                'category_slug': 'furniture-decor',
                'brand': 'ErgoPosture',
                'price': 18999.00,
                'original_price': 28999.00,
                'stock': 15,
                'rating': 4.9,
                'reviews_count': 145,
                'badge': 'Ergo Master',
                'emoji': '🪑',
                'image_url': '/static/img/products/office_chair.jpg',
                'is_diwali_deal': True,
                'is_featured': True,
                'description': 'Breatheable Korean high-tensile mesh with dynamic lumbar support, 4D adjustable armrests, aluminum wheelbase, and Class-4 gas lift.'
            },
            {
                'name': 'Nordic Solid Oak Minimalist Study Desk',
                'category_slug': 'furniture-decor',
                'brand': 'Nordic Studio',
                'price': 14499.00,
                'original_price': 21999.00,
                'stock': 10,
                'rating': 4.8,
                'reviews_count': 72,
                'badge': 'Solid Wood',
                'emoji': '🛋️',
                'image_url': '/static/img/products/oak_desk.jpg',
                'is_diwali_deal': False,
                'is_featured': True,
                'description': 'FSC-certified solid European oak with soft-closing dual stationery drawers, integrated cable management channel, and matte lacquer finish.'
            },
            {
                'name': 'Lumière Arc Smart Ambient LED Floor Lamp',
                'category_slug': 'furniture-decor',
                'brand': 'Lumière',
                'price': 4299.00,
                'original_price': 6999.00,
                'stock': 28,
                'rating': 4.7,
                'reviews_count': 64,
                'badge': 'Smart Home',
                'emoji': '💡',
                'image_url': '/static/img/products/floor_lamp.jpg',
                'is_diwali_deal': True,
                'is_featured': True,
                'description': 'Minimalist standing corner lamp with 16 million RGB colors, warm reading light temperature control, app control, and voice sync.'
            },

            # Beauty & Skincare
            {
                'name': 'Lumina Botanics 20% Vitamin C Radiance Serum',
                'category_slug': 'beauty-wellness',
                'brand': 'Lumina Botanics',
                'price': 1899.00,
                'original_price': 2999.00,
                'stock': 50,
                'rating': 4.9,
                'reviews_count': 310,
                'badge': 'Top Beauty',
                'emoji': '✨',
                'image_url': '/static/img/products/serum.jpg',
                'is_diwali_deal': True,
                'is_featured': True,
                'description': 'Formulated with stabilized L-Ascorbic Acid, Ferulic Acid, and Hyaluronic Acid to brighten complexion, reduce hyperpigmentation, and boost collagen.'
            },
            {
                'name': 'Oud Royal Extrait de Parfum (100ml)',
                'category_slug': 'beauty-wellness',
                'brand': 'Maison de Grasse',
                'price': 4999.00,
                'original_price': 8499.00,
                'stock': 22,
                'rating': 4.8,
                'reviews_count': 160,
                'badge': 'Diwali Gift',
                'emoji': '🌸',
                'image_url': '/static/img/products/perfume.jpg',
                'is_diwali_deal': True,
                'is_featured': True,
                'description': 'Luxury artisanal fragrance featuring warm notes of Cambodian agarwood, Damascus rose, amber, and vanilla with 14+ hours longevity.'
            },

            # Sports & Fitness
            {
                'name': 'IronFlex Smart Quick-Adjust Dumbbells (24kg Pair)',
                'category_slug': 'sports-fitness',
                'brand': 'IronFlex',
                'price': 16999.00,
                'original_price': 24999.00,
                'stock': 18,
                'rating': 4.9,
                'reviews_count': 180,
                'badge': 'Home Gym',
                'emoji': '🏋️',
                'image_url': '/static/img/products/dumbbells.jpg',
                'is_diwali_deal': True,
                'is_featured': True,
                'description': 'Replaces 15 pairs of traditional weights with a simple turn of the dial from 2.5kg to 24kg per dumbbell. Laser-cut steel plates with silent coating.'
            },
            {
                'name': 'Zenith Pro Eco-Friendly Alignment Yoga Mat (6mm)',
                'category_slug': 'sports-fitness',
                'brand': 'Zenith Yoga',
                'price': 2199.00,
                'original_price': 3499.00,
                'stock': 42,
                'rating': 4.8,
                'reviews_count': 95,
                'badge': 'Eco Choice',
                'emoji': '🧘',
                'image_url': '/static/img/products/yoga_mat.jpg',
                'is_diwali_deal': False,
                'is_featured': True,
                'description': 'Natural tree rubber base with non-slip polyurethane top surface, laser-etched alignment body lines, and complimentary carrying strap.'
            },
            {
                'name': 'AeroShield Carbon Road Cycling Helmet',
                'category_slug': 'sports-fitness',
                'brand': 'AeroShield',
                'price': 4499.00,
                'original_price': 6999.00,
                'stock': 26,
                'rating': 4.7,
                'reviews_count': 52,
                'badge': 'Safety First',
                'emoji': '🚴',
                'image_url': '/static/img/products/cycling_helmet.jpg',
                'is_diwali_deal': False,
                'is_featured': True,
                'description': 'In-mold carbon reinforcement with MIPS rotational impact protection, 24 cooling ventilation channels, and magnetic Fidlock buckle.'
            },

            # Books & Stationery
            {
                'name': 'Mastering Scalable Systems Architecture (Collector Hardcover)',
                'category_slug': 'books-stationery',
                'brand': 'TechCraft Press',
                'price': 1999.00,
                'original_price': 2999.00,
                'stock': 35,
                'rating': 4.9,
                'reviews_count': 120,
                'badge': 'Bestseller',
                'emoji': '📖',
                'image_url': '/static/img/products/leather_journal.jpg',
                'is_diwali_deal': False,
                'is_featured': True,
                'description': 'A masterwork on distributed systems, event-driven design, transactional consistency, and high-throughput data engineering.'
            },
            {
                'name': 'Imperial Brass Piston Fountain Pen & Ink Set',
                'category_slug': 'books-stationery',
                'brand': 'Imperial Heritage',
                'price': 2499.00,
                'original_price': 4299.00,
                'stock': 20,
                'rating': 4.8,
                'reviews_count': 60,
                'badge': 'Collector',
                'emoji': '✒️',
                'image_url': '/static/img/products/fountain_pen.jpg',
                'is_diwali_deal': True,
                'is_featured': True,
                'description': 'Precision-machined raw brass body with gold-plated medium nib, smooth piston filling mechanism, and bottle of archival black ink.'
            },

            # Bags & Accessories
            {
                'name': 'Artisan Full-Grain Leather Messenger Briefcase',
                'category_slug': 'accessories-bags',
                'brand': 'Artisan Craft',
                'price': 7499.00,
                'original_price': 12999.00,
                'stock': 22,
                'rating': 4.9,
                'reviews_count': 140,
                'badge': 'Pure Leather',
                'emoji': '💼',
                'image_url': '/static/img/products/leather_bag.jpg',
                'is_diwali_deal': True,
                'is_featured': True,
                'description': 'Vegetable-tanned full-grain leather that patinas beautifully with age. Dedicated padded 16" laptop sleeve, brass hardware, and detachable shoulder strap.'
            },
            {
                'name': 'AeroSight Polarized Titanium Aviator Sunglasses',
                'category_slug': 'accessories-bags',
                'brand': 'AeroSight',
                'price': 3499.00,
                'original_price': 5999.00,
                'stock': 36,
                'rating': 4.7,
                'reviews_count': 88,
                'badge': 'UV400',
                'emoji': '🕶️',
                'image_url': '/static/img/products/sunglasses.jpg',
                'is_diwali_deal': False,
                'is_featured': True,
                'description': 'Ultralight titanium frame weighing only 18 grams, 9-layer TAC polarized lenses with 100% UV400 blocking and anti-reflective inner coating.'
            },

            # Gourmet & Essentials
            {
                'name': 'Estate Reserve Single-Origin Arabica Beans (1kg)',
                'category_slug': 'grocery-essentials',
                'brand': 'Estate Reserve',
                'price': 1299.00,
                'original_price': 1899.00,
                'stock': 50,
                'rating': 4.9,
                'reviews_count': 220,
                'badge': 'Fresh Roast',
                'emoji': '☕',
                'image_url': '/static/img/products/coffee_beans.jpg',
                'is_diwali_deal': True,
                'is_featured': True,
                'description': 'Shade-grown specialty coffee beans from Chikmagalur estates, medium roasted with notes of dark chocolate, caramel, and hazelnut.'
            },
            {
                'name': 'Tuscan Gold Cold-Pressed Extra Virgin Olive Oil (1L)',
                'category_slug': 'grocery-essentials',
                'brand': 'Tuscan Gold',
                'price': 1799.00,
                'original_price': 2499.00,
                'stock': 35,
                'rating': 4.8,
                'reviews_count': 94,
                'badge': 'Imported',
                'emoji': '🫒',
                'image_url': '/static/img/products/olive_oil.jpg',
                'is_diwali_deal': False,
                'is_featured': True,
                'description': 'Single-harvest cold-pressed extra virgin olive oil with low acidity (<0.2%), packed in dark UV-protective glass bottle.'
            },
            {
                'name': 'Diwali Royal Celebration Dry Fruits & Sweets Hamper',
                'category_slug': 'grocery-essentials',
                'brand': 'Royal Feast',
                'price': 2499.00,
                'original_price': 3999.00,
                'stock': 40,
                'rating': 5.0,
                'reviews_count': 180,
                'badge': 'Diwali Special',
                'emoji': '🪔',
                'image_url': '/static/img/products/diwali_hamper.jpg',
                'is_diwali_deal': True,
                'is_featured': True,
                'description': 'Handcrafted festive gift box containing California almonds, jumbo cashews, Afghan pistachios, Medjool dates, and artisanal brass diya.'
            }
        ]

        # Seed products into DB
        for pdata in products_data:
            cat = cat_objs.get(pdata['category_slug'])
            if not cat:
                continue

            prod = Product.query.filter_by(name=pdata['name']).first()
            if not prod:
                prod = Product(
                    name=pdata['name'],
                    category_id=cat.id,
                    brand=pdata.get('brand'),
                    price=pdata['price'],
                    original_price=pdata.get('original_price'),
                    stock=pdata['stock'],
                    rating=pdata['rating'],
                    reviews_count=pdata['reviews_count'],
                    badge=pdata.get('badge'),
                    emoji=pdata.get('emoji', '📦'),
                    image_url=pdata.get('image_url'),
                    is_diwali_deal=pdata.get('is_diwali_deal', False),
                    is_featured=pdata.get('is_featured', True),
                    description=pdata['description'],
                    is_active=True
                )
                db.session.add(prod)
                db.session.flush()

                # Add variants if present
                for v in pdata.get('variants', []):
                    variant = ProductVariant(
                        product_id=prod.id,
                        variant_type=v['type'],
                        variant_value=v['value'],
                        price_adjustment=v['adj'],
                        stock=v['stock']
                    )
                    db.session.add(variant)
            else:
                # Update attributes
                prod.price = pdata['price']
                prod.original_price = pdata.get('original_price')
                prod.image_url = pdata.get('image_url')
                prod.brand = pdata.get('brand')
                prod.is_diwali_deal = pdata.get('is_diwali_deal', False)
                prod.is_featured = pdata.get('is_featured', True)
                prod.description = pdata['description']
                prod.stock = pdata['stock']

        # ---------------------------------------------------------
        # 5. Seed Customer Delivery Addresses
        # ---------------------------------------------------------
        cust = User.query.filter_by(email='customer@kartmart.local').first()
        if cust:
            if cust.addresses.count() == 0:
                addr1 = Address(
                    user_id=cust.id,
                    recipient_name="Rahul Sharma",
                    phone="9812345678",
                    street_address="Flat 402, Green Valley Apartments, Road No. 12, Banjara Hills",
                    landmark="Near City Center Mall",
                    city="Hyderabad",
                    state="Telangana",
                    pincode="500034",
                    address_type="Home",
                    is_default=True
                )
                addr2 = Address(
                    user_id=cust.id,
                    recipient_name="Rahul Sharma (Office)",
                    phone="9812345678",
                    street_address="Tower B, 7th Floor, Cyber Gateway, HITEC City",
                    landmark="Opposite Mindspace",
                    city="Hyderabad",
                    state="Telangana",
                    pincode="500081",
                    address_type="Work",
                    is_default=False
                )
                db.session.add(addr1)
                db.session.add(addr2)
                print(" -> Seeded 2 sample customer addresses.")

        db.session.commit()
        total_products = Product.query.count()
        print(f"[+] Successfully seeded {total_products} products across {len(cat_objs)} categories!")


if __name__ == '__main__':
    seed_expanded_catalog()
