# Generated by Django 3.0 on 2020-02-15 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date_start',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='tguser',
            name='date_joined',
            field=models.DateField(auto_now_add=True),
        ),
    ]
