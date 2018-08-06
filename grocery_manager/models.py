from django.db import models
from django.utils import timezone


class Item(models.Model):
    product_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250)
    brand = models.CharField(max_length=100)
    count = models.IntegerField(default=1)
    weight = models.FloatField(default=0)
    weight_units = models.CharField(max_length=10, default="None")

    def __str__(self):
        return "%s" % self.name


class PriceTracking(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    price = models.FloatField()
    sale = models.BooleanField(default=False)
