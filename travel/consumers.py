import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Profile, Comment, Review, Notification, Activity, Tour

from django.contrib.auth.models import User
from django.template.loader import render_to_string
import urllib.request

class ReviewConsumer(WebsocketConsumer):
    def connect(self):
        self.review_name = self.scope['url_route']['kwargs']['review_name']
        self.review_group_name = 'chat_%s' % self.review_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.review_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.review_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        parentCommentId = text_data_json['parentCommentId']
        reviewId = text_data_json['reviewId']
        userId = text_data_json['userId']
        if userId.isnumeric():
            userId = int(userId)
        user = User.objects.get(id=userId)
        review = Review.objects.get(id=reviewId)

        if parentCommentId != -1:
            parentComment = Comment.objects.get(id=parentCommentId)
            comment = Comment(user=user, parent_comment=parentComment, review=review, content=message)
        else:
            comment = Comment(user=user, review=review, content=message)
        comment.save()
        activity = Activity(user=user, acti="comment on a review", url=review.get_absolute_url())
        activity.save()
        commentInfor = {
            'parentCommentId': parentCommentId,
            'id': comment.id,
        }

        commentInfor = json.dumps(commentInfor)
        htmlRender = render_to_string("travel/includes/comments.html", {'comment': comment})

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.review_group_name,
            {
                'type': 'chat_message',
                'comment': commentInfor,
                'htmlRender': htmlRender
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        comment = event['comment']
        htmlRender = event['htmlRender']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'comment': comment,
            'htmlRender': htmlRender,
        }))


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['userId']
        self.room_group_name = 'user_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = int(text_data_json['message'])
        notitication = Notification.objects.get(pk=message)
        notitication.status = 2
        notitication.save()

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))


class SubmitReviewConsumer(WebsocketConsumer):
    def connect(self):
        self.submit_review_name = self.scope['url_route']['kwargs']['tourId']
        self.review_group_name = 'review_%s' % self.submit_review_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.review_group_name,
            self.channel_name
        )
        self.accept()
    def disconnect(self, code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.review_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        pass

    def chat_message(self, event):
        htmlRender = event['htmlRender']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            # 'review': review,
            'htmlRender': htmlRender,
        }))
