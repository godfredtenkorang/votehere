# Generated by Django 5.1.7 on 2025-07-02 13:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0049_payment_transaction_id'),
        ('vote', '0033_remove_category_nomination_start_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestForPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=225)),
                ('phone', models.CharField(max_length=14)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('account_details', models.TextField()),
                ('date_requested', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vote.category')),
            ],
            options={
                'ordering': ('-date_requested',),
            },
        ),
    ]
