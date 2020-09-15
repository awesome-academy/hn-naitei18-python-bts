from django.test import TestCase
from django.urls import reverse
import json
from travel.models import Tour
from django.contrib.auth.models import User


class TourListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        num_of_tours = 6
        for tour_id in range(num_of_tours) :
            Tour.objects.create(title= f"Maldives {tour_id}", destination=f"Maldives {tour_id}", 
                start_location= f"Ha Noi {tour_id}", date=tour_id ,content= "Maldives là một quốc gia với gần 1,200 hòn đảo san hô lớn nhỏ tạo thành ở phía Nam Ấn Độ, thuộc Ấn Độ Dương. Trong số đó, khoảng 200 hòn đảo là có người địa phương sinh sống.",
                place=f"Ha Noi {tour_id}, Maldives {tour_id}", base_price=20000, rating= 5)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/tours')
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('tours'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('tours'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'travel/tour_list.html')
    
    def test_search_tour(self):
        response = self.client.get(reverse("tours"), {'place': 'Maldives 1' ,'duration':1, 'cost':40000})
        self.assertEqual(len(response.context['tour_list']),1)
        self.assertEqual(response.status_code, 200)

class TourDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        num_of_tours = 6
        for tour_id in range(num_of_tours) :
            Tour.objects.create(title= f"Maldives {tour_id}", destination=f"Maldives {tour_id}", 
                start_location= f"Ha Noi {tour_id}", date=tour_id ,content= "Maldives là một quốc gia với gần 1,200 hòn đảo san hô lớn nhỏ tạo thành ở phía Nam Ấn Độ, thuộc Ấn Độ Dương. Trong số đó, khoảng 200 hòn đảo là có người địa phương sinh sống.",
                place="Ha Noi, Maldives", base_price=20000, rating= 5)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/tour/1')
        self.assertEqual(response.status_code, 302)
    
    def test_view_url_accessible_by_name(self):
        url = reverse('tour-detail', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        url = reverse('tour-detail', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'travel/tour_detail.html')

class CreatingVoteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Tour.objects.create(title="Maldives", destination="Maldives", 
            start_location= "Ha Noi", date=7 ,content="Maldives là một quốc gia với gần 1,200 hòn đảo san hô lớn nhỏ tạo thành ở phía Nam Ấn Độ, thuộc Ấn Độ Dương. Trong số đó, khoảng 200 hòn đảo là có người địa phương sinh sống.",
            place="Ha Noi, Maldives", base_price=20000, rating= 5)
        User.objects.create(username = "hieu", email="hieunt@gmail.com", password="anhhieu98", is_active=True)

    def test_creating_vote(self):
        user = User.objects.get(id=1)
        check = self.client.login(username = user.username, password=user.password)
        tour = Tour.objects.get(id=1)
        url = reverse('voting', args=[tour.id])
        response = self.client.post(url,{'voting':['3']})
        self.assertEqual(response.status_code,200)

        