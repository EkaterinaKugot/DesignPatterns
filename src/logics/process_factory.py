from src.core.abstract_processor import abstract_processor
from src.models.transaction import transaction_model
from src.models.turnover import turnover_model
from src.logics.transaction_service import transaction_service
from src.errors.validator import Validator
from src.errors.custom_exception import ArgumentException
from datetime import datetime, timedelta

class turnover_process(abstract_processor):
    __start_period: datetime = None
    __end_period: datetime = None
    __turnovers: list[turnover_model] = []   

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

    @staticmethod
    def create(data: dict) -> 'turnover_process':
        start_period = data.get("start_period")
        end_period = data.get("end_period")

        if start_period is None:
            start_period = datetime(2024, 1, 1)
        if end_period is None:
            end_period = datetime.now() + timedelta(minutes=1)

        try:
            start_period = datetime.strptime(start_period, "%Y-%m-%dT%H:%M:%SZ")
            end_period = datetime.strptime(end_period, "%Y-%m-%dT%H:%M:%SZ")
        except:
            ArgumentException("start_period", start_period)
            ArgumentException("end_period", end_period)

        turnover_p = turnover_process()
        turnover_p.start_period = start_period
        turnover_p.end_period = end_period
        turnover_p.turnovers = []
        return turnover_p

    """
    Переопределение метода расчета оборотов
    """
    def processor(self, transactions: list[transaction_model]) -> list:
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
                
                cond_transaction = transaction_service(transaction.type_transaction)
                quantity = cond_transaction.transaction(quantity, transaction.quantity)
                if idx != -1:
                    self.turnovers[idx].turnover = int(quantity)
                else:
                    turnover = turnover_model.create(transaction.storage, int(quantity), transaction.nomenclature, transaction.range)
                    self.turnovers.append(turnover)

        return self.turnovers