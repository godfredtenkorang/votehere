# Generated by Django 4.1 on 2024-04-13 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0013_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
