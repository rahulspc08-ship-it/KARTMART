from app.extensions import db
from app.models import CartItem, Product


class CartService:

    @staticmethod
    def get_cart_query(user_id=None, session_id=None):
        if user_id:
            return CartItem.query.filter_by(user_id=user_id)
        elif session_id:
            return CartItem.query.filter_by(session_id=session_id)
        return CartItem.query.filter(False)

    @classmethod
    def get_cart_details(cls, user_id=None, session_id=None):
        items = cls.get_cart_query(user_id, session_id).all()
        subtotal = sum(item.subtotal for item in items)
        total_items = sum(item.quantity for item in items)
        delivery_fee = 0.0 if (subtotal > 499 or subtotal == 0) else 40.0
        
        return {
            'items': items,
            'cart_items': items,
            'subtotal': round(subtotal, 2),
            'total_items': total_items,
            'delivery_fee': delivery_fee,
            'total': round(subtotal + delivery_fee, 2)
        }

    @classmethod
    def add_to_cart(cls, product_id, quantity=1, user_id=None, session_id=None):
        product = Product.query.get(product_id)
        if not product or not product.is_active:
            return False, "Product not available"
        if product.stock < 1:
            return False, "Sorry, this product is currently out of stock"

        existing_item = cls.get_cart_query(user_id, session_id).filter_by(product_id=product_id).first()
        if existing_item:
            new_qty = existing_item.quantity + quantity
            if new_qty > product.stock:
                return False, f"Only {product.stock} units available in stock"
            existing_item.quantity = new_qty
        else:
            if quantity > product.stock:
                return False, f"Only {product.stock} units available in stock"
            item = CartItem(
                user_id=user_id,
                session_id=session_id if not user_id else None,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(item)

        db.session.commit()
        return True, f"Added {product.name} to cart"

    @classmethod
    def update_quantity(cls, cart_item_id, quantity, user_id=None, session_id=None):
        item = cls.get_cart_query(user_id, session_id).filter_by(id=cart_item_id).first()
        if not item:
            return False, "Cart item not found"

        if quantity <= 0:
            db.session.delete(item)
            db.session.commit()
            return True, "Item removed from cart"

        if quantity > item.product.stock:
            return False, f"Only {item.product.stock} units available in stock"

        item.quantity = quantity
        db.session.commit()
        return True, "Cart updated"

    @classmethod
    def remove_item(cls, cart_item_id, user_id=None, session_id=None):
        item = cls.get_cart_query(user_id, session_id).filter_by(id=cart_item_id).first()
        if item:
            db.session.delete(item)
            db.session.commit()
            return True, "Item removed"
        return False, "Item not found"

    @classmethod
    def clear_cart(cls, user_id=None, session_id=None):
        cls.get_cart_query(user_id, session_id).delete()
        db.session.commit()
        return True

    @classmethod
    def merge_guest_cart(cls, session_id, user_id):
        if not session_id or not user_id:
            return
        guest_items = CartItem.query.filter_by(session_id=session_id).all()
        for g_item in guest_items:
            existing = CartItem.query.filter_by(user_id=user_id, product_id=g_item.product_id).first()
            if existing:
                existing.quantity = min(existing.quantity + g_item.quantity, existing.product.stock)
                db.session.delete(g_item)
            else:
                g_item.user_id = user_id
                g_item.session_id = None
        db.session.commit()
