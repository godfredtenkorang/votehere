# Generated by Django 5.1.7 on 2025-04-12 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_event_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticketpayment',
            options={'ordering': ('-date_created',)},
        ),
    ]
