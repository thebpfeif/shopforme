from django.contrib import admin
from .models import Item, PriceTracking

# Register your models here. This is what allows us to modify, edit,
# and delete entries
admin.site.register(Item)
admin.site.register(PriceTracking)
