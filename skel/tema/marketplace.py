"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import re
import copy
import time
import string
import logging
import unittest
from random import choice
from threading import Lock
from logging.handlers import RotatingFileHandler
from .product import Tea


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor
        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.marketplace = dict()
        self.consumer_carts = dict()
        self.index = 0
        self.lock_consumers = Lock()
        self.lock_producers = Lock()

        self.logger = logging.getLogger("Logger")
        self.logger.setLevel(logging.INFO)
        self.console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        self.console_formatter.converter = time.gmtime
        self.file_handler = RotatingFileHandler("marketplace.log", "a", 4096, 10)
        self.file_handler.setFormatter(self.console_formatter)
        self.logger.addHandler(self.file_handler)

        self.logger.info("Initialized Marketplace class")

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        producer_id = ''.join(choice(string.digits + string.ascii_letters) for i in range(10))
        self.lock_producers.acquire()

        # Make sure that the id is unique
        while producer_id in self.marketplace.keys():
            producer_id = ''.join(choice(string.digits + string.ascii_letters) for i in range(10))
        self.marketplace.update({producer_id: list()})
        self.lock_producers.release()

        self.logger.info("Registered producer with ID: %s", producer_id)

        return producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace
        :type producer_id: String
        :param producer_id: producer id
        :type product: Product
        :param product: the Product that will be published in the Marketplace
        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        self.logger.info("Producer with ID %s wants to publish product %s", producer_id, product)

        self.lock_producers.acquire()

        is_able_to_publish = False
        if len(self.marketplace[producer_id]) < self.queue_size_per_producer:
            product_copy = copy.copy(product)
            self.marketplace[producer_id].append(product_copy)
            self.logger.info("Producer with ID %s published product: %s", producer_id, product)

            is_able_to_publish = True

        self.lock_producers.release()
        if not is_able_to_publish:
            self.logger.info("Producer with ID %s did NOT publish product: %s",
                             producer_id, product)

        return is_able_to_publish

    def new_cart(self):
        """
        Creates a new cart for the consumer
        :returns an int representing the cart_id
        """
        self.lock_consumers.acquire()

        index = self.index
        self.consumer_carts.update({index: list()})
        self.index += 1

        self.lock_consumers.release()
        self.logger.info("Created cart with ID: %d", index)
        return index

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns
        :type cart_id: Int
        :param cart_id: id cart
        :type product: Product
        :param product: the product to add to cart
        :returns True or False. If the caller receives False, it should wait and then try again
        """
        is_item_found = False
        self.logger.info("Searching product %s to add to cart %d", product, cart_id)
        self.lock_consumers.acquire()
        for producer in self.marketplace:
            for item in self.marketplace[producer]:
                if item == product:
                    self.marketplace[producer].remove(item)
                    self.consumer_carts[cart_id].append(item)
                    is_item_found = True
                    self.logger.info("Found product %s and added to cart %d", product, cart_id)
                    break
            if is_item_found:
                break

        self.lock_consumers.release()
        if not is_item_found:
            self.logger.info("NOT found product %s and NOT added to cart %d", product, cart_id)
        return is_item_found

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.
        :type cart_id: Int
        :param cart_id: id cart
        :type product: Product
        :param product: the product to remove from cart
        """
        self.logger.info("Attempting to remove product %s from cart %d", product, cart_id)
        for item in self.consumer_carts[cart_id]:
            if product == item:
                self.consumer_carts[cart_id].remove(item)
                self.logger.info("FOUND and removed product %s from cart %d", product, cart_id)
                return
        self.logger.info("NOT FOUND and removed product %s from cart %d", product, cart_id)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.
        :type cart_id: Int
        :param cart_id: id cart
        """
        self.logger.info("Placing order from cart %s: %s", cart_id, self.consumer_carts[cart_id])
        return self.consumer_carts[cart_id]


class TestMarketplaceMethods(unittest.TestCase):
    """
    Class that tests the functionality of Marketplace's methods.
    """

    def setUp(self) -> None:
        """
        Setup function to initialize the Marketplace instance
        """
        self.market = Marketplace(20)

    def test_register_producer(self):
        """
        Tests the functionality of 'register_producer' method
        """
        regex_pattern = r'^[a-zA-Z0-9]{10}$'
        self.assertTrue(re.match(regex_pattern, self.market.register_producer()),
                        "FAILED test_register_producer")

    def test_publish(self):
        """
        Tests the functionality of 'publish' function
        """
        producer = self.market.register_producer()
        product = Tea('Linden', 9, 'Herbal')
        self.market.publish(producer, product)
        self.assertTrue(product in self.market.marketplace[producer], "FAILED test_publish")

    def test_new_cart(self):
        """
        Tests the functionality of 'new_cart' function
        """
        cart_id = self.market.new_cart()
        self.assertTrue(cart_id == self.market.index - 1, "FAILED test_new_cart")

    def test_add_to_cart(self):
        """
        Tests the functionality of 'add_to_cart' function
        """
        producer = self.market.register_producer()
        product = Tea('Linden', 9, 'Herbal')
        product2 = Tea('Vietnam Oolong', 10, 'Oolong')
        self.market.publish(producer, product)
        self.market.publish(producer, product2)
        cart_id = self.market.new_cart()
        self.assertTrue(self.market.add_to_cart(cart_id, product2))
        self.assertEqual(product2, self.market.consumer_carts[cart_id].pop(0))

    def test_remove_from_cart(self):
        """
        Tests the functionality of 'remove_from_cart' function
        """

    def test_place_order(self):
        """
        Tests the functionality of 'place_order' function
        """
