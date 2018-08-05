from hyvee import HyVee


def main():
    shop = HyVee("email@gmail.com", "password")
    product_id = shop.get_item_id("cheese")
    shop.add_to_cart(product_id=product_id, quantity=1)


if __name__ == '__main__':
    main()
