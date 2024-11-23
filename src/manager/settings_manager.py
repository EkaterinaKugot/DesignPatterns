import json
from src.models.settings import settings
from src.core.abstract_logic import abstract_logic
from src.errors.validator import Validator
from src.errors.custom_exception import FileWriteException
from src.core.abstract_report import abstract_report
from src.core.format_reporting import format_reporting
from src.reports.csv_report import csv_report
from src.reports.md_report import md_report
from src.reports.json_report import json_report
from src.reports.xml_report import xml_report
from src.reports.rtf_report import rtf_report
from src.core.evet_type import event_type
from src.logics.observe_service import observe_service
from src.core.logging_type import logging_type
from datetime import datetime

"""
Менеджер настроек
"""
class settings_manager(abstract_logic):
    __file_name = "settings.json"
    __settings: settings = settings()
    __format_to_class = {
        "CSV": csv_report,
        "MARKDOWN": md_report,
        "JSON": json_report,
        "XML": xml_report,
        "RTF": rtf_report
    }

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance
    
    def __init__(self) -> None:
        observe_service.append(self)
    
    def convert(self) -> bool:
        data = self.open_settings_json()
        
        fields = dir(self.__settings)
        for key in data.keys():
            if key in fields:
                self.__settings.__setattr__(key, data[key])
            else:
                self.set_exception(f"Неожиданный ключ {key} со значением {data[key]}.")
        return True

    def open_settings_json(self):
        full_name = self.file_search(self.__file_name)

        with open(full_name, encoding='utf-8') as stream:
            data = json.load(stream)
        return data

    def change_settings_json(self, data: dict) -> bool:
        full_name = self.file_search(self.__file_name)
        data = json.dumps(data)

        try:
            with open(full_name, 'w', encoding='utf-8') as f:
                f.write(data)
            return True
        except:
            return False
        

    def open(self, file_name: str = "") -> bool:
        Validator.validate_type("file_name", file_name, str)
        
        if file_name != "":
            self.__file_name = file_name

        try:
            return self.convert()
        except Exception as ex:
            self.__settings = self.__default_setting()
            self.set_exception(ex)
            return False
    
    """
    Загруженные настройки
    """
    @property
    def current_settings(self) -> settings:
        return self.__settings
    
    @property
    def format_to_class(self) -> dict:
        return self.__format_to_class
    
    """
    Набор настроек по умолчанию
    """
    def __default_setting(self) -> settings:
        _settings = settings()
        _settings.inn = "380080920202"
        _settings.organization_name = "Рога и копыта (default)"
        _settings.account = "11127400937"
        _settings.сorrespondent_account = "86127390170"
        _settings.bik = "662817992"
        _settings.type_property = "ИП"
        _settings.date_block = datetime(2024, 1, 1)
        _settings.min_log_level = logging_type.DEBUG
        return _settings
    
    def get_report_class(self, format: format_reporting = None) -> abstract_report:
        if format is None:
            format = self.__settings.report_format

        Validator.validate_type("format", format, format_reporting)
        report_class = self.format_to_class.get(format.name, None)
        Validator.validate_not_none("report_class", report_class)

        return report_class()
    
    
    
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def handle_event(self, type: event_type, **kwargs):
        super().handle_event(type, **kwargs)

        if type == event_type.CHANGE_DATE_BLOCK:
            new_date_block = kwargs.get("date_block")
            Validator.validate_not_none("new_date_block", new_date_block)

            self.current_settings.date_block = new_date_block

            # Сохраняем date_block в settings.json
            set_data = self.open_settings_json()
            set_data["date_block"] = datetime.timestamp(new_date_block)

            if not self.change_settings_json(set_data):
                FileWriteException("set_data", self.__file_name)
        elif type == event_type.SAVE_DATA_REPOSITY:
            self.current_settings.first_start = False

            # Изменяем first_start в settings.json
            set_data = self.open_settings_json()
            set_data["first_start"] = self.current_settings.first_start

            if not self.change_settings_json(set_data):
                FileWriteException("set_data", self.__file_name)