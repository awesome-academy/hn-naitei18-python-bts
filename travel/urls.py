from django.urls import path
from . import views
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='home/', permanent=True)),
    path('home/', views.front_page, name='index'),
    path('register/', views.register, name='register'),
    path('login', views.login, name='login'),
    path('tours/', views.TourListView.as_view(), name='tours'),
    path('tour/<int:pk>', views.TourDetailView.as_view(), name='tour-detail'),
    path('user/<int:pk>/history', views.BookingHistory.as_view(), name='booking-history'),
    path('user/<int:pk>/activity', views.UserActivity.as_view(), name='activity')
]

