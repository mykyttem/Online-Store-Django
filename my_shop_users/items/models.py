from django.db import models


class Items(models.Model):
    name_items = models.CharField(max_length=255)
    description_items = models.CharField(max_length=255)
    category_items = models.CharField(max_length=255)

    phone = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    joined_date = models.DateField(null=True)
    author_id_item = models.IntegerField(null=True)

    status = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    guarantee = models.IntegerField(null=True)


class Items_Reviews(models.Model):
    login_user_review = models.CharField(max_length=255)
    id_user_review = models.IntegerField(null=True)
    id_item_review = models.IntegerField(null=True)
    count_useful_review = models.JSONField(default=[])
    count_not_useful_review = models.JSONField(default=[])

    date_reviews = models.DateField(null=True)
    
    text_review = models.CharField(max_length=255)
    advantages_item = models.CharField(max_length=255)
    disadvantages_item = models.CharField(max_length=255)


class Items_Questions(models.Model):
    login_user_Questions = models.CharField(max_length=255)
    id_user_Questions = models.IntegerField(null=True)
    id_item_Questions = models.IntegerField(null=True)

    count_useful_Questions = models.JSONField(default=[])
    count_not_useful_Questions = models.JSONField(default=[])

    date_Questions = models.DateField(null=True)
    text_Questions = models.CharField(max_length=255)


class Items_Questions_Replys(models.Model):
    login_user_Questions_reply = models.CharField(max_length=255)
    id_user_Questions_reply = models.IntegerField(null=True)
    id_item_Questions_reply = models.IntegerField(null=True)

    count_useful_Questions_reply = models.JSONField(default=[])
    count_not_useful_Questions_reply = models.JSONField(default=[])

    date_Questions_reply = models.DateField(null=True)
    text_Questions_reply = models.CharField(max_length=255)