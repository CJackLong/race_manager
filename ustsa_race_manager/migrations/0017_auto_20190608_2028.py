# Generated by Django 2.2 on 2019-06-09 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ustsa_race_manager', '0016_publishedpointslist_racerpoints'),
    ]

    operations = [
        migrations.AddField(
            model_name='racerresult',
            name='race_points',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='racerresult',
            name='race_result',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
