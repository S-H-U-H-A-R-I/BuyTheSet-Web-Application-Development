import asyncio
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView
from icecream import ic
from .db_operations import get_aichat_id, get_api_key, get_all_chats, get_all_products    


class BaseView(UserPassesTestMixin, TemplateView):
    
    def test_func(self) -> bool:
        """
        Denies access to the view if the user is not a staff member.
        
        Returns:
            bool: True if the user is a staff member, False otherwise.
        """
        return self.request.user.groups.filter(name='staff').exists()

    def get_context_data(self, **kwargs) -> dict:
        """
        Retrieves the context data for the view. 
        Adds the API key and chat messages associated with the user's AIChat object to the context.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        aichat_id = get_aichat_id(self.request.user.id)
        context['api_key'] = get_api_key(aichat_id)
        context['chats'] = get_all_chats(aichat_id)
        return context


class PanelView(BaseView):
    template_name = 'admin_panel/panel.html'


class ProductView(BaseView):
    template_name = 'admin_panel/products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = get_all_products()
        return context