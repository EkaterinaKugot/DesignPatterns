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

        # Рассчитываем обороты после date_block
        turnovers: dict = {}
        for transaction in transactions:
            if  transaction.period > date_block:
                self.calc_turnover(turnovers, transaction)

        # Получаем обороты до date_block
        turnovers_date_block = {}
        try:
            abstract_logic.file_search(self.file_name)
            deserializer = json_deserializer(turnover_model)
            deserializer.open(self.file_name)
            turnovers_date_block = {(tur.storage.id, tur.nomenclature.id): tur for tur in deserializer.model_objects}
        except:
            pass
        
        # Плюсуем обороты до date_block
        for key, item in turnovers_date_block.items():
            if key in turnovers.keys():
                turnovers[key].turnover = turnovers[key].turnover + item.turnover 
            else:
                turnovers[key] = item
        
        return turnovers