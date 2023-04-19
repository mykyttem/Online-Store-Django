from django.test import TestCase
from accounts_users.models import Registration
from django.contrib.auth.hashers import make_password, check_password

import random
import string

random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(255))

class TestModels(TestCase):
    def setUp(self):
        self.password = random_string
        self.item = Registration.objects.create(
            login_user=random_string,
            email_user=f'{random_string}@gmail.com',
            password_user=make_password(self.password)
        )

    
    def test_accounts_is_assigned_creation(self):
        self.assertEqual(self.item.login_user, random_string)
        self.assertEqual(self.item.email_user, f'{random_string}@gmail.com')
        self.assertTrue(check_password(self.password, self.item.password_user))