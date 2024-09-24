from src.core.abstract_logic import abstract_logic
from src.core.format_reporting import format_reporting
from src.core.abstract_report import abstract_report
from src.reports.csv_report import csv_report
from src.errors.validator import Validator

class report_factory(abstract_logic):
    __reports: dict = {}

    def __init__(self) -> None:
        super().__init__()
        self.__reports[format_reporting.CSV] = csv_report

    def create(self, format: format_reporting) -> abstract_report:
        Validator.validate_type("format", format, format_reporting)

        if format not in self.__reports.keys():
            raise self.set_exception("Указанный вариант формата  данных не реализован!")
        
        report = self.__reports[format]
        return report()
    
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)