# Generated by Django 4.1 on 2024-05-01 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0023_alter_category_options_remove_category_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='date_added',
            field=models.DateField(null=True, verbose_name='date added'),
        ),
        migrations.AlterField(
            model_name='category',
            name='end_date',
            field=models.DateField(null=True, verbose_name='end date'),
        ),
    ]
