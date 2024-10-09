from src.core.abstract_prototype import abstract_prototype
from src.dto.filter import filter
from src.errors.validator import Validator
from src.core.type_filter import type_filter
from src.models.nomenclature import nomenclature_model
from src.models.range import range_model
from src.core.abstract_reference import abstract_reference


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
            if self.__comparison_name_diff_models(item, filterDto):
                result.append(item)

        return result
    
    def __comparison_name_diff_models(self, item: abstract_reference, filterDto: filter) -> True:
        
        if isinstance(item, range_model) and item.base_range is not None:
            item_names = [item.name, item.base_range.name]
        elif isinstance(item, nomenclature_model):
            item_names = [item.full_name]
        else:
            item_names = [item.name]

        for item_name in item_names:
            if filterDto.type_filter_name == type_filter.EQUALE:
                if item_name == filterDto.name:
                    return True
            elif filterDto.type_filter_name == type_filter.LIKE:
                if filterDto.name in item_name:
                    return True
        
    
    def filter_id(self, filterDto: filter) -> list:
        if filterDto.id is None or filterDto.id == "":
            return self.data
        result = []
        for item in self.data:
            if filterDto.type_filter_id == type_filter.EQUALE:
                if str(item.id) == filterDto.id:
                    result.append(item)
            elif filterDto.type_filter_id == type_filter.LIKE:
                if filterDto.id in str(item.id):
                    result.append(item)

        return result