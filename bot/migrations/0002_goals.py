# Generated by Django 3.0 on 2020-02-13 23:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goals', to='bot.Project')),
            ],
        ),
    ]
