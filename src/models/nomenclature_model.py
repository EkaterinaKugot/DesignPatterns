from src.abstract_reference import abstract_reference
from src.models.group_nomenclature_model import group_nomenclature
from src.models.range_model import range
from src.errors.validator import Validator

class nomenclature(abstract_reference):
    __full_name: str = ""
    __group_nomenclature: group_nomenclature = group_nomenclature()
    __range: range = range("кг", 1000, range("грамм", 1))

    @property
    def full_name(self) -> str:
        return self.__full_name
    
    @full_name.setter
    def full_name(self, full_name: str):
        Validator.validate_type("full_name", full_name, str)
        Validator.validate_permissible_length("full_name", full_name, 255)
        self.__full_name = full_name.strip()

    @property
    def group_nomenclature(self) -> group_nomenclature:
        return self.__group_nomenclature
    
    @group_nomenclature.setter
    def group_nomenclature(self, group_nomenclature):
        self.__group_nomenclature = group_nomenclature

    @property
    def range(self) -> range:
        return self.__range
    
    @range.setter
    def range(self, range):
        self.__range = range
    
    """
    Режим сравнения (по id)
    """
    def __eq__(self, other) -> bool:
        return super().__eq__(other)
    
    def __ne__(self, other) -> bool:
        return super().__ne__(other)