# Generated by Django 4.1.3 on 2023-03-08 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_items_author_id_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='category',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
    ]