# Generated by Django 2.2.5 on 2019-11-03 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('find', '0003_auto_20191103_1701'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posting',
            name='posting_id',
        ),
    ]
