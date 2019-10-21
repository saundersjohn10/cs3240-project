# Generated by Django 2.2.5 on 2019-10-21 02:57

from django.db import migrations, models
import find.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Posting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driver_name', models.CharField(max_length=200)),
                ('vehicle_model', models.CharField(max_length=200)),
                ('location_to', models.CharField(max_length=200)),
                ('location_from', models.CharField(max_length=200)),
                ('date', models.DateTimeField(default=find.models.default_datetime)),
                ('riding_date', models.DateTimeField(default=find.models.default_datetime)),
                ('price', models.IntegerField(default=0)),
                ('driver_id', models.CharField(max_length=200)),
                ('num_passengers', models.IntegerField(default=0)),
            ],
        ),
    ]
