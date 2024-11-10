from src.errors.validator import Validator
from src.core.abstract_logic import abstract_logic
from src.core.evet_type import event_type
from src.logics.observe_service import observe_service
from src.dto.filter import filter
from src.logics.filter_prototype import filter_prototype
from src.reports.json_deserializer import json_deserializer
from src.models.nomenclature import nomenclature_model
from src.data_reposity import data_reposity
from src.manager.settings_manager import settings_manager
from src.processors.turnover_process import turnover_process
from src.manager.date_block_manager import date_block_manager
from flask import abort
import os

"""
Класс для работы с рецептами
"""
class turnover_service(abstract_logic):
    __settings_manager: settings_manager = None

    def __init__(self, manager: settings_manager):
        Validator.validate_type("manager", manager, settings_manager)
        self.__settings_manager = manager

        observe_service.append(self)

    def change_turnover(self, nomenclature: dict, data: dict) -> None:
        Validator.validate_type("nomenclature", nomenclature, dict)
        Validator.validate_type("data", data, dict)

        deserializer = json_deserializer(nomenclature_model)
        if not deserializer.open("", [nomenclature]):
            return abort(400)
        
        Validator.validate_empty_argument("model_objects", deserializer.model_objects)
        Validator.validate_type("model_objects[0]", deserializer.model_objects[0], nomenclature_model)
        nomenclature: nomenclature_model = deserializer.model_objects[0]

        nom_filter = filter.create({"id": nomenclature.id})

        prototype = filter_prototype(data[data_reposity.nomenclature_key()])
        prototype.create(nom_filter)

        if not prototype.data:
            return abort(400)
        
        # Изменяем в оборотах
        path = os.path.join(
            self.__settings_manager.current_settings.json_folder,
            turnover_process(self.__settings_manager).file_name
        )
        turnovers = date_block_manager.read(path)

        for key in turnovers.keys():
            if nomenclature.id in key:
                turnovers[key].nomenclature = nomenclature
                break

        date_block_manager.write(path, turnovers, self.__settings_manager)

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def handle_event(self, type: event_type, **kwargs):
        super().handle_event(type, **kwargs)

        if type == event_type.CHANGE_NOMENCLATURE:
            data = kwargs.get("data")
            Validator.validate_not_none("data", data)

            nomenclature = kwargs.get("nomenclature")
            Validator.validate_not_none("nomenclature", nomenclature)

            return self.change_turnover(nomenclature, data)