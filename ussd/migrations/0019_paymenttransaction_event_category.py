# Generated by Django 5.1.7 on 2025-05-23 22:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0010_delete_smslog'),
        ('ussd', '0018_smslog'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenttransaction',
            name='event_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='paymenttransactions', to='ticket.event'),
        ),
    ]
