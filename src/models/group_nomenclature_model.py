from src.abstract_reference import abstract_reference

class group_nomenclature(abstract_reference):
    """
    Режим сравнения (по id)
    """
    def __eq__(self, other) -> bool:
        return super().__eq__(other)
    
    def __ne__(self, other) -> bool:
        return super().__ne__(other)