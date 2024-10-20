from src.core.abstract_prototype import abstract_prototype
from src.dto.filter import filter
from src.errors.validator import Validator
from src.core.abstract_report import abstract_report
from src.dto.filtering_type import filtering_type
from src.dto.type_filter import type_filter


class models_prototype(abstract_prototype):

    def __init__(self, source: list) -> None:
        super().__init__(source)

    def create(self, data: list, filterDto: filter) -> 'models_prototype':
        Validator.validate_type("data", data, list)
        Validator.validate_type("filterDto", filterDto, filter)

        self.data = self.filter_name_id(filterDto.name, filterDto.type_filter_name)
        self.data = self.filter_name_id(filterDto.id, filterDto.type_filter_id, "id")
        instance = models_prototype(self.data)
        return instance
    
    """
    Фильтрация по имени и id
    """
    def filter_name_id(self, filterDto_arg: str, filterDto_type: type_filter, name_attr: str = "name") -> list:
        if filterDto_arg is None or filterDto_arg == "":
            return self.data
        
        result = []
        filt = filtering_type(filterDto_type)
        for item in self.data:
            item_names = self.__defining_list_data_compare(item, name_attr)
            for item_name in item_names:
                if filt.filtration(filterDto_arg, str(item_name)):
                    result.append(item)

        return result
    
    """
    Определяем список элементов для сравнения
    """
    def __defining_list_data_compare(self, item, name_attr: str = "name") -> list:
        Validator.validate_type("name_attr", name_attr, str)
        Validator.validate_empty_argument("name_attr", name_attr)

        attribute = abstract_report.get_class_fields(item)
        attribute_class: dict = item.attribute_class
        if len(attribute_class) != 0:
            for key, value in attribute_class.items():
                if isinstance(item, value) and getattr(item, key) is not None:
                    return [getattr(item, name_attr), getattr(getattr(item, key), name_attr)]
                
        if "full_name" in attribute and name_attr == "name":
            return [getattr(item, "full_name")]
        else:
            return [getattr(item, name_attr)]