from django.test import SimpleTestCase
from django.urls import reverse, resolve
from items.views import items, item_information, reviews_items, questions_items, item_search


class TestUrls(SimpleTestCase):
    """Checks whether the URL is configured correctly to view the list of items"""

    def test_items_url_resolves(self):
        url = reverse('items')
        self.assertEquals(resolve(url).func, items)


    def test_items_information_url_resolves(self):
        url = reverse('item_information', kwargs={'id': 1, 'item_name': 'test'})
        self.assertEquals(resolve(url).func, item_information)


    def test_items_reviews_url_resolves(self):
        url = reverse('item_reviews', kwargs={'id': 1, 'item_name': 'test'})
        self.assertEquals(resolve(url).func, reviews_items)


    def test_items_questions_url_resolves(self):
        url = reverse('item_questions', kwargs={'id': 1, 'item_name': 'test'})
        self.assertEquals(resolve(url).func, questions_items)

    
    def test_items_search_url_resolves(self):
        url = reverse('item_search', kwargs={'result_item_name': 'test'})
        self.assertEquals(resolve(url).func, item_search)