from abc import ABC, abstractmethod
from src.errors.validator import Validator
from src.models.transaction import transaction_model
from src.logics.transaction_service import transaction_service
from src.models.turnover import turnover_model
from src.manager.settings_manager import settings_manager


"""
Абстрактный класс для процессов транзакции
"""
class abstract_processor:
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
    
    @abstractmethod
    def processor(self, transactions: list[transaction_model]):
        pass

    def calc_turnover(self, turnovers: dict, transaction: transaction_model) -> None:
        quantity = 0
        turnover_exists = False 
        current_key = (transaction.storage.id, transaction.nomenclature.id)
        if current_key in turnovers.keys():
            quantity = turnovers[current_key].turnover
            turnover_exists = True
            
        cond_transaction = transaction_service(transaction.type_transaction)
        quantity = cond_transaction.transaction(quantity, transaction.quantity)
            
        if turnover_exists:
            turnovers[current_key].turnover = int(quantity)
        else:
            turnover = turnover_model.create(transaction.storage, int(quantity), transaction.nomenclature, transaction.range)
            turnovers[current_key] = turnover