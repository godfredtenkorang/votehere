# Generated by Django 5.1.7 on 2025-05-20 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0005_smslog'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='access_code',
            field=models.CharField(blank=True, max_length=4, null=True, unique=True),
        ),
    ]
