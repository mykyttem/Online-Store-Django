from django.db import models


class Order_Items(models.Model):
    # Контактна інформація
    client_number = models.CharField(max_length=15)
    client_name = models.CharField(max_length=30)
    client_username = models.CharField(max_length=30)
    client_email = models.CharField(max_length=30)

    # Оплата
    payment_upon_receipt = models.BooleanField(default=False, null=True)
    online_payment = models.BooleanField(default=False, null=True)

    # Отримувач
    I_receiver = models.BooleanField(default=False, null=True)
    other_person = models.BooleanField(default=False, null=True)
    do_not_call_me_back = models.BooleanField(default=False, null=True)

    author_item_id = models.IntegerField()