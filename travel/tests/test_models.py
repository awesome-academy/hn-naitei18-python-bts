from django.test import TestCase
from travel.models import Tour, Image, Voting
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

class TourModelTest(TestCase):
    @classmethod
    def setUpTestData(self):
        Tour.objects.create(title="Maldives", destination="Maldives", 
            start_location= "Ha Noi", date=7 ,content="Maldives là một quốc gia với gần 1,200 hòn đảo san hô lớn nhỏ tạo thành ở phía Nam Ấn Độ, thuộc Ấn Độ Dương. Trong số đó, khoảng 200 hòn đảo là có người địa phương sinh sống.",
            place="Ha Noi, Maldives", base_price=20000, rating= 5)

    def test_title_max_length(self):
        tour = Tour.objects.get(id=1)
        title = tour._meta.get_field('title').max_length
        self.assertEquals(title, 200)

    def test_date_default(self):
        tour = Tour.objects.get(id=1)
        date_default = tour._meta.get_field('date').default 
        self.assertEquals(date_default, 1) 

    def test_get_absolute_url(self):
        tour = Tour.objects.get(id=1)
        url = tour.get_absolute_url()
        self.assertIn('tour/1',url)
    
    def test_object_name(self):
        tour = Tour.objects.get(id=1)
        self.assertEquals(str(tour), tour.title)


class ImageModelTest(TestCase):
    @classmethod
    def setUpTestData(self):
        tour = Tour.objects.create(title="Maldives", destination="Maldives", 
            start_location= "Ha Noi", date=7 ,content="Maldives là một quốc gia với gần 1,200 hòn đảo san hô lớn nhỏ tạo thành ở phía Nam Ấn Độ, thuộc Ấn Độ Dương. Trong số đó, khoảng 200 hòn đảo là có người địa phương sinh sống.",
            place="Ha Noi, Maldives", base_price=20000, rating= 5)
        image = Image()
        image.tour = tour
        image.url =  SimpleUploadedFile(name='dog.jpg', content=open('/home/nthieubk/Desktop/dog.jpg', 'rb').read(), content_type='image/jpg')
        image.description = "Cho maldives"
        image.save()
    
    def test_description_max_length(self):
        image = Image.objects.get(id=1)
        description = image._meta.get_field('description').max_length
        self.assertEquals(description,100)
    
    def test_image_path(self):
        image = Image.objects.get(id=1)
        path = 'images/tours/'
        self.assertIn(path,str(image.url))

class VotingModelTest(TestCase):
    @classmethod
    def setUpTestData(self):
        tour = Tour.objects.create(title="Maldives", destination="Maldives", 
            start_location= "Ha Noi", date=7 ,content="Maldives là một quốc gia với gần 1,200 hòn đảo san hô lớn nhỏ tạo thành ở phía Nam Ấn Độ, thuộc Ấn Độ Dương. Trong số đó, khoảng 200 hòn đảo là có người địa phương sinh sống.",
            place="Ha Noi, Maldives", base_price=20000, rating= 5)
        user = User.objects.create(username= "hieu", email="hieunt@gmail.com", password="anhhieu98")
        Voting.objects.create(user=user, tour= tour, star = 3)
    
    def test_star_default(self):
        voting = Voting.objects.get(id=1)
        star = voting._meta.get_field('star').default
        self.assertEquals(star,0)

