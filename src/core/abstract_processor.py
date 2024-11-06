from abc import ABC, abstractmethod
from src.errors.validator import Validator
from src.models.transaction import transaction_model
from src.manager.settings_manager import settings_manager


"""
Абстрактный класс для процессов транзакции
"""
class abstract_processor(ABC):
    __file_name: str = "turnover_until_date_block.json"
    __settings_manager: settings_manager = None

    def __init__(self, manager: settings_manager) -> None:
        Validator.validate_type("manager", manager, settings_manager)
        self.__settings_manager = manager

    @property
    def settings_manager(self) -> settings_manager:
        return self.__settings_manager

    """
    Имя файла с расчитанными оборотами до date_block
    """
    @property
    def file_name(self) -> str:
        return self.__file_name
    
    @file_name.setter
    def file_name(self, file_name: str):
        Validator.validate_type("file_name", file_name, str)
        self.__file_name = file_name
    
    @abstractmethod
    def processor(self, transactions: list[transaction_model]):
        pass