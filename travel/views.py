from django.shortcuts import render
import datetime

from django.views import generic
from .models import Tour
from django.shortcuts import get_object_or_404


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
