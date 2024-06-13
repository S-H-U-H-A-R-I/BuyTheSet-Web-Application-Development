import json
from.products_db_operations import create_or_update_product

async def handle_incoming_message(data, send_product):
    """Update or create a product based on the message"""
    product_id = int(data['id'])
    field = data['field']
    value = data['value']
    new_fields = {field: value}
    created = await create_or_update_product(product_id, new_fields)
    await send_product(product_id, not created)