# Generated by Django 5.1.1 on 2024-10-11 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews_api', '0006_remove_movie_description_remove_movie_movie_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.CharField(blank=True, default='Action', max_length=255, null=True),
        ),
    ]
