import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from icecream import ic
from .products_db_operations import get_product, get_products
from .products_message_handlers import handle_incoming_message


class ProductConsumer(AsyncJsonWebsocketConsumer):
    GROUP_NAME = 'Products'
    
    async def connect(self):
        await self.channel_layer.group_add(self.GROUP_NAME, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.GROUP_NAME, self.channel_name)
       
    async def receive(self, text_data: str):
        data = json.loads(text_data)
        if 'sort_fields' in data:
            await self._send_sorted_products(data['sort_fields'])
        else:
            await handle_incoming_message(data, self._send_product)

    async def product_message(self, event):
        await self.send(text_data=event['message'])

    async def _send_product(self, product_id, update=False):
        """Fetch a single product and send it to the group."""
        product = await get_product(product_id)
        await self._send_to_group({ 'product': product, 'update': update })
        
    async def _send_sorted_products(self, sort_fields):
        """Fetch sorted products and send them to the client."""
        products = await get_products(sort_fields)
        await self._send_to_client({ 'sorted_products': products })

    async def _send_to_group(self, message):
        """Send a message to the group."""
        await self.channel_layer.group_send(self.GROUP_NAME, {'type': 'product.message', 'message': json.dumps(message)})

    async def _send_to_client(self, message):
        """Send a message to the client."""
        await self.send(text_data=json.dumps(message))