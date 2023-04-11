from django.db import models


class Order_Items(models.Model):
    # Контактна інформація
    client_number = models.CharField(max_length=15)
    client_name = models.CharField(max_length=30)
    client_username = models.CharField(max_length=30)
    client_email = models.CharField(max_length=30)
    id_client = models.IntegerField()

    # Оплата
    payment_upon_receipt = models.BooleanField(default=False, null=True)
    online_payment = models.BooleanField(default=False, null=True)

    # Отримувач
    I_receiver = models.BooleanField(default=False, null=True)
    other_person = models.BooleanField(default=False, null=True)
    do_not_call_me_back = models.BooleanField(default=False, null=True)

    # Get id, name item
    item_id = models.JSONField()
    status_order = models.CharField(max_length=30, default='Очікування')
    date_order = models.DateTimeField(null=True)