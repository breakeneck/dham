# Generated by Django 3.0.2 on 2020-01-21 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route', models.CharField(max_length=64)),
                ('params', models.CharField(max_length=255)),
                ('code', models.TextField()),
                ('is_default', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('ip', models.GenericIPAddressField(protocol='IPv4')),
                ('active', models.BooleanField()),
                ('actions', models.ManyToManyField(to='board.Actions')),
            ],
        ),
    ]
