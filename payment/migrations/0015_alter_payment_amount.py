# Generated by Django 4.1 on 2024-04-13 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0014_alter_payment_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
