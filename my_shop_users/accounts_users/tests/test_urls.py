from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts_users.views import accounts_users, sign_in, my_profile, create_item, edit_item, my_orders, orders_my_client, client_items

class TestUrls(SimpleTestCase):
    def test_accounts_users(self):
        url = reverse('accounts_registration')  
        self.assertEqual(resolve(url).func, accounts_users)
    

    def test_sign_in(self):
        url = reverse('sign_in')
        self.assertEqual(resolve(url).func, sign_in)


    def test_my_profile(self):
        url = reverse('my_profile')
        self.assertEqual(resolve(url).func, my_profile)


    def test_create_item(self):
        url = reverse('create_item')
        self.assertEqual(resolve(url).func, create_item)


    def test_edit_item(self):
        url = reverse('edit_item')
        self.assertEqual(resolve(url).func, edit_item)


    def test_my_orders(self):
        url = reverse('my_orders')
        self.assertEqual(resolve(url).func, my_orders)


    def test_orders_my_client(self):
        url = reverse('orders_my_client')
        self.assertEqual(resolve(url).func, orders_my_client)


    def test_client_items(self):
        url = reverse('client_items', kwargs={'get_id_order': 1, 'get_name_client': 'name'})
        self.assertEqual(resolve(url).func, client_items)