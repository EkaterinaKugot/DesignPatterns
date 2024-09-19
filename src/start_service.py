from src.core import abstract_logic
from src.data_reposity import data_reposity
from src.errors.validator import Validator
from src.models.group import group_model

class start_service(abstract_logic):
    __reposity: data_reposity = None

    def __init__(self, reposity: data_reposity) -> None:
        super.__init__()
        Validator.validate_type("reposity", reposity, data_reposity)
        self.__reposity = reposity

    def __create_nomenclature_groups(self): 
        list = [group_model.default_group_cold(), group_model.default_group_source()]
        self.__reposity.data[data_reposity.group_key()] = list

    def create(self):
        self.__create_nomenclature_groups()