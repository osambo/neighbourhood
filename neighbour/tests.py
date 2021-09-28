from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile,Post,Comment,Location,Category,Neighborhood,Business

# Create your tests here.
class ProfileTestClass(TestCase):
    # Set up method
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile(id=1,first_name='John',last_name='Doe',user = self.user,bio='test bio')

    #Testing instance
    def test_instance(self):
        self.assertTrue(isinstance(self.profile,Profile))

class PostTestClass(TestCase):
    # Set up method
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post(id=1,title='Test',post='This is a test',user = self.user)

    #Testing instance
    def test_instance(self):
        self.assertTrue(isinstance(self.post,Post))

class CommentTestClass(TestCase):
    # Set up method
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post(id=1,title='Test',content='This is a test',user = self.user)
        self.comment = Comment(id=1,post=self.post,user=self.user)

    #Testing instance
    def test_instance(self):
        self.assertTrue(isinstance(self.comment,Comment))

class LocationTestClass(TestCase):
    #Setup method
    def setUp(self):
        self.location = Location(id=1,name='Test name')

    #Testing instance
    def test_instance(self):
        self.assertTrue(isinstance(self.location,Location))

class CategoryTestClass(TestCase):
    #Setup method
    def setUp(self):
        self.category = Category(id=1,name='Test name')

    #Testing instance
    def test_instance(self):
        self.assertTrue(isinstance(self.category,Category))

class NeighbourhoodTestClass(TestCase):
    #Setup method
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.location = Location(id=1,name='Test name')
        self.neighbourhood = Neighbourhood(id=1,name='Test name',location=self.location,admin=self.user,occupants=1)

    #Testing instance
    def test_instance(self):
        self.assertTrue(isinstance(self.neighbourhood,Neighbourhood))

    def test_create_neighbourhood(self):
        self.location.save()
        self.neighbourhood.create_neighbourhood()
        self.assertTrue(len(Neighbourhood.objects.all()) > 0)

    def test_delete_neighborhood(self):
        self.location.save()
        self.neighbourhood.create_neighbourhood()
        self.neighbourhood = Neighbourhood.objects.get(id=1)
        self.neighbourhood.delete_neighbourhood()
        self.assertTrue(len(Neighbourhood.objects.all()) == 0)

    def test_find_neighborhood(self):
        self.location.save()
        self.neighbourhood.create_neighborhood()
        self.searched_neighbourhood = Neighbourhood.find_neighbourhood(1)
        self.assertTrue(self.searched_neighbuorhood == self.neighbourhood)

    def test_update_neighborhood(self):
        self.location.save()
        self.neighbourhood.create_neighbourhood()
        self.neighbourhood = Neighbourhood.objects.get(id=1)
        self.neighbourhood.name = 'Changed name'
        self.neighbourhood.update_neighbourhood()
        self.updated_neighbourhood = Neighbourhood.objects.get(id=1)
        self.assertEqual(self.updated_neighbourhood.name,'Changed name')

    def test_update_occupants(self):
        self.location.save()
        self.neighbourhood.create_neighbourhood()
        self.neighbourhood = Neighbourhood.objects.get(id=1)
        self.neighbourhood.update_occupants()
        self.updated_neighbourhood = Neighbourhood.objects.get(id=1)
        self.assertTrue(self.updated_neighbourhood.occupants == 2)

class BusinessTestClass(TestCase):
    #Setup method
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.location = Location(id=1,name='Test name')
        self.neighbourhood = Neighbourhood(id=1,name='Test name',location=self.location,admin=self.user,occupants=1)
        self.business = Business(id=1,name='Test name')
        self.business = Business(id=1,name='Test',user=self.user,description='Test description',neighbourhood=self.neighbourhood,category=self.category,email='test@test.com')
        self.location.save()
        self.neighbourhood.save()
        self.category.save()
        self.business.save()


    #Testing instance
    def test_instance(self):
        self.assertTrue(isinstance(self.business,Business))

    def test_create_business(self):
        self.business.create_business()
        self.assertTrue(len(Business.objects.all()) > 0)

    def test_delete_business(self):
        self.business.delete_business()
        self.assertTrue(len(Business.objects.all()) == 0)

    def test_find_business(self):
        self.business = Business.find_business(1)
        self.assertEqual(self.business.id, 1)

    def test_update_business(self):
        self.business = Business.find_business(1)
        self.business.name = 'Changed name'
        self.business.update_business()
        self.updated_business = Business.find_business(1)
        self.assertEqual(self.updated_business.name, 'Changed name')