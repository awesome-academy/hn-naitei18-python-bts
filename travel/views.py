from django.shortcuts import render, redirect
import datetime
from django.db import transaction
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Tour, Review, Booking, Follower, Profile, Voting, Activity, Notification
from django.shortcuts import get_object_or_404
from django.conf import settings
from travel.forms import SignupForm, ProfileForm, UserForm
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from datetime import timedelta
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
import sys
from django.contrib import messages
from django.core.paginator import Paginator
from asgiref.sync import async_to_sync
import json
from channels.layers import get_channel_layer
# Create your views here.


def front_page(request):
    """View function for home page of site."""
    # date = datetime.time
    all_tour = Tour.objects.all()
    context = {
        'tour_list': all_tour,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'front_page.html', context=context)


@login_required
def follow(request, pk):
    if request.method == 'POST':
        tuser = get_object_or_404(User, pk=pk)
        is_followed = 0

        if (Follower.objects.filter(follower=request.user, following=tuser)):
            Follower.objects.filter(follower=request.user, following=tuser).delete()
            is_followed = 0
            activity = Activity(user=request.user, acti="now unfollow user" + tuser.username, url = tuser.profile.get_absolute_url())
        else:
            follow = Follower(follower=request.user, following=tuser)
            follow.save()
            is_followed = 1
            activity = Activity(user=request.user, acti="now follow user" + tuser.username, url = tuser.profile.get_absolute_url())
        review_num = Review.objects.filter(user=tuser).count()
        activity.save()

        return render(request, 'profile_details.html',
                      {'user': tuser, 'is_followed': is_followed, 'review_num': review_num})
    else:
        url = request.META.get('HTTP_REFERER')
        return  HttpResponseRedirect(url)

from django.core import serializers
from django.db.models import Count
import json
# @login_required
def get_notification(request):
    user = User.objects.get(username=str(request.user))
    notifications = Notification.objects.filter(user=user, status=1)
    notification_list = [ i for i in notifications.values('pk', 'action', 'action_model_id', 'action_user', 'user')]
    for i, notification in enumerate(notification_list):
        notification['action_username'] = notifications[i].action_user.username
        notification['action_type'] = notifications[i].get_action_display()
        notification['create_date'] = notifications[i].create_date.strftime('%H:%M %d-%m-%Y')
        if int(notification['action']) == 3 :
            notification['booking_status'] = Booking.objects.get(pk=notification['action_model_id']).get_status_display()
    message = {
        "notifications" : notification_list
    }
    message = json.dumps(message)
    return HttpResponse(message)

def profile(request, pk):
    is_followed = 0
    user = get_object_or_404(User, pk=pk)
    review_num = Review.objects.filter(user=user).count()
    if request.user.is_authenticated:
        if Follower.objects.filter(follower=request.user, following=user):
            is_followed = 1
    return render(request, 'profile_details.html', {'user': user, 'is_followed': is_followed, 'review_num': review_num})


@login_required
@transaction.atomic
def update_profile(request):
    review_num = Review.objects.filter(user=request.user).count()
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            if request.FILES.get('avatar', None) != None:
                try:
                    os.remove(request.user.profile.avatar.url)
                except Exception as e:
                    print('Exception in removing old profile image: ', e)
                request.user.profile.avatar = request.FILES['avatar']
                request.user.profile.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return HttpResponseRedirect(reverse('profile'))
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {'form': form, 'review_num': review_num})


from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.mail import send_mail
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

import os
import environ

env = environ.Env()
# reading .env file
environ.Env.read_env()


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.address = form.cleaned_data.get('address')
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your travel account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = "html"
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def login(request):
    """View function for register site."""
    context = {
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'registration/login.html', context=context)


