from src.errors.validator import Validator
import json
import glob
from src.core.abstract_reference import abstract_reference
from src.core.abstract_logic import abstract_logic
from src.core.abstract_report import abstract_report
from src.core.transaction_type import transaction_type
from src.core.evet_type import event_type
from datetime import datetime

"""
Класс для десериализации json отчета обратно в объекты
"""
class json_deserializer(abstract_logic):

    def __init__(self, model_class) -> None:
        self.model_class = model_class
        self.model_objects: list = None

    """
    Десериализации данных из JSON
    """
    def open(self, file_name: str):
        Validator.validate_type("file_name", file_name, str)

        try:
            return self.__deserialize_data(file_name)
        except Exception as ex:
            self.set_exception(ex)
            return False
    
    """
    Десериализации данных
    """
    def __deserialize_data(self, file_name: str):
        full_path = self.file_search(file_name)

        with open(full_path, encoding='utf-8') as stream:
            data_list = json.load(stream)

        Validator.validate_type("data_list", data_list, list)

        objects = []
        
        for item in data_list:
            obj = self.__deserialize_model(item, self.model_class)
            objects.append(obj)
        
        self.model_objects = objects
        return True

    """
    Заполнение модели данными
    """
    def __deserialize_model(self, item, model_class: abstract_reference):
        fields = abstract_report.get_class_fields(model_class, True)
        obj = model_class()
        for key, value in item.items():
            deserialized_value = self.__deserialize(obj, key, value)
            
            if key in fields:
                setattr(obj, key, deserialized_value)
        return obj

    """
    Преобразование данных в модели
    """
    def __deserialize(self, obj, key, value):
        if isinstance(value, dict):
            new_model_class = obj.attribute_class.get(key, None)
            Validator.validate_not_none("new_model_class", new_model_class)
            deserialized_value = self.__deserialize_model(value, new_model_class)
        elif isinstance(value, list):
            deserialized_value = [self.__deserialize(obj, key, item) for item in value]
        elif isinstance(value, str):
            try:
                deserialized_value = transaction_type[value]
            except:
                deserialized_value = value  
        elif key == "period":
            try:
                deserialized_value = datetime.fromtimestamp(value)
            except:
                deserialized_value = value  
        else:
            deserialized_value = value
        return deserialized_value

    """
    Перегрузка абстрактного метода
    """
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def handle_event(self, type: event_type, **kwargs):
        super().handle_event(type, **kwargs)