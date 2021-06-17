# Generated by Django 3.2.4 on 2021-06-17 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='status',
            field=models.IntegerField(choices=[(1, 'Finished'), (2, 'Pending'), (3, 'In Progress'), (4, 'Failed')], default=2),
        ),
    ]
