from hyvee import HyVee
from secrets import email, password


def main():
    shop = HyVee(email=email, password=password)
    product_id = shop.get_item_id("cheese")
    shop.add_to_cart(product_id=product_id, quantity=1)


if __name__ == '__main__':
    main()
