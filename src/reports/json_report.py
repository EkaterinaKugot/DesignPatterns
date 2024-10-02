from src.core.format_reporting import format_reporting
from src.core.abstract_report import abstract_report
from src.errors.validator import Validator
import json

"""
Отчет формирует набор данных в формате json
"""
class json_report(abstract_report):

    def __init__(self) -> None:
        super().__init__()
        self.__format = format_reporting.JSON

    def create(self, data: list):
        Validator.validate_type("data", data, list)
        Validator.validate_empty_argument("data", data)
        
        first_model = data[0]
        fields = self.get_class_fields(first_model)

        json_data = []
        
        # Данные
        for row in data:
            row_data = {}
            for field in fields:
                value = getattr(row, field)
                
                row_data[field] = self.__serialize(value)
            json_data.append(row_data)
        
        self.result = json.dumps(json_data, indent=4, ensure_ascii=False)

    """
    Преобразование в словарь
    """
    def __serialize(self, value):
        if isinstance(value, list):
            return [self.__serialize(item) for item in value]
        elif hasattr(value, "to_dict"):
            return value.to_dict()
        elif hasattr(value, "__dict__"):
            return {key: self.__serialize(val) for key, val in value.__dict__.items() if not key.startswith("_")}
        else:
            return value