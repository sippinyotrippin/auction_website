# Generated by Django 4.2.1 on 2023-08-30 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_listing_current_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('your_listing', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='yolisting', to='auctions.listing')),
            ],
        ),
    ]
