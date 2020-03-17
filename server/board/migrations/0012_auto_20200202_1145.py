# Generated by Django 3.0.2 on 2020-02-02 09:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0011_auto_20200128_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenario',
            name='is_running',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='scenarioactions',
            name='at_time',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2020, 2, 2, 9, 45, 3, 252043, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='scenario',
            name='type',
            field=models.IntegerField(choices=[(0, 'One Time'), (1, 'Everyday'), (2, 'Workdays'), (3, 'Weekend')], default=0),
        ),
    ]