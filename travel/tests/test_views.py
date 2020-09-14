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

class CreateBookingViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK',is_active = True)

        test_user1.save()

        tour = Tour.objects.create(title="HaNoi", destination="a", start_location="b", date=4, content="content",
                            place="place", base_price=400, rating=5)
        tour.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/tour/1/booking')
        self.assertRedirects(response, '/accounts/login/?next=/tour/1/booking')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/tour/1/booking')
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'travel/create_booking.html')

    def test_creating_vote(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        tour = Tour.objects.get(id=1)
        url = reverse('booking', args=[tour.id])
        response = self.client.post(url,{'start_date': ['2020-09-19'], 'members': ['1']})
        self.assertEqual(response.status_code,302)



