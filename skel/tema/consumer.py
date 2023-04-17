"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.name = kwargs['name']
        self.cart_id = self.marketplace.new_cart()

    def run(self):
        for operation in self.carts[0]:
            if operation['type'] == "add":
                for index in range(operation['quantity']):
                    while not self.marketplace.add_to_cart(self.cart_id, operation['product']):
                        sleep(self.retry_wait_time)

            elif operation['type'] == "remove":
                for index in range(operation['quantity']):
                    self.marketplace.remove_from_cart(self.cart_id, operation['product'])

        self.marketplace.place_order(self.cart_id)
