"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread, Lock
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
        self.print_lock = Lock()

    def run(self):
        for order_batch in self.carts:
            for operation in order_batch:
                if operation['type'] == "add":
                    index = 0
                    while index < operation['quantity']:
                        while not self.marketplace.add_to_cart(self.cart_id, operation['product']):
                            sleep(self.retry_wait_time)
                        index += 1

                elif operation['type'] == "remove":
                    index = 0
                    while index < operation['quantity']:
                        self.marketplace.remove_from_cart(self.cart_id, operation['product'])
                        index += 1

        product_list = self.marketplace.place_order(self.cart_id)

        self.print_lock.acquire()
        for product in product_list:
            print("{0} bought {1}".format(self.name, product))
        self.print_lock.release()
