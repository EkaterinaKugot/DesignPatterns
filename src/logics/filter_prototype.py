from src.core.abstract_prototype import abstract_prototype
from src.dto.filter import filter
from src.errors.validator import Validator
from src.core.abstract_report import abstract_report
from src.logics.filter_service import filter_service
from src.core.filter_type import filter_type

"""
Класс для фильтрации данных
"""
class filter_prototype(abstract_prototype):

    def __init__(self, source: list) -> None:
        super().__init__(source)

    """
    Переопределение метода для фильтрации по name и id
    """
    def create(self, filterDto: filter) -> 'filter_prototype':
        Validator.validate_type("filterDto", filterDto, filter)

        self.data = self.__filter_name_id(filterDto.name, filterDto.type_filter_name, "name", filterDto.model)
        self.data = self.__filter_name_id(filterDto.id, filterDto.type_filter_id, "id", filterDto.model)
        self.data = self.__filter_period(filterDto.period)
        instance = filter_prototype(self.data)
        return instance
    
    """
    Фильтрация по имени и id
    """
    def __filter_name_id(
        self, 
        filterDto_arg: str, 
        filterDto_type: filter_type, 
        name_attr: str = "name",
        filterDto_model: str = "",
    ) -> list:
        if filterDto_arg is None or filterDto_arg == "":
            return self.data
        
        result = []
        if filterDto_model is None or len(filterDto_model) == 0:
            result = self.__filter_model(filterDto_arg, filterDto_type, name_attr)
        else:
            result = self.__filter_internal_model(filterDto_arg, filterDto_type, name_attr, filterDto_model)

        return result
    
    def __filter_period(self, filterDto_period: list):
        if filterDto_period is None or len(filterDto_period) != 2:
            return self.data
        
        result = []
        for item in self.data:
            if filterDto_period[0] <= item.period <= filterDto_period[1]:
                result.append(item)
        return result

    """
    Фильтрация по имени и id текущей модели
    """
    def __filter_model(self, filterDto_arg: str, filterDto_type: filter_type, name_attr: str):
        result = []
        filt = filter_service(filterDto_type)
        for item in self.data:
            item_names = self.__defining_list_data_compare(item, name_attr)
            for item_name in item_names:
                if filt.filtration(filterDto_arg, str(item_name)):
                    result.append(item)
        return result
    
    """
    Фильтрация по имени и id внутренней модели
    """
    def __filter_internal_model(self, filterDto_arg: str, filterDto_type: filter_type, name_attr: str, filterDto_model: str):
        result = []
        # Проверяем, что модель, по которой нужно отфильтровать, есть
        if len(self.data) == 0:
            return result
        
        first_model = self.data[0]
        attribute_class = first_model.attribute_class

        if filterDto_model not in attribute_class.keys():
            return self.data
        
        # Фильтруем
        type_internal_model = attribute_class[filterDto_model]
        filt = filter_service(filterDto_type)
        for item in self.data:
            internal_model = getattr(item, filterDto_model)
            if isinstance(internal_model, type_internal_model):
                item_names = self.__defining_list_data_compare(internal_model, name_attr)
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