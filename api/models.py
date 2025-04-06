from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Car(models.Model):
    marka = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.IntegerField()
    price = models.IntegerField()
    mileage = models.FloatField()
    body_type = models.CharField(max_length=255)
    transmission = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    phoneNumber = models.CharField(max_length=11)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'car')