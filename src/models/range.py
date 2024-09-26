from src.core.base_model import base_model_name
from src.errors.validator import Validator

"""
Модель единицы измерения
"""
class range_model(base_model_name):
    __conversion_factor: int = 1
    __base_range: range = None

    """
    Значение
    """
    @property
    def conversion_factor(self) -> int:
        return self.__conversion_factor
    
    @conversion_factor.setter
    def conversion_factor(self, conversion_factor: int):
        Validator.validate_type("conversion_factor", conversion_factor, int)
        self.__conversion_factor = conversion_factor

    """
    Базовая единица измеения
    """
    @property
    def base_range(self) -> 'range_model':
        return self.__base_range
    
    @base_range.setter
    def base_range(self, base_range: 'range_model'):
        Validator.validate_type("base_range", base_range, range_model)
        self.__base_range = base_range

    @staticmethod
    def create(name: str, conversion_factor: int, base_range: 'range_model' = None) -> 'range_model':
        item = range_model()
        item.name = name
        item.conversion_factor = conversion_factor
        if base_range is not None:
            Validator.validate_permissible_value("base_range", base_range.conversion_factor, conversion_factor)
            item.base_range = base_range
            
        return item
    
    def to_dict(self):
        return {
            "base_range": self.base_range.to_dict() if self.base_range is not None else self.base_range,
            "conversion_factor": self.conversion_factor,
            "id": self.id,
            "name": self.name
        }