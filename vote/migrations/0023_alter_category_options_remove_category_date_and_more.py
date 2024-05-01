# Generated by Django 4.1 on 2024-05-01 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0022_remove_category_content'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('-date_added',), 'verbose_name_plural': 'categories'},
        ),
        migrations.RemoveField(
            model_name='category',
            name='date',
        ),
        migrations.AddField(
            model_name='category',
            name='date_added',
            field=models.DateTimeField(null=True, verbose_name='date added'),
        ),
        migrations.AddField(
            model_name='category',
            name='end_date',
            field=models.DateTimeField(null=True, verbose_name='end date'),
        ),
    ]
