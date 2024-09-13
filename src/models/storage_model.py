from src.abstract_reference import abstract_reference

class storage(abstract_reference):
    """
    Режим сравнения (по id)
    """
    def equal(self, other) -> bool:
        return super().equal(other)
    
    def unequal(self, other) -> bool:
        return super().unequal(other)