from django.test import SimpleTestCase
from django.urls import reverse, resolve
from client_service.views import checkout

class TestUrls(SimpleTestCase):
    """Checks whether the URL is configured correctly to view the list of elements"""

    def test_checkout(self):
        url = reverse('checkout')
        self.assertEquals(resolve(url).func, checkout)