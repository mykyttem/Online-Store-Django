# Generated by Django 4.1.3 on 2023-03-08 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0009_items_reviews_id_item_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='items_reviews',
            old_name='id_item_comment',
            new_name='id_item_review',
        ),
    ]