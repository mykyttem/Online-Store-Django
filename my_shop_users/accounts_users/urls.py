from django.urls import path
from . import views


urlpatterns = [
    path('registration/', views.accounts_users, name='accounts_registration'),
    path('sign_in/', views.sign_in, name='sign_in'),

    path('my_profile/', views.my_profile, name='my_profile'),
    path('my_profile/edit-profile/', views.edit_profile, name='edit_profile'),
    path('profile/seller/<int:id>/<str:login>/', views.see_profile_seller, name='see_profile_seller'),
    
    path('create_item/', views.create_item, name='create_item'),
    path('edit_item', views.edit_item, name='edit_item'),
    
    path('my_orders/', views.my_orders, name='my_orders'),
    path('my_orders-items/<int:get_id_order>/', views.my_orders_items, name='my_orders_items'),
    path('orders_my_client/', views.orders_my_client, name='orders_my_client'),
    path('orders_my_client/items-cleint/<int:get_id_order>/<str:get_name_client>', views.client_items, name='client_items')
]