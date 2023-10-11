# Generated by Django 4.2.1 on 2023-10-09 13:54

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0025_alter_comment_posting_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='posting_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 9, 13, 54, 40, 920532)),
        ),
    ]