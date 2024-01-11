from django.db import models
from django.utils.timezone import now


# Create your models here.

# Django models
class CarMake(models.Model):
    name = models.CharField(max_length=30, default='Need to fill')
    description = models.CharField(max_length=100, default="Need to fill")

    def __str__(self):
        return self.name


class CarModel(models.Model):
    TYPE_CHOICES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('SPORT', 'Sport'),
    ]
    maker = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, default='Need to fill')
    dealer_id = models.IntegerField(default=0)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, null=False)
    year = models.DateField(default=now, blank=True)
    def __str__(self):
        return self.name


# Pyhon classes
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, state, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.state = state
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

 
# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id
        
    def __str__(self):
        return "Dealer name: " + self.dealership + " Review: " + self.review + " Sentiment: " + self.sentiment
    