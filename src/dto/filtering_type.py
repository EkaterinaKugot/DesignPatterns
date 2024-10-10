from src.dto.filter import filter
from src.errors.validator import Validator
from src.dto.type_filter import type_filter

class filtering_type:

    def __init__(self, type_filter_element: type_filter):
        Validator.validate_type("type_filter_element", type_filter_element, type_filter)
        self.filtration = getattr(self, type_filter_element.value.lower())

    @property
    def methods(self) -> list:
        return self.__methods

    def equale(self, first_arg: str, second_arg: str):
        Validator.validate_type("first_arg", first_arg, str)
        Validator.validate_type("second_arg", second_arg, str)

        return first_arg == second_arg
    
    def like(self, part_element: str, element: str):
        Validator.validate_type("part_element:", part_element, str)
        Validator.validate_type("element", element, str)

        return part_element in element