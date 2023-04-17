"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import copy
import string
import time
from random import choice
from threading import Lock
import logging
from logging.handlers import RotatingFileHandler


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

        self.logger.info("Registered producer with ID: {0}".format(producer_id))

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
        self.logger.info("Producer with ID {0} wants to publish product {1}".format(producer_id, product))

        self.lock_producers.acquire()

        is_able_to_publish = False
        if len(self.marketplace[producer_id]) < self.queue_size_per_producer:
            product_copy = copy.copy(product)
            self.marketplace[producer_id].append(product_copy)
            self.logger.info("Producer with ID {0} published product: {1}".format(producer_id, product))

            is_able_to_publish = True

        self.lock_producers.release()
        if not is_able_to_publish:
            self.logger.info("Producer with ID {0} did not publish product: {1}".format(producer_id, product))

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
        self.logger.info("Created cart with ID: {0}".format(index))
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
        self.logger.info("Searching product {0} to add to cart {1}".format(product, cart_id))
        self.lock_consumers.acquire()
        for producer in self.marketplace.keys():
            for item in self.marketplace[producer]:
                if item == product:
                    self.marketplace[producer].remove(item)
                    self.consumer_carts[cart_id].append(item)
                    is_item_found = True
                    self.logger.info("Found product {0} and added to cart {1}".format(product, cart_id))
                    break
            if is_item_found:
                break

        self.lock_consumers.release()
        if not is_item_found:
            self.logger.info("NOT found product {0} and NOT added to cart {1}".format(product, cart_id))
        return is_item_found

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        self.logger.info("Attempting to remove product {0} from cart {1}".format(product, cart_id))
        for item in self.consumer_carts[cart_id]:
            if product == item:
                self.consumer_carts[cart_id].remove(item)
                self.logger.info("FOUND and removed product {0} from cart {1}".format(product, cart_id))
                return
        self.logger.info("NOT FOUND and removed product {0} from cart {1}".format(product, cart_id))

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        self.logger.info("Placing order from cart {0}: {1}".format(cart_id, self.consumer_carts[cart_id]))
        return self.consumer_carts[cart_id]
