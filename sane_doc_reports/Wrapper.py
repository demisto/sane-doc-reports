from abc import ABC, abstractmethod


class Wrapper(ABC):
    """ Insert elements and styles that wrap normal Element objects """

    def __init__(self, cell_object, section):
        self.cell_object = cell_object
        self.section = section

    @abstractmethod
    def insert(self):
        pass

    def __str__(self):
        return str(self)
