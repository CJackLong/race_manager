# Generated by Django 2.2 on 2019-06-12 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ustsa_race_manager', '0020_auto_20190611_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='racer',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='racer',
            name='inj',
            field=models.BooleanField(default=False),
        ),
    ]