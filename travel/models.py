from django.db import models
from datetime import date, datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='media/images/avatar', blank= True)
    address = models.CharField(max_length = 200, blank=True)
    phone = models.CharField(max_length = 10, null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Tour(models.Model):
    """Mode representing a tour."""
    title = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    start_location = models.CharField(max_length=200)
    date = models.IntegerField(default=1)
    content = models.TextField(max_length=1000, help_text="Enter Description ")
    place = models.CharField(max_length=200, help_text="places in tour", null=True, blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()

    class Meta:
        ordering = ['-rating']

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a particular tour instance."""
        return reverse('tour-detail', args=[str(self.id)])


class Image(models.Model):
    """Model representing Image"""
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE)

    def upload_location(self, filename):
        filebase, extension = filename.split('.')
        return 'images/%s.%s' % (self.color.name, extension)

    count = str(Tour.objects.count() + 1)
    url = models.ImageField(upload_to='images/tours/' + count)
    description = models.CharField(max_length=100, help_text="Description for images")


class Booking(models.Model):
    """Model representing booking."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE)
    start_date = models.DateField()
    return_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    members = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)

    class Status(models.IntegerChoices):
        WATTING = 1
        ACCEPTED = 2
        REJECT = 3
        CANCEL = 4
        SUCCESS = 5

    status = models.IntegerField(choices=Status.choices, default=1)

    class Meta:
        ordering = ['-create_date']

    def __str__(self):
        """String for representing the Model object."""
        return str(self.user)

    def get_absolute_url(self):
        """Returns the url to access a particular tour instance."""
        return reverse('', args=[str(self.id)])


class Review(models.Model):
    """Model representing reviews"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE)
    content = models.TextField(max_length=1000, help_text="Enter your feeling", null=True, blank=True)
    rating = models.IntegerField(help_text=" Enter 1 - 5")
    picture = models.ImageField(upload_to='images/reviews', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-rating', '-create_date']

    def get_absolute_url(self):
        """Returns the url to access a particular review instance."""
        return reverse('', args=[str(self.id)])


class Comment(models.Model):
    """docstring for comment"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey('Review', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('Comment', on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(max_length=1000)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_date']

    def __str__(self):
        """String for representing the Model object."""
        return str(self.user)

    def get_absolute_url(self):
        """Returns the url to access a particular comment instance."""
        return reverse('', args=[str(self.id)])


class Activity(object):
    """docstring for Activity"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    acti = models.CharField(max_length=200, help_text="name of activity")
    url = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        """String for representing the Model object."""
        return self.acti

    def get_absolute_url(self):
        """Returns the url to access a particular tour instance."""
        return reverse('', args=[str(self.id)])
