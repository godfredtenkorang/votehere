# Generated by Django 4.1 on 2024-03-01 00:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0009_delete_awards'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nominees',
            name='slug',
        ),
    ]