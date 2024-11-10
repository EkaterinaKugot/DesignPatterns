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
from flask import abort
import os

"""
Класс для работы с номенклатурами
"""
class nomenclature_service(abstract_logic):
    __settings_manager: settings_manager = None

    def __init__(self, manager: settings_manager):
        Validator.validate_type("manager", manager, settings_manager)
        self.__settings_manager = manager

        observe_service.append(self)

    @staticmethod
    def get_nomenclature(data: list, id: str) -> list:
        Validator.validate_type("data", data, list)

        item_filter = filter.create({"id": id})

        prototype = filter_prototype(data)
        prototype.create(item_filter)
        
        return prototype.data
    
    @staticmethod
    def put_nomenclature(new_nomenclature: dict, data: dict) -> list[bool, nomenclature_model]:
        Validator.validate_type("new_nomenclature", new_nomenclature, dict)
        Validator.validate_type("data", data, dict)

        nom_data = data[data_reposity.nomenclature_key()]

        deserializer = json_deserializer(nomenclature_model)
        if not deserializer.open("", [new_nomenclature]):
            return abort(400)
        
        Validator.validate_empty_argument("model_objects", deserializer.model_objects)
        Validator.validate_type("model_objects[0]", deserializer.model_objects[0], nomenclature_model)
        nomenclature: nomenclature_model = deserializer.model_objects[0]

        # Проверяем, есть ли номенклатура с таким же именем и единицой измерения
        name_filter = filter.create({"name": nomenclature.full_name})
        range_filter = filter.create({"id": nomenclature.range.id}, "range")

        prototype = filter_prototype(nom_data)
        prototype.create(name_filter)
        prototype.create(range_filter)

        # Если нет такой номенлатуры, то добавляем
        if not prototype.data:
            data[data_reposity.nomenclature_key()].append(nomenclature)
            print(nomenclature.full_name)
            return False
        
        return True
    
    @staticmethod
    def delete_nomenclature(nomenclature: dict, data: list) -> bool:
        Validator.validate_type("nomenclature", nomenclature, dict)
        Validator.validate_type("data", data, list)

        deserializer = json_deserializer(nomenclature_model)
        if not deserializer.open("", [nomenclature]):
            return abort(400)
        
        Validator.validate_empty_argument("model_objects", deserializer.model_objects)
        Validator.validate_type("model_objects[0]", deserializer.model_objects[0], nomenclature_model)
        nomenclature: nomenclature_model = deserializer.model_objects[0]

        nom_filter = filter.create({"id": nomenclature.id})

        prototype = filter_prototype(data)
        prototype.create(nom_filter)

        # Если номенлатура есть, то блокируем удаление
        if prototype.data:
            return True
        
        return abort(400)
    
    def change_nomenclature(self, nomenclature: dict, data: dict) -> None:
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
        
        # Изменяем в номенклатурах
        for i, nom in enumerate( data[ data_reposity.nomenclature_key() ] ):
            if nom.id == nomenclature.id:
                data[data_reposity.nomenclature_key()][i] = nomenclature
                break
        

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def handle_event(self, type: event_type, **kwargs):
        super().handle_event(type, **kwargs)

        if type == event_type.DELETE_NOMENCLATURE:
            data = kwargs.get("data")
            Validator.validate_not_none("data", data)

            nomenclature = kwargs.get("nomenclature")
            Validator.validate_not_none("nomenclature", nomenclature)

            self.delete_nomenclature(nomenclature, data)
        elif type == event_type.CHANGE_NOMENCLATURE:
            data = kwargs.get("data")
            Validator.validate_not_none("data", data)

            nomenclature = kwargs.get("nomenclature")
            Validator.validate_not_none("nomenclature", nomenclature)

            self.change_nomenclature(nomenclature, data)