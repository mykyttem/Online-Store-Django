# Generated by Django 4.1.3 on 2023-04-05 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order_Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_number', models.CharField(max_length=15)),
                ('client_name', models.CharField(max_length=30)),
                ('client_username', models.CharField(max_length=30)),
                ('client_email', models.CharField(max_length=30)),
                ('payment_upon_receipt', models.BooleanField()),
                ('online_payment', models.BooleanField()),
                ('I_receiver', models.BooleanField()),
                ('other_person', models.BooleanField()),
                ('do_not_call_me_back', models.BooleanField()),
                ('author_item_id', models.IntegerField()),
            ],
        ),
    ]