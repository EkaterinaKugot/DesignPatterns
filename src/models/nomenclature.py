from src.core.base_model import base_model_id
from src.models.group import group_model
from src.models.range import range_model
from src.errors.validator import Validator

class nomenclature_model(base_model_id):
    __full_name: str = ""
    __group: group_model = None
    __range: range_model = None

    @property
    def full_name(self) -> str:
        return self.__full_name
    
    @full_name.setter
    def full_name(self, full_name: str):
        Validator.validate_type("full_name", full_name, str)
        Validator.validate_permissible_length("full_name", full_name, 255)
        self.__full_name = full_name.strip()

    """
    Группа номенклатуры
    """
    @property
    def group(self) -> group_model:
        return self.__group
    
    @group.setter
    def group(self, group: group_model):
        Validator.validate_type("group", group, group_model)
        self.__group = group

    """
    Единица измерения
    """
    @property
    def range(self) -> range_model:
        return self.__range
    
    @range.setter
    def range(self, range: range_model):
        Validator.validate_type("range", range, range_model)
        self.__range = range