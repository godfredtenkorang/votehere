# Generated by Django 5.1.7 on 2025-04-19 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ussd', '0010_customsession_event_id_customsession_payment_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customsession',
            name='msisdn',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
