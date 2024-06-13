from services.cart import GlobalCartService


def get_cart(request):
    cart=GlobalCartService.get_user_cart(request)
    return {'cart': cart, 'cart_quantity': GlobalCartService.get_total_cart_items(cart)}