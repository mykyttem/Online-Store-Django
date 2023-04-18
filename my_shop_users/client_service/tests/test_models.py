from django.test import TestCase
from client_service.models import Order_Items
from django.utils import timezone

class TestModels(TestCase):
    """test for creating models"""

    def setUp(self):
        self.checkout = Order_Items.objects.create(
            # Contact information
            client_number=38048932,
            client_name = 'name',
            client_username = 'username',
            client_email = 'email@gmail.com',
            id_client = 143242323,

            # Payment
            payment_upon_receipt = True,
            online_payment = False,

            # Recipient
            I_receiver = False,
            other_person = True,
            do_not_call_me_back = False,

            # Get id, name item, authors
            item_id = [1, 3, 4, 5, 6, 7, 8, 9, 10],
            authors_items = [1, 3, 4, 5, 6, 7, 8, 9, 10],
            status_order = 'Очікування',
            date_order='2023-04-18 20:21:45.720118+00:00'
        )


    def test_items_is_assigned_creation(self):
        self.assertEqual(self.checkout.client_number, 38048932)
        self.assertEqual(self.checkout.client_name, 'name')
        self.assertEqual(self.checkout.client_username, 'username')
        self.assertEqual(self.checkout.client_email, 'email@gmail.com')
        self.assertEqual(self.checkout.id_client, 143242323)

        self.assertEqual(self.checkout.payment_upon_receipt, True)
        self.assertEqual(self.checkout.online_payment, False)

        self.assertEqual(self.checkout.I_receiver, False)
        self.assertEqual(self.checkout.other_person, True)
        self.assertEqual(self.checkout.do_not_call_me_back, False)
    
        self.assertEqual(self.checkout.item_id, [1, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertEqual(self.checkout.authors_items, [1, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertEqual(self.checkout.status_order, 'Очікування')
        self.assertEqual(self.checkout.date_order, '2023-04-18 20:21:45.720118+00:00')