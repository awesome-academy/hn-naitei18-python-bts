from django.shortcuts import render, redirect
import datetime
from django.db import transaction
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Tour, Review, Booking
from django.shortcuts import get_object_or_404
from django.conf import settings
from travel.forms import SignUpForm, ProfileForm, UserForm
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from datetime import timedelta
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
import sys
from django.contrib import messages


# Create your views here.


def front_page(request):
    """View function for home page of site."""
    # date = datetime.time
    context = {
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'front_page.html', context=context)


def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    """View function for register site."""

    return render(request, 'profile_details.html', {'user': user})


@login_required
@transaction.atomic
def update_profile(request):
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
        return render(request, 'profile.html', {'form': form})


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.address = form.cleaned_data.get('address')
            user.save()
            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=password)
            # login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    """View function for register site."""
    context = {
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'registration/login.html', context=context)


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
            messages.error(request, 'Booking fail')
            return render(request, 'travel/create_booking.html', context=context)
        else:
            messages.success(request, 'Booking success!')
            return HttpResponseRedirect(reverse('index'))
    else:
        context = {
            'tour': tour
        }
    return render(request, 'travel/create_booking.html', context=context)


class TourListView(generic.ListView):
    model = Tour


def tour_detail(request, pk):
    model = get_object_or_404(Tour, pk=pk)
    suggest_tour = Tour.objects.all().exclude(pk=pk)[:3]
    suggest_review = Tour.objects.get(pk=pk).review_set.all().order_by('?')[:3]
    context = {
        'tour': model,
        'suggest_tour': suggest_tour,
        'suggest_review': suggest_review,
    }
    return render(request, 'travel/tour_detail.html', context)


def tour_review(request, pk):
    model = get_object_or_404(Review, pk=pk)
    suggest_tour = Tour.objects.all().exclude(pk=pk)[:3]
    suggest_review = model.tour.review_set.all().exclude(pk=pk)[:2]
    comment = Review.objects.get(pk=pk).comment_set.all().order_by('create_date')
    context = {
        'review': model,
        'suggest_tour': suggest_tour,
        'suggest_review': suggest_review,
        'comment_list': comment,
    }
    return render(request, 'travel/tour_review.html', context)


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
        picture = request.POST['review-image']
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
            return HttpResponseRedirect(reverse('index'))
    else:
        context = {
            'selected_tour': selected_tour,
            'tour_list': tour_list,
        }

    return render(request, 'travel/review_new.html', context)


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
        picture = request.POST['review-image']
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
            return HttpResponseRedirect(reverse('index'))
    else:
        context = {
            'tour': 'New tour',
            'tour_list': tour_list,
        }

    return render(request, 'travel/review_new.html', context)


class BookingHistory(generic.View):
    pass


class UserActivity(generic.View):
    pass
