from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static  import static
from django.urls import include, path
from . import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_panel/', include('admin_panel.urls')),
    path('api/', include('api.urls')),
    path('', include('store.urls')),
    path('cart/', include('cart.urls')),
    path('payments/', include('payments.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
