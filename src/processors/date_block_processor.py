from src.core.abstract_processor import abstract_processor
from src.models.transaction import transaction_model
from src.errors.validator import Validator
from src.manager.settings_manager import settings_manager
from src.processors.calculation_process import calculation_process
from src.manager.date_block_manager import date_block_manager
from datetime import datetime
import os

class date_block_processor(abstract_processor):
    __process_start_date: datetime = datetime(1900, 1, 1)

    def __init__(self, manager: settings_manager) -> None:
        super().__init__(manager)

    """
    Дата начала расчета всех оборотов
    """
    @property
    def process_start_date(self) -> datetime:
        return self.__process_start_date
    
    """
    Переопределение метода расчета оборотов до даты блокировки
    """
    def processor(self, transactions: list[transaction_model]) -> bool:
        date_block = self.settings_manager.current_settings.date_block
        Validator.validate_not_none("date_block", date_block)
        Validator.validate_more_permissible_value("date_block", date_block, self.process_start_date)

        turnovers: dict = {}
        for transaction in transactions:
            if self.process_start_date <= transaction.period <= date_block:
                calculation_process.processor(turnovers, transaction)

        path = os.path.join(self.settings_manager.current_settings.json_folder, self.file_name)

        if date_block_manager.write(path, turnovers, self.settings_manager):
            return True
        else:
            return False
