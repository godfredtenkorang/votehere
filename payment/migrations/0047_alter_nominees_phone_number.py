# Generated by Django 5.1.7 on 2025-05-13 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0046_nominees_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nominees',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=225, null=True),
        ),
    ]
