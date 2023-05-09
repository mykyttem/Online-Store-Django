from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from . import orders


urlpatterns = [
    path('registration/', views.registration, name='accounts_registration'),
    path('sign_in/', views.sign_in, name='sign_in'),

    # profile
    path('my_profile/', views.my_profile, name='my_profile'),
    path('my_profile/edit-profile/', views.edit_profile, name='edit_profile'),
    path('profile/seller/<int:id>/<str:login>/', views.see_profile_seller, name='see_profile_seller'),
    path('my_profile/my-chats/<int:id>/', views.my_chats, name='my_chats'),
    
    path('my_profile/create_item/', views.create_item, name='create_item'),
    path('my_profile/edit_item/<int:item_id>/<str:name_items_get_edit>/', views.edit_item, name='edit_item'),
    
    # orders
    path('my_orders/', orders.my_orders, name='my_orders'),
    path('my_orders-items/<int:get_id_order>/', orders.my_orders_items, name='my_orders_items'),
    path('orders_my_client/', orders.orders_my_client, name='orders_my_client'),
    path('orders_my_client/items-cleint/<int:get_id_order>/<str:get_name_client>', orders.client_items, name='client_items')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)