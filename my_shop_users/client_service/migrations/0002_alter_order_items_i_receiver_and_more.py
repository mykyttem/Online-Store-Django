# Generated by Django 4.1.3 on 2023-04-05 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_items',
            name='I_receiver',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='order_items',
            name='do_not_call_me_back',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='order_items',
            name='online_payment',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='order_items',
            name='other_person',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='order_items',
            name='payment_upon_receipt',
            field=models.BooleanField(null=True),
        ),
    ]