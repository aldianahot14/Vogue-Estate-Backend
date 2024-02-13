from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Agent(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    license = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

   
    def __str__(self):
        return self.name
    
    def has_listing(self):
        return self.listings.exists()

class Listing(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    description = models.TextField()
    price = models.PositiveIntegerField()
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    sqft = models.PositiveIntegerField()
    agent = models.ForeignKey(Agent, related_name='listings', on_delete=models.CASCADE)


def __str__(self):
        return f"{self.address}, {self.city}, {self.state} {self.zipcode}"

class ListingImage(models.Model):
    property = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.URLField(max_length=200)

    def __str__(self):
        return f"Image for {self.property}"


class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    


    def __str__(self):
        return self.name