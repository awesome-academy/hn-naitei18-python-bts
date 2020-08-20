from django.shortcuts import render
import datetime
from django.views import generic


# Create your views here.


def front_page(request):
    """View function for home page of site."""
    # date = datetime.time
    context = {
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'base_generic.html', context=context)

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
    pass


class TourDetailView(generic.DetailView):
    pass


class BookingHistory(generic.View):
    pass


class UserActivity(generic.View):
    pass
