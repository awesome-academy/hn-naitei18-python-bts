from django.contrib import admin
from .models import Tour, Image, Booking, Review, Comment, Profile, Follower, Voting, Activity, Notification


# Register your models here.

class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_location', 'destination', 'rating')
    inlines = [ImageInline, BookingInline]


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tour', 'rating')
    inlines = [CommentInline]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone')


@admin.register(Follower)
class Follower(admin.ModelAdmin):
    """docstring for Follower"""
    list_display = ('follower', 'following', 'date_added')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'start_date', 'return_date', 'status')

@admin.register(Voting)
class VotingAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'star')

@admin.register(Activity)
class UserActivity(admin.ModelAdmin):
    list_display = ('id', 'user', 'acti', 'url', 'date')
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_user', 'action', 'status')
