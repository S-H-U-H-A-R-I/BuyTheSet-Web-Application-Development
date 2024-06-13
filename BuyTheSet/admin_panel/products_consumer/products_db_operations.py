from channels.db import database_sync_to_async
from icecream import ic
from typing import Dict, List, Optional, Tuple
from store.models import Product


@database_sync_to_async
def create_or_update_product(product_id: int, new_fields: dict) -> bool:
    """
    Create a new product or update an existing one in the database.
    Return if the product was created.
    """
    product, created = Product.objects.get_or_create(pk=product_id)
    for field, value in new_fields.items():
        if hasattr(product, field):
            setattr(product, field, value)
    product.save()
    return created

@database_sync_to_async
def get_product(product_id) -> Dict:
    """Fetch a single product from the database."""
    product = Product.objects.filter(pk=product_id).prefetch_related('tags').first()
    return product.serialize_product() if product else None

@database_sync_to_async
def get_products(sort_fields: Optional[List[str]] = None) -> List[Dict]:
    """Fetch all products from the database."""
    products = Product.objects.all().prefetch_related('tags', 'additional_images')
    if sort_fields:
        order_fields = ['-{}'.format(field) if field == 'date_created' else field for field in sort_fields]            
        products = products.order_by(*order_fields)
    return [product.serialize_product() for product in products]