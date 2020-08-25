from django.urls import path
from . import views
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='home/', permanent=True)),
    path('home/', views.front_page, name='index'),
    path('register/', views.register, name='register'),
    path('editprofile/', views.update_profile, name='profile'),
    path('profile/<int:pk>', views.profile, name='profile-details'),
    path('login', views.login, name='login'),
    path('tours/', views.TourListView.as_view(), name='tours'),
    path('tour/<int:pk>', views.tour_detail, name='tour-detail'),
    path('review/<int:pk>', views.tour_review, name='tour-review'),
    path('user/<int:pk>/history', views.BookingHistory.as_view(), name='booking-history'),
    path('user/<int:pk>/activity', views.UserActivity.as_view(), name='activity'),
    path('tour/<int:pk>/booking',views.create_booking,name='booking'),
]
