from django.db import models


class Items(models.Model):
    name_items = models.CharField(max_length=255)
    description_items = models.CharField(max_length=255)
    category_items = models.CharField(max_length=255)

    phone = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    joined_date = models.DateField()
    author_id_item = models.IntegerField()

    status = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    guarantee = models.IntegerField(blank=True, null=True)

    amount_item = models.IntegerField()
    
    # old price
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True)


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