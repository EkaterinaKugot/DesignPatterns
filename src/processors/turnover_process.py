from src.core.abstract_processor import abstract_processor
from src.models.transaction import transaction_model
from src.errors.validator import Validator
from src.manager.settings_manager import settings_manager
from src.reports.json_deserializer import json_deserializer
from src.models.turnover import turnover_model
from src.core.abstract_logic import abstract_logic
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

        # Рассчитываем обороты после date_block
        turnovers: dict = {}
        if os.path.exists(path):
            deserializer = json_deserializer(turnover_model)
            deserializer.open(self.file_name)
            turnovers = {(tur.storage.id, tur.nomenclature.id): tur for tur in deserializer.model_objects}
        
        for transaction in transactions:
            if transaction.period > date_block:
                self.calc_turnover(turnovers, transaction)

        return turnovers