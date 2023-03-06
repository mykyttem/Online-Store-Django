from django.db import models



# Create your models here.
class Items(models.Model):
    name_items = models.CharField(max_length=255)
    description_items = models.CharField(max_length=255)
    phone = models.IntegerField(null=True)
    joined_date = models.DateField(null=True)