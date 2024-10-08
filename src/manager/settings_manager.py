import json
import glob
from src.models.settings import settings
from src.core.abstract_logic import abstract_logic
from src.errors.validator import Validator
from src.core.abstract_report import abstract_report
from src.core.format_reporting import format_reporting
from src.reports.csv_report import csv_report
from src.reports.md_report import md_report
from src.reports.json_report import json_report
from src.reports.xml_report import xml_report
from src.reports.rtf_report import rtf_report

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

    @property
    def format_to_class(self) -> dict:
        return self.__format_to_class

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance
    
    def convert(self) -> bool:
        path = f"./**/{self.__file_name}"
        full_name = glob.glob(path, recursive=True)[0]
        with open(full_name) as stream:
            data = json.load(stream)
        
        fields = dir(self.__settings)
        for key in data.keys():
            if key in fields:
                self.__settings.__setattr__(key, data[key])
            else:
                self.set_exception(f"Неожиданный ключ {key} со значением {data[key]}.")
        return True


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
        _settings.type_property = "lalal"
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