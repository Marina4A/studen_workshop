from django.db import models

class RepairJob(models.Model):
    car_make = models.TextField()
    car_model = models.TextField()
    description = models.TextField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.car_make} {self.car_model} - {self.description}, ${self.price}"