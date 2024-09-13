from src.abstract_reference import abstract_reference
from src.models.group_nomenclature_model import group_nomenclature
from src.models.range_model import range

class nomenclature(abstract_reference):
    __full_name: str = ""
    __group_nomenclature: group_nomenclature = group_nomenclature()
    __range: range = range("кг", 1000, range("грамм", 1))

    @property
    def full_name(self) -> str:
        return self.__full_name
    
    @full_name.setter
    def full_name(self, full_name: str):
        if not isinstance(full_name, str) or len(full_name) > 255:
            raise TypeError("Некорректно передан параметр!")
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
    def equal(self, other) -> bool:
        return super().equal(other)
    
    def unequal(self, other) -> bool:
        return super().unequal(other)