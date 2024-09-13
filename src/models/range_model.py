from src.abstract_reference import abstract_reference

"""
Модель единицы измерения
"""
class range(abstract_reference):

    def __init__(self, unit_name: str = "грамм", conversion_factor: int = 1, base_range: range = None):
        super().__init__()
        if base_range is not None and base_range.conversion_factor > conversion_factor:
            raise TypeError("Некорректно передан параметр!")
        if not isinstance(unit_name, str) or not isinstance(conversion_factor, int):
            raise TypeError("Некорректно передан параметр!")
        self.unit_name = unit_name
        self.conversion_factor = conversion_factor
        self.base_range = base_range

    """
    Режим сравнения (по наименованию)
    """
    def equal(self, other) -> bool:
        if other is None: return False
        if not isinstance(other, range): return False
        return self.name == other.name
    
    def unequal(self, other) -> bool:
        return self.name != other.name