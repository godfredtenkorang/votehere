# Generated by Django 4.1 on 2024-02-29 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0006_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='awards',
            options={'ordering': ('-name',), 'verbose_name_plural': 'awards'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('-name',), 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='nominees',
            options={'ordering': ('-name',), 'verbose_name_plural': 'nominees'},
        ),
    ]
