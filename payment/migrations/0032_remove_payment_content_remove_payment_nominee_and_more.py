# Generated by Django 4.1 on 2024-04-17 23:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0031_remove_nominees_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='content',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='nominee',
        ),
        migrations.DeleteModel(
            name='Nominees',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
