# Generated by Django 4.1 on 2024-05-01 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0037_alter_nominees_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
    ]
