# Generated by Django 2.2 on 2019-06-06 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ustsa_race_manager', '0009_auto_20190606_0145'),
    ]

    operations = [
        migrations.CreateModel(
            name='RaceOfficial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('ussa_number', models.CharField(max_length=200)),
                ('fis_td_number', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='race',
            name='state',
            field=models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], default='NY', max_length=200),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='race',
            name='officials',
        ),
        migrations.CreateModel(
            name='Assignments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('official', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ustsa_race_manager.RaceOfficial')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ustsa_race_manager.Race')),
            ],
        ),
        migrations.AddField(
            model_name='race',
            name='officials',
            field=models.ManyToManyField(through='ustsa_race_manager.Assignments', to='ustsa_race_manager.RaceOfficial'),
        ),
    ]