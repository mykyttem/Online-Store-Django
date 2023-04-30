from django.db import models


class Order_Items(models.Model):
    # Contact Information
    client_number = models.CharField(max_length=15)
    client_name = models.CharField(max_length=30)
    client_username = models.CharField(max_length=30)
    client_email = models.CharField(max_length=30)
    id_client = models.IntegerField()

    # Payment
    payment_upon_receipt = models.BooleanField(default=False, null=True)
    online_payment = models.BooleanField(default=False, null=True)

    # Recipient
    I_receiver = models.BooleanField(default=False, null=True)
    other_person = models.BooleanField(default=False, null=True)
    do_not_call_me_back = models.BooleanField(default=False, null=True)

    item_id = models.JSONField()
    authors_items = models.JSONField()

    status_order = models.CharField(max_length=30, default='Очікування')
    date_order = models.DateTimeField(null=True)
    id_confirmed_sellers = models.JSONField(default=[])
    
    # promotion code
    order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_amount_use_promotion_code = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)