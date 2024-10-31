from src.core.abstract_logic import abstract_logic
from src.reports.json_deserializer import json_deserializer
from src.models.turnover import turnover_model
from src.reports.report_factory import report_factory
from src.core.format_reporting import format_reporting
from src.manager.settings_manager import settings_manager
import os

"""
Менеджер даты блокировки
"""
class date_block_manager(abstract_logic):
    
    @staticmethod
    def read(file_path: str) -> dict:
        turnovers = {}
        if os.path.exists(file_path):
            file_name = os.path.basename(file_path)
            deserializer = json_deserializer(turnover_model)
            deserializer.open(file_name)
            turnovers = {(tur.storage.id, tur.nomenclature.id, tur.range.id): tur for tur in deserializer.model_objects}
        
        return turnovers

    @staticmethod
    def write(file_path: str, turnovers: dict, manager: settings_manager = settings_manager()) -> bool:
        result = []
        if len(turnovers.values()) == 0:
            try:
                os.remove(file_path)
            except:
                pass
        else:
            report = report_factory(manager).create(format_reporting.JSON)
            report.create(list(turnovers.values()))
            result = report.result

        try:
            if len(result) != 0:
                with open(file_path , 'w', encoding='utf-8') as f:
                    f.write(result)
            return True
        except:
            return False


    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)