from src.core.base_model import base_model_name
from src.errors.validator import Validator

"""
Модель единицы измерения
"""
class range_model(base_model_name):

    def __init__(self, unit_name: str = "грамм", conversion_factor: int = 1, base_range: range = None):
        super().__init__()
        if base_range is not None:
            Validator.validate_permissible_value("base_range ", base_range.conversion_factor, conversion_factor)
        Validator.validate_type("unit_name", unit_name, str)
        Validator.validate_type("conversion_factor", conversion_factor, int)
        self.unit_name = unit_name
        self.conversion_factor = conversion_factor
        self.base_range = base_range