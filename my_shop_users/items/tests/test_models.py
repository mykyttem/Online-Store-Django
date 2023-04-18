from django.test import TestCase
from items.models import Items, Items_Reviews, Items_Questions, Items_Questions_Replys
from datetime import date

class TestModels(TestCase):
    """test for creating models"""

    def setUp(self):
        self.item = Items.objects.create(
            name_items='Items',
            description_items='description',
            category_items='category',
            phone=380894394,
            price=20,
            joined_date=date(2023, 5, 10),
            author_id_item=1
        )

        self.item_review = Items_Reviews.objects.create(
            login_user_review='login',
            id_user_review=1,
            id_item_review=1,
            count_useful_review=0,
            count_not_useful_review=0,
            date_reviews=date(2023, 5, 10),
            text_review='test_review',
            advantages_item='advantages_review',
            disadvantages_item='disadvantages_item'
        )

        self.item_question = Items_Questions.objects.create(
            login_user_Questions='login',
            id_user_Questions=1,
            id_item_Questions=1,
            count_useful_Questions=0,
            count_not_useful_Questions=0,
            date_Questions=date(2023, 5, 10),
            text_Questions='test_question'
        )

        self.item_question_reply = Items_Questions_Replys.objects.create(
            login_user_Questions_reply='login',
            id_user_Questions_reply=1,
            id_item_Questions_reply=1,
            count_useful_Questions_reply=0,
            count_not_useful_Questions_reply=0,
            date_Questions_reply=date(2023, 5, 10),
            text_Questions_reply='test_question_reply'
        )

    def test_items_is_assigned_creation(self):
        self.assertEqual(self.item.name_items, 'Items')
        self.assertEqual(self.item.description_items, 'description')
        self.assertEqual(self.item.category_items, 'category')
        self.assertEqual(self.item.phone, 380894394)
        self.assertEqual(self.item.price, 20)
        self.assertEqual(self.item.joined_date, date(2023, 5, 10))
        self.assertEqual(self.item.author_id_item, 1)

    def test_items_reviews_is_assigned_creation(self):
        self.assertEqual(self.item_review.login_user_review, 'login')
        self.assertEqual(self.item_review.id_user_review, 1)
        self.assertEqual(self.item_review.id_item_review, 1)
        self.assertEqual(self.item_review.count_useful_review, 0)
        self.assertEqual(self.item_review.count_not_useful_review, 0)
        self.assertEqual(self.item_review.date_reviews, date(2023, 5, 10))
        self.assertEqual(self.item_review.text_review, 'test_review')
        self.assertEqual(self.item_review.advantages_item, 'advantages_review')
        self.assertEqual(self.item_review.disadvantages_item, 'disadvantages_item')

    def test_items_questions_is_assigned_creation(self):
        self.assertEqual(self.item_question.login_user_Questions, 'login')
        self.assertEqual(self.item_question.id_user_Questions, 1)
        self.assertEqual(self.item_question.id_item_Questions, 1)
        self.assertEqual(self.item_question.count_useful_Questions, 0)
        self.assertEqual(self.item_question.count_not_useful_Questions, 0)
        self.assertEqual(self.item_question.date_Questions, date(2023, 5, 10))
        self.assertEqual(self.item_question.text_Questions, 'test_question')

    def test_items_questions_replys_is_assigned_creation(self):
        self.assertEqual(self.item_question_reply.login_user_Questions_reply, 'login')
        self.assertEqual(self.item_question_reply.id_user_Questions_reply, 1)
        self.assertEqual(self.item_question_reply.id_item_Questions_reply, 1)
        self.assertEqual(self.item_question_reply.count_useful_Questions_reply, 0)
        self.assertEqual(self.item_question_reply.count_not_useful_Questions_reply, 0)
        self.assertEqual(self.item_question_reply.date_Questions_reply, date(2023, 5, 10))
        self.assertEqual(self.item_question_reply.text_Questions_reply, 'test_question_reply')