# Generated by Django 5.1.7 on 2025-03-21 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0042_pageexpiration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='email',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='name',
        ),
    ]
