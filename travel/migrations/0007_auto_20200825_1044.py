# Generated by Django 3.0.8 on 2020-08-25 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0006_auto_20200824_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='media/images/avatar'),
        ),
    ]
