# Generated by Django 2.2 on 2019-05-18 03:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ustsa_race_manager', '0004_auto_20190426_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='racerresult',
            name='race_time',
            field=models.DurationField(default=datetime.timedelta(seconds=2400)),
        ),
    ]
