"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import copy
import string
from random import choice
from threading import Lock


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
        self.marketplace = list()
        self.producer_ids = list()
        self.consumer_carts = dict()
        self.index = 0
        self.lock_consumers = Lock()
        self.lock_producers = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        producer_id = ''.join(choice(string.digits + string.ascii_letters) for i in range(10))
        self.lock_producers.acquire()

        # Make sure that the id is unique
        while producer_id in self.producer_ids:
            producer_id = ''.join(choice(string.digits + string.ascii_letters) for i in range(10))
        self.producer_ids.append(producer_id)
        self.lock_producers.release()

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
        self.lock_producers.acquire()

        is_able_to_publish = False
        if len(self.marketplace) < self.queue_size_per_producer:
            self.marketplace.append(copy.copy(product))
            is_able_to_publish = True

        self.lock_producers.release()

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
        self.lock_consumers.acquire()
        for item in self.marketplace:
            if item == product:
                self.marketplace.remove(item)
                self.consumer_carts[cart_id].append(item)
                is_item_found = True
                break

        self.lock_consumers.release()
        return is_item_found

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        for item in self.consumer_carts[cart_id]:
            if product == item:
                self.consumer_carts[cart_id].remove(item)
                return

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        return self.consumer_carts[cart_id]
