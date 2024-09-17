from src.abstract_reference import abstract_reference
from src.errors.validator import Validator

"""
Модель единицы измерения
"""
class range(abstract_reference):

    def __init__(self, unit_name: str = "грамм", conversion_factor: int = 1, base_range: range = None):
        super().__init__()
        if base_range is not None:
            Validator.validate_permissible_value("base_range ", base_range.conversion_factor, conversion_factor)
        Validator.validate_type("unit_name", unit_name, str)
        Validator.validate_type("conversion_factor", conversion_factor, int)
        self.unit_name = unit_name
        self.conversion_factor = conversion_factor
        self.base_range = base_range

    """
    Режим сравнения (по наименованию)
    """
    def __eq__(self, other) -> bool:
        if other is None: return False
        if not isinstance(other, range): return False
        return self.name == other.name
    
    def __ne__(self, other) -> bool:
        return self.name != other.name