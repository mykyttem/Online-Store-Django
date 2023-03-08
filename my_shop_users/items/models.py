from django.db import models



# Create your models here.
class Items(models.Model):
    name_items = models.CharField(max_length=255)
    description_items = models.CharField(max_length=255)
    category_items = models.CharField(max_length=255)

    phone = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    joined_date = models.DateField(null=True)
    author_id_item = models.IntegerField(null=True)


class Items_Reviews(models.Model):
    login_user_review = models.CharField(max_length=255)
    id_user_review = models.IntegerField(null=True)
    id_item_review = models.IntegerField(null=True)

    date_reviews = models.DateField(null=True)
    
    text_review = models.CharField(max_length=255)
    advantages_item = models.CharField(max_length=255)
    disadvantages_item = models.CharField(max_length=255)