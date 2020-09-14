from django.test import TestCase
from travel.models import Profile
from datetime import timedelta
from django.contrib.auth.models import User
from ..models import Profile, Review, Tour, Booking, Comment
from datetime import date
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

class BookingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        tour = Tour.objects.create(title="HaNoi", destination="a", start_location="b", date=4, content="content",
                            place="place", base_price=400, rating=5)
        User.objects.create(username="name")
        start_date =date.today()
        members = 2
        Booking.objects.create(user=User.objects.get(id=1), tour=tour, start_date =date.today(), return_date = start_date + timedelta(days=tour.date), members = members, price = members * tour.base_price )


    def test_get_absolute_url(self):
        booking = Booking.objects.get(id=1)
        self.assertIn('/booking/1/detail', booking.get_absolute_url().__str__())


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        tour = Tour.objects.create(title="HaNoi", destination="a", start_location="b", date=4, content="content",
                            place="place", base_price=400, rating=5)
        user = User.objects.create(username="name")
        review = Review.objects.create(user=User.objects.get(id=1), tour=Tour.objects.get(id=1), title="title",
                              picture=SimpleUploadedFile(name='test_image.jpg',
                                                         content=open("media/images/avatar/download.jpeg", 'rb').read(),
                                                         content_type='image/jpeg'),
                              content="content about the trip", rating=5)
        comment = Comment(user=user, review= review, content = "test thu thoi" )
        comment.save()

    def test_content_length(self):
        comment= Comment.objects.get(id=1)
        max_length = comment._meta.get_field('content').max_length
        self.assertEquals(max_length, 1000)
