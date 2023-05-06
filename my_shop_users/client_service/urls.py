from django.urls import path
from . import views


urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path("chat/<str:room_name>/", views.room, name="room"),
]   