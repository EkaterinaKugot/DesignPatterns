from src.core.abstract_processor import abstract_processor
from src.models.transaction import transaction_model
from src.errors.validator import Validator
from src.manager.settings_manager import settings_manager
from src.processors.calculation_process import calculation_process
from src.manager.date_block_manager import date_block_manager
import os

class turnover_process(abstract_processor):

    def __init__(self, manager: settings_manager) -> None:
        super().__init__(manager)

    """
    Переопределение метода расчета оборотов
    """
    def processor(self, transactions: list[transaction_model]) -> dict:
        date_block = self.settings_manager.current_settings.date_block
        Validator.validate_not_none("date_block", date_block)
        path = os.path.join(self.settings_manager.current_settings.json_folder , self.file_name) 

        # Получаем оброты до date_block
        turnovers: dict = date_block_manager.read(path)
        print(turnovers)
        
        # Рассчитываем обороты после date_block
        for transaction in transactions:
            if transaction.period > date_block:
                calculation_process.processor(turnovers, transaction)

        return turnovers