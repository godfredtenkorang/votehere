# Generated by Django 4.1 on 2024-04-15 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0030_nominees_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nominees',
            name='content',
        ),
    ]
