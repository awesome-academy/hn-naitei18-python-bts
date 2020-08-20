from django.shortcuts import render
import datetime
from django.views import generic
from .models import Tour


# Create your views here.


def front_page(request):
    """View function for home page of site."""
    # date = datetime.time
    context = {
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'front_page.html', context=context)


def register(request):
    """View function for register site."""
    context = {
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'register.html', context=context)


def login(request):
    """View function for register site."""
    context = {
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'registration/login.html', context=context)


class TourListView(generic.ListView):
    model = Tour
    # def tour_image =

class TourDetailView(generic.DetailView):
    model = Tour


class BookingHistory(generic.View):
    pass


class UserActivity(generic.View):
    pass
