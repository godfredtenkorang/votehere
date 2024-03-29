# Generated by Django 4.1 on 2024-03-03 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0013_alter_category_options'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ('-date_created',)},
        ),
        migrations.AddField(
            model_name='payment',
            name='nominee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vote.nominees'),
        ),
    ]
