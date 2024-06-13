import json
import requests
from services.cart import GlobalCartService
from BuyTheSet.secrets import DISTANCEMATRIX_API_KEY


def create_shipping_address(form, user, is_collect):
    address1 = form.cleaned_data['address1']
    address2 = form.cleaned_data['address2']
    shipping_address = form.save(commit=False)
    shipping_address.user = user
    if is_collect:
        shipping_address.address1 = ''
        shipping_address.address2 = ''
    else:
        shipping_address.address1 = address1
        shipping_address.address2 = address2
    return shipping_address


def is_within_distance(destination):
    API_KEY = DISTANCEMATRIX_API_KEY
    origin = 'Cape Town City Centre, Cape Town, 8000, South Africa'
    url = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&key={API_KEY}'
    response = requests.get(url)
    data = json.loads(response.text)
    if 'rows' in data and data['rows']:
        elements = data['rows'][0]['elements']
        if elements[0]['status'] == 'OK':
            distance = elements[0]['distance']['value']
            return distance <= 50000
    return False


def get_cart_items_data(cart):
    cart_items = GlobalCartService.get_cart_items(cart)
    cart_items_data = []
    for item in cart_items:
        item_data = {
            'id': item.product.id,
            'name': item.product.name,
            'price': item.product.sale_price if item.product.is_sale else item.product.price,
            'quantity': item.quantity,
            'total': item.product.sale_price * item.quantity if item.product.is_sale else item.product.price * item.quantity,
            'image_url': item.product.image.url,
            'product': {
                'quantity': item.product.quantity,
            }
        }
        cart_items_data.append(item_data)
    return cart_items_data