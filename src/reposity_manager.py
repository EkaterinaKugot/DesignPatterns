from src.core.abstract_logic import abstract_logic
from src.reports.report_factory import report_factory
from src.core.format_reporting import format_reporting
from src.manager.settings_manager import settings_manager
from src.core.evet_type import event_type
from src.logics.observe_service import observe_service
from src.errors.custom_exception import FileWriteException
from src.errors.validator import Validator
from src.reports.json_deserializer import json_deserializer
from src.data_reposity import data_reposity
from flask import abort
import os
import json


"""
Менеджер data_reposity
"""
class reposity_manager(abstract_logic):
    __settings_manager: settings_manager = None
    __file_name: str = "data_reposity.json"

    def __init__(self, manager: settings_manager) -> None:
        super().__init__()
        Validator.validate_type("manager", manager, settings_manager)
        self.__settings_manager = manager

        observe_service.append(self)

    """
    Восстановить данные
    """
    def __restore_data(self, reposity_data: dict): 
        Validator.validate_type("reposity_data", reposity_data, dict)

        file_path = os.path.join(
            self.__settings_manager.current_settings.json_folder, self.__file_name
        )

        if os.path.exists(file_path):
            with open(file_path, encoding='utf-8') as stream:
                data_dict = json.load(stream)
            
            models = data_reposity.keys_and_models()
            for key, list in data_dict.items():
                if key in models.keys():
                    deserializer = json_deserializer(models[key])
                    deserializer.open("", data_list=list)
                    reposity_data[key] = deserializer.model_objects
        else:
            abort(400)
        print(len(reposity_data[data_reposity.nomenclature_key()]))

    """
    Сохранить данные
    """
    def __save_data(self, reposity_data: dict): 
        Validator.validate_type("reposity_data", reposity_data, dict)

        file_path = os.path.join(
            self.__settings_manager.current_settings.json_folder, self.__file_name
        )
        if os.path.exists(file_path):
            os.remove(file_path)

        result = {}
        report = report_factory(self.__settings_manager).create(format_reporting.JSON)
        for key, data in reposity_data.items():
            report.create(data)
            result[key] = json.loads(report.result)

        try:
            if len(result) != 0:
                data = json.dumps(result, indent=4, ensure_ascii=False)
                with open(file_path , 'w', encoding='utf-8') as f:
                    f.write(data)
        except:
            FileWriteException("data_reposity", self.__file_name)

    
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def handle_event(self, type: event_type, **kwargs):
        super().handle_event(type, **kwargs)

        if type == event_type.SAVE_DATA_REPOSITY:
            data = kwargs.get("data")
            Validator.validate_not_none("data", data)

            self.__save_data(data)
        elif type == event_type.RESTORE_DATA_REPOSITY:
            data = kwargs.get("data")
            Validator.validate_not_none("data", data)

            self.__restore_data(data)