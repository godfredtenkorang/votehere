# Generated by Django 5.0.5 on 2024-06-23 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0026_blog'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='slug',
            field=models.SlugField(max_length=10, null=True),
        ),
    ]
