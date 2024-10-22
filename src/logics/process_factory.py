from src.core.abstract_processor import abstract_processor
from src.core.transaction_type import transaction_type
from src.models.transaction import transaction_model
from src.models.turnover import turnover_model
from src.logics.transaction_service import transaction_service
from src.errors.validator import Validator
from datetime import datetime

class turnover_process(abstract_processor):
    __start_date: datetime = None
    __end_date: datetime = None
    __turnovers: list[turnover_model] = []

    def __init__(self, start_date: datetime, end_date: datetime):
        self.start_date = start_date
        self.end_date = end_date

    """
    Начало периода
    """
    @property
    def start_date(self) -> datetime:
        return self.__start_date
    
    @start_date.setter
    def start_date(self, start_date: datetime):
        Validator.validate_type("start_date", start_date, datetime)
        self.__start_date = start_date

    """
    Конец периода
    """
    @property
    def end_date(self) -> datetime:
        return self.__end_date
    
    @end_date.setter
    def end_date(self, end_date: datetime):
        Validator.validate_type("end_date", end_date, datetime)
        self.__end_date = end_date

    """
    Обороты
    """
    @property
    def turnovers(self) -> list[turnover_model]:
        return self.__turnovers
    
    @turnovers.setter
    def turnovers(self, turnovers: list[turnover_model]):
        Validator.validate_type("turnovers", turnovers, list)
        self.__turnovers = turnovers

    """
    Переопределение метода расчета оборотов
    """
    def create(self, transactions: list[transaction_model]) -> list:
        for transaction in transactions:
            if self.start_date <= transaction.period <= self.end_date:
                quantity = 0
                idx = -1
                for i, tur in enumerate(self.turnovers):
                    if transaction.nomenclature == tur.nomenclature and \
                        transaction.storage == tur.storage:
                        quantity = tur.turnover
                        idx = i
                        break
                
                cond_transaction = transaction_service(transaction_type.RECEIPT)
                quantity = cond_transaction.transaction(quantity, transaction.quantity)
                if idx != -1:
                    self.turnovers[idx].turnover = quantity
                else:
                    turnover = turnover_model.create(transaction.storage, quantity, transaction.nomenclature, transaction.range)
                    self.turnovers.append(turnover)

        return self.turnovers