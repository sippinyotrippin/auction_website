# Generated by Django 4.2.1 on 2023-10-09 13:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0024_alter_comment_content_alter_comment_posting_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='posting_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 9, 13, 7, 1, 583115)),
        ),
    ]
