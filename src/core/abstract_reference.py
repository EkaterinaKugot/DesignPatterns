from abc import ABC, abstractmethod
import uuid
from src.errors.validator import Validator

"""
Абстрактный класс для обработки моделей
"""
class abstract_reference(ABC):
    __name = ""

    def __init__(self):
        self.__id = uuid.uuid1().int

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name: str):
        Validator.validate_type("name", name, str)
        Validator.validate_permissible_length("name", name, 50)
        self.__name = name.strip()

    @property
    def id(self) -> int:
        return self.__id

    """
    Абстрактный метод для сравнения равенства
    """
    @abstractmethod
    def __eq__(self, other_model) -> bool:
        if other_model is None: return False
        if not isinstance(other_model, abstract_reference): return False
        return self.id == other_model.id
    
    """
    Абстрактный метод для сравнения неравенства
    """
    @abstractmethod
    def __ne__(self, other_model) -> bool:
        return self.id != other_model.id