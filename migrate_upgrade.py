"""
Safe non-destructive migration script for KARTMART upgrade.
Creates newly introduced tables and safely adds columns to existing tables.
Compatible with SQLite and MySQL.
"""
from app import create_app
from app.extensions import db
from sqlalchemy import inspect, text


def run_migration():
    app = create_app()
    with app.app_context():
        print("[*] Starting non-destructive database upgrade migration...")
        
        # 1. Create all new tables (addresses, wishlist_items, support_tickets, campaigns, product_variants)
        db.create_all()
        print("[+] Ensured all tables exist via db.create_all().")

        inspector = inspect(db.engine)
        
        # Helper to check if column exists
        def get_existing_columns(table_name):
            try:
                return [c['name'] for c in inspector.get_columns(table_name)]
            except Exception:
                return []

        # 2. Add columns to 'coupons'
        coupon_cols = get_existing_columns('coupons')
        if 'campaign_id' not in coupon_cols:
            db.session.execute(text("ALTER TABLE coupons ADD COLUMN campaign_id INTEGER"))
            print(" -> Added campaign_id to coupons")
        if 'discount_type' not in coupon_cols:
            db.session.execute(text("ALTER TABLE coupons ADD COLUMN discount_type VARCHAR(20) DEFAULT 'percentage'"))
            print(" -> Added discount_type to coupons")
        if 'start_date' not in coupon_cols:
            db.session.execute(text("ALTER TABLE coupons ADD COLUMN start_date DATETIME"))
            print(" -> Added start_date to coupons")
        if 'end_date' not in coupon_cols:
            db.session.execute(text("ALTER TABLE coupons ADD COLUMN end_date DATETIME"))
            print(" -> Added end_date to coupons")
        if 'times_used' not in coupon_cols:
            db.session.execute(text("ALTER TABLE coupons ADD COLUMN times_used INTEGER DEFAULT 0"))
            print(" -> Added times_used to coupons")

        # 3. Add columns to 'orders'
        order_cols = get_existing_columns('orders')
        if 'cancellation_reason' not in order_cols:
            db.session.execute(text("ALTER TABLE orders ADD COLUMN cancellation_reason VARCHAR(150)"))
            print(" -> Added cancellation_reason to orders")
        if 'cancellation_comments' not in order_cols:
            db.session.execute(text("ALTER TABLE orders ADD COLUMN cancellation_comments TEXT"))
            print(" -> Added cancellation_comments to orders")
        if 'cancelled_at' not in order_cols:
            db.session.execute(text("ALTER TABLE orders ADD COLUMN cancelled_at DATETIME"))
            print(" -> Added cancelled_at to orders")
        if 'refund_status' not in order_cols:
            db.session.execute(text("ALTER TABLE orders ADD COLUMN refund_status VARCHAR(50) DEFAULT 'Not Applicable'"))
            print(" -> Added refund_status to orders")
        if 'refund_amount' not in order_cols:
            db.session.execute(text("ALTER TABLE orders ADD COLUMN refund_amount FLOAT DEFAULT 0.0"))
            print(" -> Added refund_amount to orders")
        if 'refund_ref' not in order_cols:
            db.session.execute(text("ALTER TABLE orders ADD COLUMN refund_ref VARCHAR(50)"))
            print(" -> Added refund_ref to orders")

        # 4. Add columns to 'order_items'
        item_cols = get_existing_columns('order_items')
        if 'product_image' not in item_cols:
            db.session.execute(text("ALTER TABLE order_items ADD COLUMN product_image VARCHAR(500)"))
            print(" -> Added product_image to order_items")
        if 'product_variant' not in item_cols:
            db.session.execute(text("ALTER TABLE order_items ADD COLUMN product_variant VARCHAR(100)"))
            print(" -> Added product_variant to order_items")

        # 5. Add columns to 'categories'
        cat_cols = get_existing_columns('categories')
        if 'parent_id' not in cat_cols:
            db.session.execute(text("ALTER TABLE categories ADD COLUMN parent_id INTEGER"))
            print(" -> Added parent_id to categories")
        if 'image_url' not in cat_cols:
            db.session.execute(text("ALTER TABLE categories ADD COLUMN image_url VARCHAR(500)"))
            print(" -> Added image_url to categories")

        # 6. Add columns to 'products'
        prod_cols = get_existing_columns('products')
        if 'additional_images' not in prod_cols:
            db.session.execute(text("ALTER TABLE products ADD COLUMN additional_images TEXT"))
            print(" -> Added additional_images to products")
        if 'brand' not in prod_cols:
            db.session.execute(text("ALTER TABLE products ADD COLUMN brand VARCHAR(100)"))
            print(" -> Added brand to products")
        if 'is_diwali_deal' not in prod_cols:
            db.session.execute(text("ALTER TABLE products ADD COLUMN is_diwali_deal BOOLEAN DEFAULT 0"))
            print(" -> Added is_diwali_deal to products")
        if 'is_featured' not in prod_cols:
            db.session.execute(text("ALTER TABLE products ADD COLUMN is_featured BOOLEAN DEFAULT 1"))
            print(" -> Added is_featured to products")

        # 7. Add columns to 'users'
        user_cols = get_existing_columns('users')
        if 'avatar_url' not in user_cols:
            db.session.execute(text("ALTER TABLE users ADD COLUMN avatar_url VARCHAR(500)"))
            print(" -> Added avatar_url to users")
        if 'reset_token' not in user_cols:
            db.session.execute(text("ALTER TABLE users ADD COLUMN reset_token VARCHAR(100)"))
            print(" -> Added reset_token to users")
        if 'reset_token_expiry' not in user_cols:
            db.session.execute(text("ALTER TABLE users ADD COLUMN reset_token_expiry DATETIME"))
            print(" -> Added reset_token_expiry to users")

        db.session.commit()
        print("[+] Migration completed successfully with zero data loss!")


if __name__ == '__main__':
    run_migration()
