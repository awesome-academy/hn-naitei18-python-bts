from django.contrib import admin
from .models import Tour, Image, Booking, Review, Comment


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
    list_display = ('user', 'tour', 'rating')
    inlines = [CommentInline]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'start_date', 'return_date', 'status')
