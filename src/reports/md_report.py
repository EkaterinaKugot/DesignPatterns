from src.core.format_reporting import format_reporting
from src.core.abstract_report import abstract_report
from src.errors.validator import Validator

"""
Отчет формирует набор данных в формате md
"""
class md_report(abstract_report):

    def __init__(self) -> None:
        super().__init__()
        self.__format = format_reporting.MARKDOWN

    def create(self, data: list):
        self.result = ""
        Validator.validate_type("data", data, list)
        Validator.validate_empty_argument("data", data)
        
        first_model = data[0]
        fields = list(
            filter(
                lambda x: not x.startswith("_") and x != "attribute_class" and
                not callable(getattr(first_model.__class__, x)), dir(first_model)
                )
            )
        # Заголовок
        self.result += "| " + " | ".join(fields) + " |\n"
        
        # Разделитель
        self.result += "| " + " | ".join(["---"] * len(fields)) + " |\n"
        
        # Данные
        for row in data:
            row_data = [str(getattr(row, field)) for field in fields]
            self.result += "| " + " | ".join(row_data) + " |\n"