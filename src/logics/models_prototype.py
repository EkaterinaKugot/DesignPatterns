from src.core.abstract_prototype import abstract_prototype
from src.dto.filter import filter
from src.errors.validator import Validator
from src.core.abstract_report import abstract_report
from src.dto.filtering_type import filtering_type


class models_prototype(abstract_prototype):

    def __init__(self, source: list) -> None:
        super().__init__(source)

    def create(self, data: list, filterDto: filter):
        Validator.validate_type("data", data, list)
        Validator.validate_type("filterDto", filterDto, filter)

        self.data = self.filter_name(filterDto)
        self.data = self.filter_id(filterDto)
        instance = models_prototype(self.data)
        return instance
    
    def filter_name(self, filterDto: filter) -> list:
        if filterDto.name is None or filterDto.name == "":
            return self.data
        
        result = []
        for item in self.data:
            item_names = self.__defining_list_data_compare(item)

            filt = filtering_type(filterDto.type_filter_name)
            for item_name in item_names:
                if filt.filtration(filterDto.name, item_name):
                    result.append(item)

        return result

    def __defining_list_data_compare(self, item, name_attr: str = "name"):
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
        
    
    def filter_id(self, filterDto: filter) -> list:
        if filterDto.id is None or filterDto.id == "":
            return self.data
        
        result = []
        filt = filtering_type(filterDto.type_filter_id)
        for item in self.data:
            item_ids = self.__defining_list_data_compare(item, "id")
            for item_id in item_ids:
                if filt.filtration(filterDto.id, str(item_id)):
                    result.append(item)

        return result