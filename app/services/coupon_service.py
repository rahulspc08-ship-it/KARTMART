from app.models import Coupon


class CouponService:

    @staticmethod
    def validate_and_apply(coupon_code, subtotal):
        if not coupon_code:
            return 0.0, None, "No coupon applied"
        
        clean_code = coupon_code.strip().upper()
        coupon = Coupon.query.filter_by(code=clean_code, is_active=True).first()
        
        if not coupon:
            return 0.0, None, f"Invalid promo code: {clean_code}"
            
        if coupon.is_expired:
            return 0.0, None, f"Promo code '{clean_code}' has expired or is no longer valid"

        if subtotal < coupon.min_order_amount:
            return 0.0, None, f"Code '{clean_code}' requires a minimum cart value of ₹{coupon.min_order_amount}"
            
        discount = coupon.calculate_discount(subtotal)
        return discount, coupon, f"Success! Applied {coupon.discount_percent}% discount (-₹{discount})"

    @staticmethod
    def list_featured_coupons():
        return Coupon.query.filter_by(is_active=True).all()
