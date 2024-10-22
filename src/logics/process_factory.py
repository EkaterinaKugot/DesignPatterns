from src.core.abstract_processor import abstract_processor
from src.core.transaction_type import transaction_type
from src.models.transaction import transaction_model
from src.models.turnover import turnover_model
from src.logics.transaction_service import transaction_service
from src.errors.validator import Validator
from datetime import datetime, timedelta

class turnover_process(abstract_processor):
    __start_period: datetime = None
    __end_period: datetime = None
    __turnovers: list[turnover_model] = []

    def __init__(self, start_period: datetime = None, end_period: datetime = None):
        if start_period is None:
            start_period = datetime(2024, 1, 1)
        if end_period is None:
            end_period = datetime.now() + timedelta(minutes=1)
        self.start_period = start_period
        self.end_period = end_period
        self.turnovers = []

    """
    Начало периода
    """
    @property
    def start_period(self) -> datetime:
        return self.__start_period
    
    @start_period.setter
    def start_period(self, start_period: datetime):
        Validator.validate_type("start_period", start_period, datetime)
        self.__start_period = start_period

    """
    Конец периода
    """
    @property
    def end_period(self) -> datetime:
        return self.__end_period
    
    @end_period.setter
    def end_period(self, end_period: datetime):
        Validator.validate_type("end_period", end_period, datetime)
        self.__end_period = end_period

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
            if self.start_period <= transaction.period <= self.end_period:
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