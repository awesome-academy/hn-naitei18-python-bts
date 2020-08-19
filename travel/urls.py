from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.front_page, name='front_page'),
    path('tours/', views.TourListView.as_view(), name='tour-list'),
    path('tour/<int:pk>', views.TourDetailView.as_view(), name='tour-detail'),
    path('user/<int:pk>/history', views.BookingHistory.as_view(), name='booking-history'),
    path('user/<int:pk>/activity', views.UserActivity.as_view(), name='activity')
]
