# Generated by Django 4.1.3 on 2023-03-07 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_items_joined_date_items_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='price',
            field=models.IntegerField(null=True),
        ),
    ]
