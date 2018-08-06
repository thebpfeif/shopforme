import json
import re
import requests
from time import sleep

import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from grocery_manager.models import Item

from urllib import request

PRODUCT_ID_LENGTH = 7


class HyVee(object):
    def __init__(self, email, password):
        self.add_item_to_cart_url = "https://www.hy-vee.com/grocery/calls/ajax.asmx/AddItemToCart"
        self.cart_checkout_url = "https://www.hy-vee.com/shop/checkout/cart.aspx"
        self.search_url = "https://www.hy-vee.com/grocery/search?search="
        self.login_url = "https://www.hy-vee.com/grocery/login/?"

        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Length": "116",
            "Content-Type": "application/json; charset=utf-8",
            "Cookie": "TSPD_101=081c23015aab2800fbecb647c8d43823f857865d0d53dd99a007ba844f48bfe301ed0bdb086701aca11ff00a1a546c77:; TS015dca18_77=081c23015aab2800485958f954d728289cb166c4415bb86e639bcccf2075d11c15fc227c4ae24956b5c42d943cf014c8082ae3a4cd8238001bedad9a63104fa809c14fb14dec3b82df61464a376c5431e35e7d693119fd5d84cf4f1e9e636d3ae22ffd46bfb4f5bb4068d8d18c48c0dd; HV_AUTH=2kWqcJlOw%252bpEZRX90qmnr7s6OWrxgmhDzvfuetvD%252fKjsBWyryuCz7d%252bxJ5Lg%252fHXRaI4S6yHGXQY%252b3mv1ltNDHGT9yCQPm7nJcvONzX9NsWt7hUIZi6bVeapqMdb7pOwK%252b9FD1NighRFO1TZczx%252fST4HV0CdfgXDttUqO1H%252bzYW9nNOexTudA%252bRf3e9njQhZwMcONPros2bHM9vPhw%252flhDnmMBLIGxeQazNq2nVQuFZ4BRNdPPVGbjtWuZ3ymd1IX0KsRcPRwJI4rAJDlm69Lfg7yczOYqAd7B76YF1ggEgK071r0lI%252fI1UvNpBw%252bLv%252f4LEwUUIpO0jMisypm4DQAt0mfpW1h07WGlI4fY8AIMYd0KerCZCLzD4U%252fwzFW5tF27a1hwvhtN0LZIsFFzZOYCrtuEjOiu94YGGvO3A5rcksXK0z4dOTghbdHsc3RF0R8SiMyyozR7AjR0GA3QuMWwORhqElZQL4qpLkkFoddKawdR1EiXwpXiFAlCLPyI9zLGljkUmDXF7mfQIusFHPMgd3bdx9f0QRPhuHdeh%252bUujGMx7AS0fklozhXNsV2vHpVvhclzgEjZxoknsyKv5DCzCKxY%252fy4mpbX%252fjROtjUpO02FEzC7OLu0V3XcQPyMMDS6%257c; HV_SEC=2018-08-04T21%253a22%253a57Z%257cpBQ%2523Z%251d%25ef%25bf%25bd1%25ef%25bf%25bd%25ef%25bf%25bdt%25da%25a0%25ef%25bf%25bdND%25ef%25bf%25bd%25ef%25bf%25bd%253a!M%25ef%25bf%25bdC%2513%25ef%25bf%25bd%2522%2560%25ef%25bf%25bdO%25ef%25bf%25bd%25ef%25bf%25bd; mhv=2521348|fIzU2j9Xqg0GoHuaZ7mWFESB9Sf1KwEcOAwXzqm6Jhb1WQAt2SoAn1g0aNPJxNlFyOEU/PsGRXipRZbsk5fRkNHeVKMwwL6qjHxcYzfiU1VwuEn05+e/SYqFv0T9iJbyW3EOryHkGuF/Hj21G9vGZA==; CartTotals=itemCount=2&Total=5.77; __AntiXsrfToken=5473f232f6f34fb3afdc0f35efef7d0c; navigation=aisles; BIGipServer~Web_Administrators~Aisles-Online=!BbBcFfp9y8udp0zz9Ju9c6TNoVV4sU5UaxO5N9Cof5oMvoZ2ajVF809H1IB80pOb0c521gGXypGRdtY=; ConsumerReservationModel=%7B%22reservationId%22:0,%22timeslotId%22:0,%22reservationExpiration%22:%220001-01-01T00:00:00%22,%22reservationStartTime%22:%220001-01-01T00:00:00%22,%22reservationEndTime%22:%220001-01-01T00:00:00%22,%22formattedReservationExpiration%22:null,%22formattedReservationDate%22:null,%22formattedReservationTimeslot%22:null,%22canExtendReservation%22:false,%22serviceFee%22:0%7D; SelectedStore=%7B%22pickupId%22:165,%22lockerId%22:0,%22fulfillmentType%22:1,%22isLockerPickupPoint%22:false,%22hasLocker%22:false,%22hasPinCode%22:false,%22deliveryAddressId%22:0,%22deliveryZipCode%22:null,%22directions%22:null,%22storeId%22:116,%22storeCode%22:1463,%22name%22:%22Olathe%20#1%22,%22addressLineOne%22:%2214955%20W%20151st%20St%22,%22city%22:%22Olathe%22,%22state%22:%22KS%22,%22zip%22:%2266062%22,%22phone%22:null,%22distance%22:0,%22latitude%22:38.854741,%22longitude%22:-94.758013,%22fulfillmentLocationId%22:324,%22orderTypeId%22:1%7D",
            "Host": "www.hy-vee.com",
            "Referer": "https://www.hy-vee.com/shop/checkout/cart.aspx",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
            "X-Requested-With": "XMLHttpRequest",
            "X-NewRelic-ID": "VQYEUldbARAIXVdbAQUG"
        }
        self.data = {
            "hierarchyID": "0",
            "quantity": "1",
            "weightedItem": "0",
            "categoryName": "Product Detail",
            "refreshCartTotals": "true"
        }

        # Create a new web browser instance and login to Hy-Vee Aisles Online
        firefox_options = Options()
        firefox_options.add_argument("-headless")
        self.webdriver = webdriver.Firefox()
        self.webdriver.implicitly_wait(10)

        self.login(email=email, password=password)

    def login(self, email, password):
        email_field = "ctl00_ContentPlaceHolder1_txtEmail"
        password_field = "ctl00_ContentPlaceHolder1_txtPassword"

        self.webdriver.get(self.login_url)

        # Enter e-mail address and password, hit enter
        field = self.webdriver.find_element_by_id(email_field)
        field.send_keys(email)
        field = self.webdriver.find_element_by_id(password_field)
        field.send_keys(password)

        field.send_keys(Keys.ENTER)
        sleep(3)

        self.save_cookies()

    def add_to_cart(self, product_id, quantity=1):
        # Update values
        self.data['hierarchyID'] = product_id
        self.data['quantity'] = quantity

        self.data = json.dumps(self.data)
        req = requests.post(self.add_item_to_cart_url, headers=self.headers, data=self.data)
        sleep(1)

        # This navigation is just for show, we don't actually need to do this.
        self.webdriver.get(self.cart_checkout_url)

        print(req.status_code)

    def search_for_item(self, search_item):
        # ct101 denotes it's the first button, increment by 1
        all_results_first = 'ctl00_ContentPlaceHolder1_uclOtherList_rptProducts_ctl01_liProduct'
        frequent_purchases_first = 'ctl00_ContentPlaceHolder1_uclWhatIBuyList_rptProducts_ctl01_liProduct'

        # append search to the end of the url
        self.search_url += search_item

        self.webdriver.get(self.search_url)

        self.load_cookies()

        # TODO: Add option to grab the first result from 'Frequent Purchases'
        python_button = self.webdriver.find_element_by_id(all_results_first)

        python_button.click()

        # get the url of the selected product page
        newurl = self.webdriver.current_url

        product_id = self._get_product_id(newurl)

        return product_id

    def load_cookies(self):
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            self.webdriver.add_cookie(cookie)

    def save_cookies(self):
        pickle.dump(self.webdriver.get_cookies(), open("cookies.pkl", "wb"))

    def get_product_data(self, url):
        data = Item()

        # Navigate to desired webpage
        self.webdriver.get(url)

        data.brand = self._get_product_brand()
        data.count = self._get_product_count()
        data.product_id = self._get_product_id()
        data.name = self._get_product_name()
        data.weight = self._get_product_weight()
        data.units = self._get_product_weight_units()

        return data

    def _get_product_brand(self):
        # TODO
        return "hyvee"

    def _get_product_count(self):
        # TODO
        return 0

    def _get_product_id(self):
        url = self.webdriver.current_url
        id_pos = url.find('PD') + 2
        product_id = url[id_pos:id_pos + PRODUCT_ID_LENGTH]

        return product_id

    def _get_product_name(self):
        title_id = "ctl00_ContentPlaceHolder1_HeadingContainer"
        return self.webdriver.find_element_by_id(title_id).text

    def _get_product_price(self):
        price_id = "ctl00_ContentPlaceHolder1_pPrice"
        price = self.webdriver.find_element_by_id(price_id).text
        price.strip('¢').strip('$')

    def _get_product_weight(self):
        weight_id = "ctl00_ContentPlaceHolder1_liSize"
        product_weight = self.webdriver.find_element_by_id(weight_id).text
        # Strip out any letters
        product_weight = re.sub('[^0-9]+', '', product_weight)

        return product_weight

    def _get_product_weight_units(self):
        # TODO
        return "ounces"






