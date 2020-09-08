from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/comment/(?P<review_name>\w+)/$', consumers.ReviewConsumer),
    re_path(r'ws/notification/(?P<userId>\w+)/$', consumers.NotificationConsumer),
    re_path(r'ws/review/(?P<tourId>\w+)/$', consumers.SubmitReviewConsumer),
]


