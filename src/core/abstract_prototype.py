from abc import ABC, abstractmethod
from src.errors.validator import Validator
from src.dto.filter import filter

"""
Абстрактный класс для 
"""
class abstract_prototype(ABC):
    __data = []

    def __init__(self, source: list) -> None:
        super().__init__()
        Validator.validate_type("source", source, list)
        self.__data = source

    @property
    def data(self) -> list:
        return self.__data
    
    @data.setter
    def data(self, data: list):
        Validator.validate_type("data", data, list)
        self.__data = data

    @abstractmethod
    def create(self, data: list, filterDto: filter):
        pass
    
        