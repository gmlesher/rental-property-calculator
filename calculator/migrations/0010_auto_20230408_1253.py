# Generated by Django 3.2.7 on 2023-04-08 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0009_auto_20211207_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersettings',
            name='addr_blacklist',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='blacklist_bool',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
