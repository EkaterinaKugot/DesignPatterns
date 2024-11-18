from src.core.abstract_logic import abstract_logic
from src.core.evet_type import event_type
from src.models.group import group_model
from src.models.range import range_model
from src.models.nomenclature import nomenclature_model
from src.models.recipe import recipe_model
from src.models.storage import storage_model
from src.models.transaction import transaction_model

"""
Репозиторий
"""
class data_reposity(abstract_logic):
    __data = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(data_reposity, cls).__new__(cls)
        return cls.instance 

    """
    Набор данных
    """
    @property
    def data(self):
        return self.__data

    """
    Ключ для хранения груп номенклатур
    """
    @staticmethod
    def group_key() -> str:
        return "group"
    
    """
    Ключ для хранения номенклатур
    """
    @staticmethod
    def nomenclature_key() -> str:
        return "nomenclature"
    
    """
    Ключ для хранения единиц измерения
    """
    @staticmethod
    def range_key() -> str:
        return "range"
    
    """
    Ключ для хранения рецептов
    """
    @staticmethod
    def recipe_key() -> str:
        return "recipe"
    
    """
    Ключ для хранения складов
    """
    @staticmethod
    def storage_key() -> str:
        return "storage"
    
    """
    Ключ для хранения транзакций
    """
    @staticmethod
    def transaction_key() -> str:
        return "transaction"
    
    """
    Перегрузка абстрактного метода
    """
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def handle_event(self, type: event_type, **kwargs):
        super().handle_event(type, **kwargs)

    """
    Получить список всех ключей
    """
    @staticmethod
    def keys() -> list:
        result = []
        methods = [method for method in dir(data_reposity) if
                    callable(getattr(data_reposity, method)) and method.endswith('_key')]
        for method in methods:
            key = getattr(data_reposity, method)()
            result.append(key)

        return result
    
    """
    Получить список всех ключей и моделей
    """
    @staticmethod
    def keys_and_models() -> dict:
        return {
            data_reposity.group_key(): group_model,
            data_reposity.nomenclature_key(): nomenclature_model,
            data_reposity.range_key(): range_model,
            data_reposity.recipe_key(): recipe_model,
            data_reposity.storage_key(): storage_model,
            data_reposity.transaction_key(): transaction_model,
        }