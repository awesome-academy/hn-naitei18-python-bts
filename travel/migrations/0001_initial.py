# Generated by Django 3.0.8 on 2020-08-18 12:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('destination', models.CharField(max_length=200)),
                ('start_location', models.CharField(max_length=200)),
                ('date', models.IntegerField(default=1)),
                ('content', models.TextField(help_text='Enter Description ', max_length=1000)),
                ('place', models.CharField(blank=True, help_text='places in tour', max_length=200, null=True)),
                ('rating', models.FloatField()),
            ],
            options={
                'ordering': ['-rating'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, help_text='Enter your feeling', max_length=1000, null=True)),
                ('rating', models.IntegerField(help_text=' Enter 1 - 5')),
                ('picture', models.CharField(blank=True, max_length=100, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.Tour')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['create_date'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.ImageField(upload_to='images/')),
                ('description', models.CharField(help_text='Description for images', max_length=100)),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.Tour')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=1000)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('parent_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='travel.Comment')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.Review')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-create_date'],
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('return_date', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('members', models.IntegerField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(1, 'Watting'), (2, 'Accepted'), (3, 'Reject'), (4, 'Cancel'), (5, 'Success')], default=1)),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.Tour')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-create_date'],
            },
        ),
    ]