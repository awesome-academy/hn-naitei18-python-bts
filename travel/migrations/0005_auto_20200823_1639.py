# Generated by Django 3.1 on 2020-08-23 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0004_merge_20200821_0756'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.TextField(default='Title of your review !', help_text='One word about your trip !', max_length=100),
        ),
        migrations.AlterField(
            model_name='image',
            name='url',
            field=models.ImageField(upload_to='images/tours/5'),
        ),
    ]
