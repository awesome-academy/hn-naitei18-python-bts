from django.urls import path
from django.conf.urls import url
from . import views
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='home/', permanent=True)),
    path('home/', views.front_page, name='index'),
    # path('register/', views.register, name='register'),
    path('editprofile/', views.update_profile, name='profile'),
    path('profile/<int:pk>', views.profile, name='profile-details'),
    path('profile/<int:pk>/follow', views.follow, name='follow'),
    path('login', views.login, name='login'),
    path('tours/', views.TourListView.as_view(), name='tours'),
    path('tour/<int:pk>', views.tour_detail, name='tour-detail'),

    path('tour/<int:pk>/booking', views.create_booking, name='booking'),
    path('reviews', views.review_list, name='review-list'),
    path('review/<int:pk>', views.tour_review, name='tour-review'),
    path('review/<int:pk>/new', views.review_new, name='review-new'),
    path('review/new', views.create_review, name='create-review', ),
    path('user/history', views.booking_history, name='booking-history'),
    path('booking/<int:pk>/detail', views.booking_detail, name='booking_detail'),
    path('booking/<int:pk>/delete', views.booking_delete, name='booking_delete'),
    path('booking/<int:pk>/<int:status>', views.booking_status, name='booking_status'),

    path('user/bookinglist', views.booking_history, name='booking-history'),

    path('notifications/', views.get_notification, name='get_notification'),

    url(r'^register/$', views.signup, name='register'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('logout/', views.logout, name='logout'),
    path('tour/<int:pk>/voting', views.create_voting, name='voting'),
    path('user/activity', views.user_activity, name='user-activity'),
]
