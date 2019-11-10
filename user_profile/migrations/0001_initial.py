# Generated by Django 2.2.5 on 2019-11-10 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('cellphone', models.CharField(max_length=200)),
                ('car_type', models.CharField(max_length=200)),
                ('license_plate', models.CharField(max_length=200)),
                ('rides_driven', models.TextField()),
                ('rides_passenger', models.TextField()),
                ('rides_pending', models.TextField(default=',')),
                ('rides_declined', models.TextField(default=',')),
            ],
        ),
    ]
