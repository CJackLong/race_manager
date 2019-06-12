# Generated by Django 2.2 on 2019-06-08 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ustsa_race_manager', '0013_race_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignments',
            name='position',
            field=models.CharField(choices=[('ChiefRace', 'Chief of Race'), ('Datamanager', 'Data Manager'), ('Raceadmin', 'Race Administrator'), ('ChiefTiming', 'Chief of Timing'), ('Referee', 'Referee'), ('CourseChief', 'Course Chief'), ('StartReferee', 'Start Referee'), ('FinishReferee', 'Finish Referee'), ('TD', 'Technical Delegate')], default='CLR', max_length=20),
        ),
    ]
