# Generated by Django 3.2.4 on 2021-06-22 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20210619_0158'),
    ]

    operations = [
        migrations.AddField(
            model_name='places',
            name='is_agent',
            field=models.BooleanField(default=False),
        ),
    ]
