from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.hashers import make_password, check_password

from accounts_users.models import Registration
from items.models import Items
from client_service.models import Order_Items

from datetime import datetime

import random
import string

random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(255))
random_range = random.randrange(0, 10000000)

class TestViewIsDisplayed(TestCase):
    def test_displayed_page_registration(self):
        response = self.client.get('/registration/')
        self.assertTemplateUsed(response, 'registration.html')


    def test_displayed_page_sign_in(self):
        response = self.client.get('/sign_in/')
        self.assertTemplateUsed(response, 'sign_in.html')


    def test_displayed_page_my_profile(self):
        # Create user
        password = random_string
        hashed_password = make_password(password)
        self.user = Registration.objects.create(
            login_user=random_string,
            email_user=f'{random_string}@gmail.com',
            password_user=hashed_password
        )

        # send POST-request
        response = self.client.post('/sign_in/', {
            'login': self.user.login_user,
            'email': self.user.email_user,
            'password': random_string,
        })

        # check that the password is valid
        self.assertTrue(check_password(password, self.user.password_user))

        # checking, successful redirect
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('my_profile'))

        # checking, data displayed
        response = self.client.get(reverse('my_profile'))
        self.assertContains(response, self.user.login_user)
        self.assertContains(response, self.user.email_user)
        self.assertContains(response, self.user.id)

        # create item for user
        self.user = Items.objects.create(
            name_items=random_string,
            description_items=random_string,
            category_items=random_string,
            phone=random_range,
            price=random_range,
            joined_date=datetime.now(),
            author_id_item=self.user.id
        )

        # check that the item is associated with the correct user
        self.assertEqual(self.user.author_id_item, self.user.id)

        # check that the item is displayed on the profile page
        response = self.client.get(reverse('my_profile'))
        self.assertContains(response, self.user.name_items)
        self.assertContains(response, self.user.price) 

        # check template
        self.assertTemplateUsed(response, 'my_profile.html')


    def setUp(self):
        # come in page 
        session = self.client.session
        session['id'] = random_range
        session.save()


    def test_my_orders(self):
        """Test check my orders, creating few items and order"""
        response = self.client.get('/my_orders/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_orders.html')

        # check my orders
        order_itemms = []
        items_orders = []   

        for i in range(3):
            self.order_item = Order_Items.objects.create(
                id_client=random_range,
                item_id=[1, 2, 3, 4, 5, 10],
                authors_items=[1, 2, 3, 4, 5, 10]
            )

            self.item = Items.objects.create(
                name_items=random_string,
                price=random_range,
                author_id_item=random_range
            )

            items_orders.append(self.item)
            order_itemms.append(self.order_item)

        response = self.client.get('/my_orders/')

        data_order = {
            'list_id_items': [],
            'list_id_order': []
        }

        for data in order_itemms:
            data_order['list_id_order'].append(data.id)        
            data_order['list_id_items'].append(data.item_id) 

        list_id_order = data_order['list_id_order']
        list_id_items = data_order['list_id_items']

        sort_data = {}

        for i in range(len(list_id_order)):
            sort_data[str(list_id_order[i])] = list_id_items[i]

        show_order_item = {}

        for number, item_ids in sort_data.items():  
            info_item = Items.objects.filter(id__in=item_ids).values()  
            show_order_item[number] = list(info_item)


        for key, value in show_order_item.items():
            for item in value:
                self.assertContains(response, item['name_items'])
                self.assertContains(response, item['price'])



    def test_orders_my_client(self):
        response = self.client.get('/orders_my_client/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders_my_client.html')

        # check orders my clients
        order_itemms = []
        items_orders = []  

        for i in range(3):
            self.order_item = Order_Items.objects.create(
                client_number=random_range,
                client_name=random_string,
                client_username=random_string,
                client_email=f'{random_string}@gmail.com',
                id_client=random_range,

                payment_upon_receipt=True,
                online_payment=False,

                I_receiver=False,
                other_person=True,
                do_not_call_me_back=True,

                status_order='Очікування',

                item_id=[1, 2, 3, 4, 6],
                authors_items=[11, 22, 32, 43, 5, 13]
            )


            self.item = Items.objects.create(
                name_items=random_string,
                price=random_range,
                author_id_item=random_range
            )

    
            items_orders.append(self.item)
            order_itemms.append(self.order_item)

        response = self.client.get('/orders_my_client/')
    
        all_orders = Order_Items.objects.filter(authors_items__icontains=10).values()
        
        for data in all_orders:
            for field in ['client_name', 'client_number', 'client_username', 'id_client', 
                          'client_email', 'payment_upon_receipt', 'online_payment', 'I_receiver', 
                          'other_person', 'do_not_call_me_back', 'status_order']:
                
                self.assertContains(response, data[field])



    def test_orders_my_client_items(self):
        url = reverse('client_items', kwargs={'get_id_order': 1, 'get_name_client': 'name_items'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client_items.html')


        # Created more items in DB
        items = []
        for i in range(3):
            item = Items.objects.create(name_items=random_string, price=random_range)
            items.append(item)


        # Get page list items
        for item in items:
            url = reverse('items')
            response = self.client.get(url)

            # Checking, on page displayed all created items
            self.assertContains(response, item.name_items)
            self.assertContains(response, item.price)


    def test_displayed_page_create_item(self):
        response = self.client.get('/create_item/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_item.html')