# Generated by Django 4.2.1 on 2023-08-29 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='current_price',
            field=models.IntegerField(),
        ),
    ]
