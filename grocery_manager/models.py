from django.db import models
from django.utils import timezone


class Item(models.Model):
    product_id = models.IntegerField()
    name = models.CharField(max_length=250)
    brand = models.CharField(max_length=100)
    count = models.IntegerField()
    weight = models.IntegerField()

    def __str__(self):
        return "%s" % self.name
