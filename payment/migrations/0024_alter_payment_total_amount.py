# Generated by Django 4.1 on 2024-04-13 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0023_payment_total_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='total_amount',
            field=models.FloatField(null=True),
        ),
    ]
