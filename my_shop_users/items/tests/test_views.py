from django.test import TestCase
from django.urls import reverse
from items.models import Items, Items_Reviews, Items_Questions, Items_Questions_Replys

import random
import string
from datetime import datetime

random_range = random.randrange(0, 10000000)
random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(255))

class TestViewsIsDisplayed(TestCase):
    """
    Test whether the data from models are displayed on the pages
    """

    def test_displayed_items(self):
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


    def test_displayed_items_information(self):
        items = []
        for i in range(3):
            item = Items.objects.create(name_items=random_string, price=random_range, description_items=random_string)
            items.append(item)

        for item in items:
            url = reverse('item_information', kwargs={'id': item.id, 'item_name': item.name_items})
            response = self.client.get(url)

            self.assertContains(response, item.name_items)
            self.assertContains(response, item.price)
            self.assertContains(response, item.description_items)


    def test_displayed_items_reviews(self):
        item = Items.objects.create(name_items=random_string, price=random_range, description_items=random_string)

        reviews = []
        for i in range(3):
            review = Items_Reviews.objects.create(login_user_review=random_string, id_item_review=item.id, 
                                                    date_reviews=datetime.now(), 
                                                    text_review=random_string, advantages_item=random_string, 
                                                    disadvantages_item=random_string)
            reviews.append(review)


        url = reverse('item_reviews', kwargs={'id': item.id, 'item_name': item.name_items})
        response = self.client.get(url)

        for review in reviews:
            self.assertContains(response, review.login_user_review)
            self.assertContains(response, review.date_reviews.strftime('%B %d, %Y'))
            self.assertContains(response, review.text_review)
            self.assertContains(response, review.advantages_item)
            self.assertContains(response, review.disadvantages_item)


    def test_displayed_items_Questions(self):
        item = Items.objects.create(name_items=random_string)

        Questions = []
        for i in range(3):
            questionn = Items_Questions.objects.create(login_user_Questions=random_string, id_item_Questions=item.id, 
                                                    date_Questions=datetime.now(), 
                                                    text_Questions=random_string)
            Questions.append(questionn)


        url = reverse('item_questions', kwargs={'id': item.id, 'item_name': item.name_items})
        response = self.client.get(url)

        for question in Questions:
            self.assertContains(response, question.login_user_Questions)
            self.assertContains(response, question.date_Questions.strftime('%B %d, %Y'))
            self.assertContains(response, question.text_Questions)


        # test questions replys
        Questions_Replys = []
        for i in range(3):
            questionn_replys = Items_Questions_Replys.objects.create(login_user_Questions_reply=random_string, id_item_Questions_reply=item.id, 
                                                    date_Questions_reply=datetime.now(), 
                                                    text_Questions_reply=random_string)
            Questions_Replys.append(questionn_replys)


        url = reverse('item_questions', kwargs={'id': item.id, 'item_name': item.name_items})
        response = self.client.get(url)

        for question_replys in Questions_Replys:
            self.assertContains(response, question_replys.login_user_Questions_reply)
            self.assertContains(response, question_replys.date_Questions_reply.strftime('%B %d, %Y'))
            self.assertContains(response, question_replys.text_Questions_reply)


    def test_displayed_items_search(self):
        items = []
        for i in range(3):
            item = Items.objects.create(name_items=random_string)
            items.append(item)


        for item in items:
            url = reverse('item_search', kwargs={'result_item_name': item.name_items})
            response = self.client.get(url)


            self.assertContains(response, item.name_items)
            self.assertContains(response, item.price)