from icecream import ic
from services.cart import GlobalCartService
from .models import Cart, CartItem



def get_item_quantity(cart, product_id):
    cart_item = cart.cartitem_set.filter(product_id=product_id).first()
    if cart_item:
        return cart_item.quantity
    return 0


def update_item_quantity(cart, product_id, quantity):
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
    product = cart_item.product
    if quantity > product.quantity:
        quantity = product.quantity
    cart_item.quantity = quantity
    cart_item.save()


def get_cart_by_id(cart_id):
    return Cart.objects.get(id=cart_id)


def merge_carts(user_cart, guest_cart):
    for item in guest_cart.cartitem_set.all():
        user_item, created = CartItem.objects.get_or_create(cart=user_cart, product=item.product)
        user_item.quantity = item.quantity
        user_item.save()
    guest_cart.delete()
    

def add(cart, product, quantity):
    if not cart:
        raise ValueError("Cart is not initialized.")
    if quantity <= 0:
        raise ValueError("Quantity must be a positive integer.")
    CartItem.objects.update_or_create(cart=cart, product=product, defaults={'quantity': quantity})
    GlobalCartService.get_total_cart_items(cart)
    

def get_products(cart):
    if cart:
        return [item.product for item in cart.cartitem_set.all()]
    return []


def get_quantity(cart):
    if cart:
        return {str(item.product.id): item.quantity for item in cart.cartitem_set.all()}
    return {}


def cart_total(cart):
    if cart:
        total = 0
        for item in cart.cartitem_set.all():
            product = item.product
            quantity = item.quantity
            if product.is_sale:
                total += product.sale_price * quantity
            else:
                total += product.price * quantity
        return total
    return 0


def update_or_delete_cart_item(cart, product, quantity):
    if not cart:
        raise ValueError("Cart is not initialized.")
    if quantity <= 0:
        raise ValueError("Quantity must be a positive integer.")
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
        

def delete_cart_item(cart, product):
    if cart:
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass


def clear_all_items_from_cart(cart):
    cart.cartitem_set.all().delete()