from django.core.exceptions import ValidationError
from django.test import TestCase
from ..models import Review, Tour, User
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
# from datetime import date, datetime
# Create your tests here.

class ReviewModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ReviewModelTest, cls).setUpClass()
        Tour.objects.create(title="HaNoi", destination="a", start_location="b", date=4, content="content",
                            place="place", base_price=400, rating=5)
        User.objects.create(username="name")
        Review.objects.create(user=User.objects.get(id=1), tour=Tour.objects.get(id=1), title="title",
                              picture=SimpleUploadedFile(name='test_image.jpg',
                                                         content=open("media/images/avatar/download.jpeg", 'rb').read(),
                                                         content_type='image/jpeg'),
                              content="content about the trip", rating=5)

    def test_title_length(self):
        review = Review.objects.get(id=1)
        max_length = review._meta.get_field('title').max_length
        self.assertEquals(max_length, 100)

    def test_content_length(self):
        review = Review.objects.get(id=1)
        max_length = review._meta.get_field('content').max_length
        self.assertEquals(max_length, 1000)

    def test_rating_value(self):
        review = Review.objects.get(id=1)
        if int(review.rating) > 5:
            raise ValidationError(_('Review rating beyond 5'))
        elif int(review.rating) <0:
            raise ValidationError(_('Review rating under 0'))

    def test_get_absolute_url(self):
        review = Review.objects.get(id=1)
        self.assertIn('/review/1', review.get_absolute_url().__str__())
