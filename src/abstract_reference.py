from abc import ABC, abstractmethod
import uuid

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
    def name(self, value: str):
        if not isinstance(value, str) or len(value) > 50:
            raise TypeError("Некорректно передан параметр!")
        self.__name = value.strip()

    @property
    def id(self) -> int:
        return self.__id

    def __eq__(self, other_model) -> bool:
        return self.equal(other_model)
    
    def __ne__(self, other_model) -> bool:
        return self.unequal(other_model)

    """
    Абстрактный метод для сравнения равенства
    """
    @abstractmethod
    def equal(self, other) -> bool:
        if other is None: return False
        if not isinstance(other, abstract_reference): return False
        return self.id == other.id
    
    """
    Абстрактный метод для сравнения неравенства
    """
    @abstractmethod
    def unequal(self, other) -> bool:
        return self.id != other.id