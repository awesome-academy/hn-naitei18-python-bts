from django.shortcuts import render,redirect
import datetime
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Tour, Booking
from django.shortcuts import get_object_or_404
from django.conf import settings
from travel.forms import SignUpForm, ProfileForm, UserForm
from django.contrib.auth import authenticate
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from datetime import timedelta  
from django.contrib.auth.models import User

# Create your views here.


def front_page(request):
    """View function for home page of site."""
    # date = datetime.time
    context = {
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'front_page.html', context=context)


def profile(request):
    """View function for register site."""
    context = {
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'profile.html', context=context)

def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.address = form.cleaned_data.get('address')
            user.save()
            #username = form.cleaned_data.get('username')
            #password = form.cleaned_data.get('password1')
            #user = authenticate(username=username, password=password)
            #login(request, user)
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

import sys
from django.contrib import  messages
def create_booking(request,pk):
    tour = get_object_or_404(Tour, pk=pk)
    user = User.objects.get(username=str(request.user))
    if request.method == 'POST':
        start_date = request.POST['start_date']
        members = request.POST['members']
        start_date = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        members = int(members)
        price = members * tour.base_price
        return_date = start_date + timedelta(days=tour.date)
        booking = Booking(user = user, tour = tour, start_date = start_date, return_date = return_date, price = price, members = members)
        try:
            booking.save()
        except:
            messages.error(request,'Booking fail')
            return render(request, 'travel/create_booking.html', context=context)
        else:
            messages.success(request, 'Booking success!')
            return HttpResponseRedirect(reverse('index') )
    else :
        context = {
            'tour': tour
        }
    return render(request, 'travel/create_booking.html', context=context)

class TourListView(generic.ListView):
    model = Tour


def tour_detail(request, pk):
    model = get_object_or_404(Tour, pk=pk)
    suggest_tour = Tour.objects.all().order_by('?').exclude(pk=pk)[:3]

    context = {
        'tour': model,
        'suggest_tour': suggest_tour,
    }
    return render(request, 'travel/tour_detail.html', context)


class BookingHistory(generic.View):
    pass


class UserActivity(generic.View):
    pass

