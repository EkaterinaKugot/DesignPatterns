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
    Переопределения метода для создания turnover_process
    """
    def create(data: dict = None) -> 'turnover_process':
        start_period = None
        end_period = None
        
        if data is not None:
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
            pass

        turnover_p = turnover_process()
        turnover_p.start_period = start_period
        turnover_p.end_period = end_period
        return turnover_p

    """
    Переопределение метода расчета оборотов
    """
    def processor(self, transactions: list[transaction_model]) -> list:
        turnovers: list[turnover_model] = [] 
        for transaction in transactions:
            if self.start_period <= transaction.period <= self.end_period:
                quantity = 0
                idx = -1
                for i, tur in enumerate(turnovers):
                    if transaction.nomenclature == tur.nomenclature and \
                        transaction.storage == tur.storage:
                        quantity = tur.turnover
                        idx = i
                        break
                
                cond_transaction = transaction_service(transaction.type_transaction)
                quantity = cond_transaction.transaction(quantity, transaction.quantity)
                if idx != -1:
                    turnovers[idx].turnover = int(quantity)
                else:
                    turnover = turnover_model.create(transaction.storage, int(quantity), transaction.nomenclature, transaction.range)
                    turnovers.append(turnover)

        return turnovers