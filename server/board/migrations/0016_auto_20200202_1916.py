# Generated by Django 3.0.2 on 2020-02-02 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0015_auto_20200202_1852'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeekDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=8)),
            ],
        ),
        migrations.AlterField(
            model_name='scenarioactions',
            name='at_time',
            field=models.TimeField(default='00:00'),
        ),
        migrations.AddField(
            model_name='scenarioactions',
            name='days',
            field=models.ManyToManyField(blank=True, to='board.WeekDay'),
        ),
    ]
