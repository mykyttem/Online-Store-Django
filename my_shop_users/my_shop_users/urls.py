from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('items.urls')),
    path('', include('accounts_users.urls')),
    path('', include('client_service.urls')),
    path('admin/', admin.site.urls),
]
