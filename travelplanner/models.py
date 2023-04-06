from django.db import models
from django.contrib.auth.models import User

class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='destination_photos/', null=True, blank=True)

    def __str__(self):
        return self.name

class PackingList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class PackingItem(models.Model):
    name = models.CharField(max_length=100)
    packing_list = models.ForeignKey(PackingList, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class TravelPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    packing_list = models.ForeignKey(PackingList, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    transportation = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.destination.name

class Photo(models.Model):
    travel_plan = models.ForeignKey(TravelPlan, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='travel_plan_photos/')

    def __str__(self):
        return self.photo.name
