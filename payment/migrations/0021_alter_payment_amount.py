# Generated by Django 4.1 on 2024-04-13 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0020_alter_payment_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.FloatField(default=0.0),
        ),
    ]
