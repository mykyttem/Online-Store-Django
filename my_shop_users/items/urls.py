from django.urls import path
from . import views


urlpatterns = [
    path('items/', views.items, name='items'),
    path('items/<int:id>/<str:item_name>/', views.item_information, name='item_information'),
    path('items/<int:id>/<str:item_name>/reviews', views.reviews_items, name='item_reviews'),
    path('items/<int:id>/<str:item_name>/questions', views.questions_items, name='item_questions'),
    path('items/search_item/<str:result_item_name>', views.item_search, name='item_search')
]