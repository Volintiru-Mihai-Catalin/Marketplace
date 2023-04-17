"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self)
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.products = products
        self.name = kwargs['name']
        self.daemon = kwargs['daemon']
        self.id = self.marketplace.register_producer()

    def run(self):
        while self.daemon:
            for order in self.products:
                (product, quantity, process_time) = order

                index = 0
                while index < quantity:
                    pub_status = self.marketplace.publish(self.id, order[0])
                    if pub_status:
                        index += 1
                    else:
                        sleep(self.republish_wait_time)
