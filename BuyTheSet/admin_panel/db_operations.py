from icecream import ic
from store.models import Product
from .models import AIChat, ChatMessages


def get_aichat_id(user_id: int) -> int:
    """
    Get or create an AIChat object for the given user.
    
    Args:
        user_id (int): The ID of the user.
        
    Returns:
        int: The ID of the AIChat object.
    """
    ai_chat, created = AIChat.objects.get_or_create(user_id=user_id)
    return ai_chat.id


def get_api_key(aichat_id: int) -> str:
    """
    Get the api key of the AIChat object with the given ID. If no AIChat object is found, return None.
    
    Args:
        aichat_id (int): The ID of the AIChat object.
        
    Returns:
        str: The api key of the AIChat object, or None if no AIChat object is found.
    """
    try:
        api_key = AIChat.objects.get(id=aichat_id).api_key
    except AIChat.DoesNotExist:
        api_key = None
    return api_key


def get_all_chats(aichat_id: int) -> ChatMessages:
    """
    Get all the ChatMessages objects associated with the AIChat object with the given ID.
    If no ChatMessages objects are found, return None.
    
    Args:
        aichat_id (int): The ID of the AIChat object.
        
    Returns:
        ChatMessages: The ChatMessages objects associated with the AIChat object, 
        or None if no ChatMessages objects are found.
    """
    try:
        chats = ChatMessages.objects.filter(chat=aichat_id)
    except ChatMessages.DoesNotExist:
        chats = None
    return chats


def get_all_products() -> Product:
    """
    Get all Product objects and prefetch their associated tags. If no Product objects are found, return None.

    Returns:
        Product: All Product objects, or None if no Product objects are found.
    """
    try:
        products = Product.objects.all().prefetch_related('tags')
        for product in products:
            product.date_created = product.date_created.strftime('%B %d, %Y')
    except Product.DoesNotExist:
        products = None
    return products