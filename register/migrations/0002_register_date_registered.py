# Generated by Django 4.1 on 2024-03-02 04:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='date_registered',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]