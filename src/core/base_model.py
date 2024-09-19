from src.core.abstract_reference import abstract_reference

"""
Базовый класс для наследования с поддержкой сравнения по id
"""
class base_model_id(abstract_reference):
    def __eq__(self, other) -> bool:
        return super().__eq__(other)
    
    def __ne__(self, other) -> bool:
        return super().__ne__(other)
    
"""
Базовый класс для наследования с поддержкой сравнения по наименованию
"""   
class base_model_name(abstract_reference):
    def __eq__(self, other) -> bool:
        if other is None: return False
        if not isinstance(other, base_model_name): return False
        return self.name == other.name
    
    def __ne__(self, other) -> bool:
        return self.name != other.name