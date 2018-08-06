from django.shortcuts import render

from .forms import URLScraperForm
from hyvee import HyVee
from .models import Item
from secrets import email, password


def product_scrape(request):
    # If this is a POST request then process the Form data.
    if request.method == 'POST':
        form = URLScraperForm(request.POST)

        # TODO: Sanitize data
        hyvee = HyVee(email=email, password=password)
        url = form.data['field']
        data = hyvee.get_product_data(url)
        new_entry = Item(product_id=data.product_id,
                         name=data.name,
                         brand=data.brand,
                         count=data.count,
                         weight=data.weight,
                         weight_units=data.weight_units)
        new_entry.save()

    # If this is a GET, create the default Form.
    else:
        form = URLScraperForm()

    return render(request, 'grocery_manager/post_list.html', {'form': form})

