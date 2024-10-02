from src.core.format_reporting import format_reporting
from src.core.abstract_report import abstract_report
from src.errors.validator import Validator

"""
Отчет формирует набор данных в формате RTF
"""
class rtf_report(abstract_report):

    def __init__(self) -> None:
        super().__init__()
        self.__format = format_reporting.RTF

    def create(self, data: list):
        self.result = ""
        Validator.validate_type("data", data, list)
        Validator.validate_empty_argument("data", data)
        
        first_model = data[0]
        fields = self.get_class_fields(first_model)
        
        # Начало 
        self.result += r"{\rtf1\ansi\ansicpg1251\deff0\nouicompat{\fonttbl{\f0\fnil\fcharset0 Arial;}}"
        self.result += r"{\*\generator Riched20 10.0.18362;}"

        # Заголовок
        self.result += r"\viewkind4\uc1 \pard\fs20 "
        self.result += r"\b Заголовки:\b0 " + " | ".join(fields) + r"\par "

        # Данные
        for row in data:
            row_values = []
            for field in fields:
                value = getattr(row, field)
                row_values.append(str(value) if value is not None else "")
            self.result += r"\pard " + " | ".join(row_values) + r"\par "

        self.result += r"}"
