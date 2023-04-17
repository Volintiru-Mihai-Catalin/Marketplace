"""
This module offers the available Products.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from dataclasses import dataclass


@dataclass(init=True, repr=True, order=False, frozen=True)
class Product:
    """
    Class that represents a product.
    """
    name: str
    price: int


@dataclass(init=True, repr=True, order=False, frozen=True)
class Tea(Product):
    """
    Tea products
    """
    type: str

    def __eq__(self, other):
        if isinstance(other, Tea):
            return self.type == other.type and \
                   self.name == other.name and \
                   self.price == other.price
        return False


@dataclass(init=True, repr=True, order=False, frozen=True)
class Coffee(Product):
    """
    Coffee products
    """
    acidity: str
    roast_level: str

    def __eq__(self, other):
        if isinstance(other, Coffee):
            return self.acidity == other.acidity and \
                   self.roast_level == other.roast_level and \
                   self.name == other.name \
                   and self.price == other.price
        return False
