import json
from icecream import ic
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from services.cart import GlobalCartService
from store.models import Product
from .models import Cart
from . import services


@receiver(user_logged_in)
def merge_guest_cart(sender, user, request, **kwargs):
    guest_cart_id = request.session.get('cart_id')
    if guest_cart_id:
        try:
            guest_cart = services.get_cart_by_id(guest_cart_id)
            user_cart = GlobalCartService.get_user_cart(request)
            services.merge_carts(user_cart, guest_cart)
            del request.session['cart_id']
        except Cart.DoesNotExist:
            pass


def cart_add(request):
    if request.method == 'POST':
        cart = GlobalCartService.get_user_cart(request)
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        try:
            services.update_item_quantity(cart, product_id, product_qty)
            cart_quantity = GlobalCartService.get_total_cart_items(cart)
            response = {'success': True, 'cart_quantity': cart_quantity}
        except Product.DoesNotExist:
            response = {'success': False, 'error': 'Product does not exist.'}
        except Exception as e:
            response = {'success': False, 'error': str(e)}
        return JsonResponse(response)


def cart_items(request):
    cart = GlobalCartService.get_user_cart(request)
    cart_items = GlobalCartService.get_cart_items(cart)
    cart_total = GlobalCartService.calculate_total_cost_of_cart(cart)
    cart_items_data = []
    for item in cart_items:
        item_data = {
            'product': {
                'id': item.product.id,
                'name': item.product.name,
                'price': str(item.product.price),
                'sale_price': str(item.product.sale_price),
                'is_sale': item.product.is_sale,
                'quantity': item.product.quantity,
                'image_url': item.product.image.url,
            },
            'quantity': item.quantity,
        }
        cart_items_data.append(item_data)
    data = {
        'cart_items': cart_items_data,
        'cart_total': str(cart_total),
    }
    return JsonResponse(data)


def cart_delete(request):
    cart = GlobalCartService.get_user_cart(request)
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
            services.delete_cart_item(cart, product)
            cart_quantity = GlobalCartService.get_total_cart_items(cart)
            response = JsonResponse({'success': True, 'cart_quantity': cart_quantity})
        except Product.DoesNotExist:
            response = JsonResponse({'success': False, 'error': 'Product does not exist.'}, status=404)
        except Exception as e:
            response = JsonResponse({'success': False, 'error': str(e)}, status=500)
        return response
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=400)


@csrf_exempt
def cart_update(request):
    cart = GlobalCartService.get_user_cart(request)
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        try:
            product = Product.objects.get(id=product_id)
            services.update_item_quantity(cart, product_id, quantity)
            response = JsonResponse({'success': True})
        except Product.DoesNotExist:
            response = JsonResponse({'success': False, 'error': 'Product not found.'}, status=404)
        except Exception as e:
            response = JsonResponse({'success': False, 'error': str(e)}, status=500)
        return response
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=400)

