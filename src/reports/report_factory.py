from src.core.abstract_logic import abstract_logic
from src.core.format_reporting import format_reporting
from src.core.abstract_report import abstract_report
from src.reports.csv_report import csv_report
from src.reports.md_report import md_report
from src.reports.json_report import json_report
from src.reports.xml_report import xml_report
from src.reports.rtf_report import rtf_report
from src.errors.validator import Validator
from src.manager.settings_manager import settings_manager
from src.models.settings import settings

class report_factory(abstract_logic):
    __reports: dict = {}
    __settings_manager: settings_manager = None
    __reports_setting: dict = {}

    def __init__(self, manager: settings_manager) -> None:
        super().__init__()
        self.__reports[format_reporting.CSV] = csv_report
        self.__reports[format_reporting.MARKDOWN] = md_report
        self.__reports[format_reporting.JSON] = json_report
        self.__reports[format_reporting.XML] = xml_report
        self.__reports[format_reporting.RTF] = rtf_report

        Validator.validate_type("manager", manager, settings_manager)
        self.__settings_manager = manager

    """
    Форматы из настроек
    """
    @property
    def reports_setting(self) -> dict:
        return self.__reports_setting
    
    @reports_setting.setter
    def reports_setting(self, reports_setting: dict):
        Validator.validate_type("reports_setting", reports_setting, dict)
        self.__reports_setting = reports_setting

    """
    Стандартные форматы
    """
    @property
    def reports(self) -> dict:
        return self.__reports
    
    @reports.setter
    def reports(self, reports: dict):
        Validator.validate_type("reports", reports, dict)
        self.__reports = reports

    """
    Текущие настройки
    """
    @property 
    def settings(self) -> settings:
        return self.__settings_manager.settings
    
    def load_formats_from_settings(self) -> None:
        tmp_reports_setting = {}
        for key, value in self.__settings_manager.format_to_class.items():
            try:
                tmp_reports_setting[format_reporting[key]] = value
            except Exception as ex:
                self.set_exception(ex)
        self.reports_setting = tmp_reports_setting
            

    def create(self, format: format_reporting) -> abstract_report:
        Validator.validate_type("format", format, format_reporting)

        if format not in self.__reports.keys():
            raise self.set_exception("Указанный вариант формата  данных не реализован!")
        
        report = self.__reports[format]
        return report()
    
    def create_default(self) -> abstract_report:
        report_format = self.settings.report_format
        return self.create(report_format)
    
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)