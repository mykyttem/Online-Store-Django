from django.urls import path
from . import views


urlpatterns = [
    path('registration', views.accounts_users, name='accounts_registration'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('my_profile/', views.my_profile, name='my_profile')
]