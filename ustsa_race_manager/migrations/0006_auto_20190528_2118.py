# Generated by Django 2.2 on 2019-05-29 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ustsa_race_manager', '0005_racerresult_race_time'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='racerresult',
            constraint=models.UniqueConstraint(fields=('racer', 'race'), name='unique_race_result'),
        ),
    ]