@login_required
def create_booking(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    user = User.objects.get(username=str(request.user))
    if request.method == 'POST':
        start_date = request.POST['start_date']
        members = request.POST['members']
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        members = int(members)
        price = members * tour.base_price
        return_date = start_date + timedelta(days=tour.date)
        booking = Booking(user=user, tour=tour, start_date=start_date, return_date=return_date, price=price,
                          members=members)
        try:
            booking.save()
        except:
            context = {
                'tour': tour
            }
            messages.error(request, 'Booking fail')
            return render(request, 'travel/create_booking.html', context=context)
        else:
            messages.success(request, 'Booking success!')
            current_site = get_current_site(request)
            html_message = render_to_string('travel/request_booking_mail.html', {'booking': booking,'domain': current_site.domain})
            send_mail(
                subject='Request booking',
                message='{0} request booking with tour {1}'.format(request.user, tour),
                html_message=html_message,
                from_email=env('EMAIL_HOST_USER'),
                recipient_list=[env('EMAIL_ADMIN'), ]
            )
            activity = Activity(user=user, acti="booking a tour " + tour.title, url=booking.get_absolute_url())
            activity.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        context = {
            'tour': tour
        }
    return render(request, 'travel/create_booking.html', context=context)


from django.db.models import Avg


def create_voting(request, pk):

    tour = get_object_or_404(Tour, pk=pk)
    user = User.objects.get(username=str(request.user))
    if request.method == 'POST':
        rate = int(request.POST.getlist('voting')[0])
        try:
            vote = tour.voting_set.get(user=user)
        except:
            vote = Voting(tour=tour, user=user, star=rate)
        else:
            vote.star = rate

        try:
            vote.save()
        except:
            messages.error(request, 'Voting fail')
        else:
            tour.rating = tour.voting_set.aggregate(Avg('star'))['star__avg']
            tour.save()
            messages.success(request, 'Voting success!')
        return HttpResponseRedirect(reverse('tour-detail', kwargs={'pk': tour.id}))

def logout(request):
    auth_logout(request)
    return redirect('index')


def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    context = {
        'booking': booking
    }
    return render(request, 'travel/booking_detail.html', context=context)


@login_required
def booking_history(request):
    user = User.objects.get(username=str(request.user))
    booking_list = user.booking_set.all()
    context = {
        'booking_list': booking_list
    }
    return render(request, 'travel/booking_history.html', context=context)


def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    try:
        booking.delete()
    except:
        messages.error(request, 'Delete booking fail')
        return render(request, reverse('booking_detail', kwargs={'pk': booking.id}), context={'booking': booking})
    else:
        messages.success(request, 'Delete booking success')
        return HttpResponseRedirect(reverse('booking-history'))

def booking_status(request, pk,status):
    booking = get_object_or_404(Booking, pk=pk)
    booking.status = status
    booking.save()

    return HttpResponseRedirect(reverse('index'))


class TourListView(generic.ListView):
    model = Tour

    def get_queryset(self):
        place_query = self.request.GET.get('place')
        date_query = self.request.GET.get('duration')
        cost_query = self.request.GET.get('cost')
        list = Tour.objects.all()
        if place_query is not None:
            if place_query == "":
                pass
            else:
                list = Tour.objects.filter(title__icontains=place_query)
        if date_query is not None:
            if date_query == 'Duration':
                pass
            elif date_query.isnumeric():
                date_query = int(date_query)
                if date_query == 0:
                    pass
                else:
                    list = list.filter(date=date_query)
        if cost_query is not None:
            if cost_query == 'Cost':
                pass
            elif cost_query.isnumeric():
                cost_query = int(cost_query)
                if cost_query == 0:
                    pass
                else:
                    list = list.filter(base_price__in=range(cost_query))
        return list

def review_list(request):
    list = Review.objects.all().order_by('-create_date')
    suggest_tour = Tour.objects.all()[:3]
    paginator = Paginator(list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'review_list': list,
        'suggest_tour': suggest_tour,
        'page_obj': page_obj,
    }
    return render(request, 'travel/review_list.html', context)


def tour_detail(request, pk):
    model = get_object_or_404(Tour, pk=pk)
    suggest_tour = Tour.objects.all().exclude(pk=pk)[:3]
    suggest_review = Tour.objects.get(pk=pk).review_set.all().order_by('-create_date')[:3]
    try:
        user = User.objects.get(username=str(request.user))
        voting = model.voting_set.get(user=user)
    except:
        voting = None
    context = {
        'tour': model,
        'suggest_tour': suggest_tour,
        'suggest_review': suggest_review,
        'voting': voting,
    }
    if request.method == 'POST':
        title = request.POST.get('review-title', 'Default title')
        content = request.POST.get('content', 'Default content')
        rating = request.POST.get('rating', '5')
        rating = int(rating)
        if request.FILES.get('review-image', None) is not None:
            picture = request.FILES['review-image']
        review = Review(user=user, tour=model, title=title, content=content, rating=rating, picture=picture)

        try:
            review.save()
        except:
            messages.error(request, 'Submit review fail')
        else:
            messages.success(request, 'Submit review success!')
            # activity = Activity(user=user, acti="create a review for tour " + model.title, url=review.get_absolute_url())
            # activity.save()
            channel_layer = get_channel_layer()
            room_name = 'review_Tour' + str(review.tour.id)
            htmlRender = render_to_string('travel/includes/review.html', {'review': review})
            # Send message to room group
            async_to_sync(channel_layer.group_send)(
                room_name,
                {
                    'type': 'chat_message',
                    'htmlRender': htmlRender,
                }
            )
    return render(request, 'travel/tour_detail.html', context)


def tour_review(request, pk):
    model = get_object_or_404(Review, pk=pk)
    suggest_tour = Tour.objects.all().exclude(pk=pk)[:3]
    suggest_review = model.tour.review_set.all().exclude(pk=pk)[:2]
    comment = Review.objects.get(pk=pk).comment_set.all().order_by('-create_date')
    context = {
        'review': model,
        'suggest_tour': suggest_tour,
        'suggest_review': suggest_review,
        'comment_list': comment,
    }
    return render(request, 'travel/tour_review.html', context)


@login_required
def review_new(request, pk):
    selected_tour = get_object_or_404(Tour, pk=pk)
    tour_list = Tour.objects.all()
    user = User.objects.get(username=str(request.user))
    if request.method == 'POST':
        tour = request.POST.get('tour-name')
        tour = Tour.objects.get(id=tour)
        title = request.POST.get('review-title', 'Default title')
        content = request.POST.get('content', 'Default content')
        rating = request.POST.get('rating', '5')
        rating = int(rating)
        if request.FILES.get('review-image', None) is not None:
            picture = request.FILES['review-image']
        review = Review(user=user, tour=tour, title=title, content=content, rating=rating, picture=picture)

        try:
            review.save()
        except:
            context = {
                'selected_tour': selected_tour,
                'tour_list': tour_list,
            }
            messages.error(request, 'Booking fail')
            return render(request, 'travel/review_new.html', context=context)
        else:
            messages.success(request, 'Booking success!')
            activity = Activity(user=user, acti="create a review for tour " + tour.title, url=review.get_absolute_url())
            activity.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        context = {
            'selected_tour': selected_tour,
            'tour_list': tour_list,
        }

    return render(request, 'travel/review_new.html', context)


@login_required
def create_review(request):
    user = User.objects.get(username=str(request.user))
    tour_list = Tour.objects.all()
    if request.method == 'POST':
        tour = request.POST.get('tour-name')
        tour = Tour.objects.get(id=tour)
        title = request.POST.get('review-title', 'Default title')
        content = request.POST.get('content', 'Default content')
        rating = request.POST.get('rating', '5')
        rating = int(rating)
        if request.FILES.get('review-image', None) is not None:
            picture = request.FILES['review-image']
        review = Review(user=user, tour=tour, title=title, content=content, rating=rating, picture=picture)

        try:
            review.save()
        except:
            context = {
                'tour_list': tour_list,
            }
            messages.error(request, 'Booking fail')
            return render(request, 'travel/review_new.html', context=context)
        else:
            messages.success(request, 'Booking success!')
            activity = Activity(user=user, acti="create a review for tour " + tour.title, url=review.get_absolute_url())
            activity.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        context = {
            'tour': 'New tour',
            'tour_list': tour_list,
        }

    return render(request, 'travel/review_new.html', context)


@login_required
def user_activity(request):
    user = User.objects.get(username=str(request.user))
    self_activities = user.activity_set.all()
    following_list1 = Follower.objects.filter(follower=request.user)
    actilist = []
    for a in following_list1:
        name = a.following.activity_set.all()
        for abc in name:
            actilist.append(abc)

    context = {
        'user': user,
        'self_activities': self_activities,
        'following_activities': actilist,
        'fl_ac_count': actilist.__len__(),
    }
    return render(request, 'travel/user_activity.html', context)
