from src.core.base_model import base_model_name
from src.errors.validator import Validator

"""
Модель единицы измерения
"""
class range_model(base_model_name):
    __unit_name: str = "гр"
    __conversion_factor: int = 1
    __base_range: range = None

    """
    Имя единицы измерения
    """
    @property
    def unit_name(self) -> str:
        return self.__unit_name
    
    @unit_name.setter
    def unit_name(self, unit_name: str):
        Validator.validate_type("unit_name", unit_name, str)
        self.__unit_name = unit_name

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
    def create(unit_name: str, conversion_factor: int, base_range: 'range_model' = None) -> 'range_model':
        item = range_model()
        item.unit_name = unit_name
        item.conversion_factor = conversion_factor
        if base_range is not None:
            Validator.validate_permissible_value("base_range", base_range.conversion_factor, conversion_factor)
            item.base_range = base_range
            
        return item


    # def __init__(self, unit_name: str = "гр", conversion_factor: int = 1, base_range: range = None):
    #     super().__init__()
    #     if base_range is not None:
    #         Validator.validate_permissible_value("base_range", base_range.conversion_factor, conversion_factor)
    #     Validator.validate_type("unit_name", unit_name, str)
    #     Validator.validate_type("conversion_factor", conversion_factor, int)
    #     self.unit_name = unit_name
    #     self.conversion_factor = conversion_factor
    #     self.base_range = base_range