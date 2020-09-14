from django.test import TestCase
from django.urls import reverse
from ..models import Profile, User, Review, Tour, Booking
from django.utils import timezone

class ReviewListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Tour.objects.create(title="HaNoi", destination="a", start_location="b", date=4, content="content",
                            place="place", base_price=400, rating=5)
        User.objects.create(username="name")
        review_number = 20
        for review_id in range(review_number):
            Review.objects.create(
                user=User.objects.get(id=1), tour=Tour.objects.get(id=1), title="title",
                content="content about the trip", rating=5
            )

    def test_reviews_view_url_exists_at_desired_location(self):
        response = self.client.get('/reviews')
        self.assertEqual(response.status_code, 302)


    def test_review_view_url_exists_at_desired_location(self):
        response = self.client.get('/review/1')
        self.assertEqual(response.status_code, 302)

    def test_pagination(self):
        pass
