from src.core.format_reporting import format_reporting
from src.core.abstract_report import abstract_report
from src.errors.validator import Validator

"""
Отчет формирует набор данных в формате CSV
"""
class csv_report(abstract_report):

    def __init__(self) -> None:
        super().__init__()
        self.__format = format_reporting.CSV

    def create(self, data: list):
        Validator.validate_type("data", data, list)
        Validator.validate_empty_argument("data", data)
        
        first_model = data[0]
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(first_model.__class__, x)), dir(first_model) ))
        # Заголовок
        for field in fields:
            self.result += f"{field};"
        self.result += "\n"
        
        # Данные
        for row in data:
            for field in fields:
                value = getattr(row, field)
                self.result += f"{value};"
            self.result += "\n"
