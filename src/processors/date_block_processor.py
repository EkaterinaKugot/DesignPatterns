from src.core.abstract_processor import abstract_processor
from src.models.transaction import transaction_model
from src.errors.validator import Validator
from src.manager.settings_manager import settings_manager
from src.reports.report_factory import report_factory
from src.core.format_reporting import format_reporting
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
                self.calc_turnover(turnovers, transaction)

        path = os.path.join(self.settings_manager.current_settings.json_folder, self.file_name)

        result = []
        if len(turnovers.values()) == 0:
            os.remove(path)
        else:
            report = report_factory(self.settings_manager).create(format_reporting.JSON)
            report.create(list(turnovers.values()))
            result = report.result

        try:
            if len(result) != 0:
                with open(path , 'w', encoding='utf-8') as f:
                    f.write(result)
            return True
        except:
            pass

        return False