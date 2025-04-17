# Generated by Django 5.1.7 on 2025-04-10 23:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('total_tickets', models.PositiveIntegerField()),
                ('available_tickets', models.PositiveIntegerField()),
                ('ticket_image', models.ImageField(default='', upload_to='ticket_img/')),
                ('date_added', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='TicketPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=14, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('quantity', models.PositiveIntegerField()),
                ('amount', models.PositiveBigIntegerField()),
                ('total_amount', models.FloatField(null=True)),
                ('ref', models.CharField(max_length=200)),
                ('verified', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.event')),
            ],
        ),
    ]
