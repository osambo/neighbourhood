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
