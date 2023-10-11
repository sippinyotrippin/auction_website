# Generated by Django 4.2.1 on 2023-10-09 11:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_alter_listing_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
        ),
        migrations.AddField(
            model_name='bid',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]