# Generated by Django 2.2 on 2019-06-08 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ustsa_race_manager', '0012_auto_20190606_0348'),
    ]

    operations = [
        migrations.AddField(
            model_name='race',
            name='status',
            field=models.CharField(choices=[('i', 'Imported'), ('p', 'Published')], default='i', max_length=200),
        ),
    ]