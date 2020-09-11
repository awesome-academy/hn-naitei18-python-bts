from django.db import models
from datetime import date, datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from PIL import Image
from django.core.validators import MaxValueValidator
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/avatar', null=True, blank=True)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular tour instance."""
        return '/profile/%s' % self.id


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
    count = str(Tour.objects.count() + 1)
    url = models.ImageField(upload_to='images/tours/' + count)
    description = models.CharField(max_length=100, help_text="Description for images")


class Voting(models.Model):
    """Model representing Image"""
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    star = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)], null=False, blank=False)

    class Meta:
        unique_together = ('tour', 'user')


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
        WAITTING = 1
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
        return '/booking/%s/detail' % self.id


class Review(models.Model):
    """Model representing reviews"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE)
    title = models.TextField(max_length=100, help_text='One word about your trip !', )
    content = models.TextField(max_length=1000, help_text="Enter your feeling", null=True, blank=True)
    rating = models.IntegerField(help_text=" Enter 1 - 5")
    picture = models.ImageField(upload_to='images/reviews', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-rating', '-create_date']

    def get_absolute_url(self):
        """Returns the url to access a particular review instance."""
        return reverse('tour-review', args=[str(self.id)])


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
        return str(self.id)

    def get_absolute_url(self):
        """Returns the url to access a particular comment instance."""
        return reverse('', args=[str(self.id)])


class Activity(models.Model):
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


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_has_notification")
    action_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_create_notification")
    action_model_id = models.IntegerField(null=False, blank=False, default=0)
    create_date = models.DateTimeField(auto_now_add=True)

    class ActionType(models.IntegerChoices):
        FOLOW = 1
        UNFOLOW = 2
        UPDATEBOOKING = 3

    class Status(models.IntegerChoices):
        UNSEEN = 1
        SEEN = 2

    action = models.IntegerField(choices=ActionType.choices, default=0)
    status = models.IntegerField(choices=Status.choices, default=1)

    class Meta:
        ordering = ['-create_date']

    def __str__(self):
        """String for representing the Model object."""
        return str(self.get_action_display())

class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('follower', 'following')

    def __unicode__(self):
        return u'%s follows %s' % (self.follower, self.following)


def create_new_folow_notifications(sender, **kwargs):
    if kwargs['created']:
        # user_profile = UserProfile.objects.create(user = kwargs['instance'])
        folow = kwargs['instance']
        channel_layer = get_channel_layer()
        room_name = 'user_' + str(folow.following.id)
        notification = Notification(user=folow.following, action_user=folow.follower, action_model_id=folow.id,
                                    action=1, status=1)
        notification.save()
        message = {
            'pk': notification.pk,
            'action': notification.action,
            'action_model_id': notification.action_model_id,
            'action_user': notification.action_user.id,
            'user': notification.user.id,
            'create_date': notification.create_date.strftime('%H:%M %d-%m-%Y'),
            'action_username': notification.action_user.username,
            'action_type': notification.get_action_display(),
        }

        message = json.dumps(message)
        async_to_sync(channel_layer.group_send)(
            room_name, {
                'type': 'chat_message',
                'message': message
            }
        )


def create_un_folow_notifications(sender, **kwargs):
    folow = kwargs['instance']
    channel_layer = get_channel_layer()
    room_name = 'user_' + str(folow.following.id)
    notification = Notification(user=folow.following, action_user=folow.follower, action_model_id=folow.id, action=2,
                                status=1)
    notification.save()
    message = {
        'pk': notification.pk,
        'action': notification.action,
        'action_model_id': notification.action_model_id,
        'action_user': notification.action_user.id,
        'user': notification.user.id,
        'create_date': notification.create_date.strftime('%H:%M %d-%m-%Y'),
        'action_username': notification.action_user.username,
        'action_type': notification.get_action_display(),
    }
    message = json.dumps(message)
    async_to_sync(channel_layer.group_send)(
        room_name, {
            'type': 'chat_message',
            'message': message
        }
    )


def create_change_booking_notifications(sender, **kwargs):
    booking = kwargs['instance']
    if booking.status != 1 :
        channel_layer = get_channel_layer()
        superusers = User.objects.filter(is_superuser=True)
        action_user = superusers[0]
        room_name = 'user_' + str(booking.user.id)
        notification = Notification(user = booking.user, action_user = action_user ,action_model_id = booking.id, action=3, status=1)
        notification.save()
        message = {
            'pk' : notification.pk, 
            'action' : notification.action , 
            'action_model_id' : notification.action_model_id, 
            'action_user' : 'admin', 
            'user' : notification.user.id, 
            'action_username': 'admin', 
            'action_type' : notification.get_action_display(),
            'create_date' : notification.create_date.strftime('%H:%M %d-%m-%Y'),
            'booking_status' : booking.get_status_display(),
        }
        message = json.dumps(message)
        async_to_sync(channel_layer.group_send)(
            room_name,{
                'type': 'chat_message',
                'message': message
            }
        )

post_save.connect(create_change_booking_notifications, sender=Booking)
post_save.connect(create_new_folow_notifications, sender=Follower)
post_delete.connect(create_un_folow_notifications, sender=Follower)
