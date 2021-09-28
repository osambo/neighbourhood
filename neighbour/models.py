from django.db import models

# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length = 40)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length = 40)

    def __str__(self):
        return self.name

class Neighbourhood(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    location = models.ForeignKey(Location, on_delete = models.CASCADE,null = True)
    occupants = models.IntegerField(default=0)

    def save_neighbourhood(self):
        self.save()

    def __str__(self):
        return self.name

    def create_neighbourhood(self):
        self.save()

    def delete_neighbourhood(self):
        self.delete()

    def update_neighbourhood(self):
        self.save()

    def update_occupants(self):
        self.occupants += 1
        self.save()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE,related_name = 'profile')
    first_name = models.CharField(max_length = 50,null=True)
    last_name = models.CharField(max_length = 50,null=True)
    bio = models.TextField(null=True)
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE)
    location = models.ForeignKey(Location,on_delete = models.CASCADE,null=True)
    email = models.EmailField(max_length=60, blank=True)
    
    def __str__(self):
        return self.user.username

class Business(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name = 'business_user')
    name =models.CharField(max_length=60)
    description = models.CharField(max_length = 150,null=True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE,null=True)
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE,related_name = 'business_neighbourhood')
    email =models.EmailField(max_length=60, blank=True)

    def __str__(self):
        return self.name

    def create_business(self):
        self.save()

    def delete_business(self):
        self.delete()

    @classmethod
    def search_business(cls,search_term):
        business = Business.objects.get(name__icontains=search_term)
        return business

    def update_business(self):
        self.save()
class Post(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=60)
    post=models.TextField()
    neighbourhood = models.ForeignKey(Neighbourhood,on_delete = models.CASCADE,null=True)
    posted=models.DateTimeField(auto_now_add=True) 
    

    def __str__(self):
        return self.title