# Generated by Django 4.1 on 2024-03-03 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0014_nominees_can_vote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nominees',
            name='can_vote',
            field=models.BooleanField(default=True),
        ),
    ]
