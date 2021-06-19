# Generated by Django 3.2.4 on 2021-06-19 01:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Places',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Pending'), (2, 'In Progress'), (3, 'Finished'), (4, 'Failed')], default=1)),
                ('place_id', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('business_status', models.CharField(max_length=255)),
                ('formatted_address', models.CharField(max_length=255)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=9)),
                ('lng', models.DecimalField(decimal_places=6, max_digits=9)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('user_ratings_total', models.PositiveIntegerField()),
                ('state', models.CharField(max_length=255)),
                ('types', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('status', models.IntegerField(choices=[(1, 'Pending'), (2, 'In Progress'), (3, 'Finished'), (4, 'Failed')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField()),
                ('reviewer', models.CharField(max_length=255)),
                ('datetime', models.DateTimeField()),
                ('rating', models.PositiveSmallIntegerField()),
                ('text', models.TextField()),
                ('reply', models.JSONField(blank=True, null=True)),
                ('language', models.CharField(max_length=10)),
                ('review_id', models.CharField(max_length=255, unique=True)),
                ('likes', models.PositiveIntegerField()),
                ('sentiment_overall', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('expertai_classification', models.JSONField(blank=True, null=True)),
                ('expertai_entities', models.JSONField(blank=True, null=True)),
                ('expertai_mainLemmas', models.JSONField(blank=True, null=True)),
                ('expertai_mainPhrases', models.JSONField(blank=True, null=True)),
                ('expertai_mainSyncons', models.JSONField(blank=True, null=True)),
                ('expertai_sentiment', models.JSONField(blank=True, null=True)),
                ('expertai_topics', models.JSONField(blank=True, null=True)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.places')),
            ],
        ),
        migrations.AddField(
            model_name='places',
            name='search',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.search'),
        ),
    ]
