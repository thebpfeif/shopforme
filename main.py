from django.conf import settings

from hyvee import HyVee
from grocery_manager.models import Item
from secrets import email, password


def main():
    shop = HyVee(email=email, password=password)
    search_item = "cheese"
    product_id = shop.get_item_id(search_item)

    # Add to the database
    new_item = Item(product_id=product_id, name=search_item, brand="Hy-Vee", weight=8, weight_units="ounces")

    shop.add_to_cart(product_id=product_id, quantity=1)


if __name__ == '__main__':
    main()
