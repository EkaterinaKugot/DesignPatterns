from src.dto.filter import filter
from src.errors.validator import Validator
from src.core.filter_type import filter_type

"""
Класс для сравнения элементов модели и данных из фильтра
"""
class filter_service:

    def __init__(self, type_filter_element: filter_type):
        Validator.validate_type("type_filter_element", type_filter_element, filter_type)
        self.filtration = getattr(self, type_filter_element.value.lower())

    def equale(self, first_arg: str, second_arg: str) -> bool:
        Validator.validate_type("first_arg", first_arg, str)
        Validator.validate_type("second_arg", second_arg, str)

        return first_arg == second_arg
    
    def like(self, part_element: str, element: str) -> bool:
        Validator.validate_type("part_element:", part_element, str)
        Validator.validate_type("element", element, str)

        return part_element in element