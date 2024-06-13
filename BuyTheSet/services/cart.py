from decimal import Decimal
from cart.models import Cart
from payments.models import Order


class GlobalCartService:
    @staticmethod
    def get_cart_items(cart):
        return cart.cartitem_set.all()
    
    @staticmethod
    def get_user_cart(request):
        user = request.user
        if user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=user)
        else:
            session = request.session
            cart_id = session.get('cart_id')
            if cart_id:
                cart = Cart.objects.filter(id=cart_id, user=None).first()
            if not cart_id or not cart:
                cart = Cart.objects.create(user=None)
                session['cart_id'] = cart.id
        return cart
    
    @staticmethod
    def get_total_cart_items(cart):
        return cart.cartitem_set.count()
    
    @staticmethod
    def calculate_total_cost_of_cart(cart):
        cart_items = GlobalCartService.get_cart_items(cart)
        total = sum(
            item.product.sale_price * item.quantity if item.product.is_sale 
            else item.product.price * item.quantity 
            for item in cart_items
        )
        shipping_fee = Decimal(Order._meta.get_field('shipping_fee').default)

        return total + shipping_fee