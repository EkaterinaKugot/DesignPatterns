from src.errors.validator import Validator
import json
import glob
from src.core.abstract_reference import abstract_reference
from src.core.abstract_logic import abstract_logic
from src.core.abstract_report import abstract_report

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
            return self.deserialize(file_name)
        except Exception as ex:
            self.set_exception(ex)
            return False
    
    """
    Десериализации данных из JSON
    """
    def deserialize(self, file_name: str):
        full_path = self.file_search(file_name)

        with open(full_path) as stream:
            data_list = json.load(stream)

        Validator.validate_type("data_list", data_list, list)
        Validator.validate_empty_argument("data_list", data_list)

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
        fields = list(filter
                          (lambda x: not x.startswith("_"), dir(model_class))
                        )
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
        else:
            deserialized_value = value
        return deserialized_value

    """
    Перегрузка абстрактного метода
    """
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)