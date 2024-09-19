from src.core import abstract_logic

"""
Репозиторий
"""
class data_reposity(abstract_logic):
    __data = []

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(data_reposity, cls).__new__(cls)
        return cls.instance 

    @property
    def data(self):
        return self.__data

    """
    Ключ для хранения груп номенклатур
    """
    @staticmethod
    def group_key() -> str:
        return "group"