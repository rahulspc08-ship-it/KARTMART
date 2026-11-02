from app.extensions import db
from app.models import Product


class InventoryService:

    @staticmethod
    def check_availability(product_id, requested_qty):
        product = Product.query.get(product_id)
        if not product or not product.is_active:
            return False, "Product is not available"
        if product.stock < requested_qty:
            return False, f"Insufficient stock for {product.name}. Available: {product.stock}"
        return True, "Available"

    @staticmethod
    def deduct_stock(product_id, quantity):
        product = Product.query.get(product_id)
        if product and product.stock >= quantity:
            product.stock -= quantity
            db.session.add(product)
            return True
        return False

    @staticmethod
    def restore_stock(product_id, quantity):
        product = Product.query.get(product_id)
        if product:
            product.stock += quantity
            db.session.add(product)
            return True
        return False

    @staticmethod
    def get_low_stock_items(threshold=5):
        return Product.query.filter(Product.stock <= threshold, Product.is_active.is_(True)).all()
