from src.errors.validator import Validator
from src.core.filter_type import filter_type
from src.core.abstract_reference import abstract_reference


"""
Фильтр
"""
class filter:
    __name: str = ""
    __type_filter_name = filter_type.EQUALE

    __id: str = ""
    __type_filter_id = filter_type.EQUALE

    __model: str = ""

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name: str):
        Validator.validate_type("name", name, str)
        self.__name = name

    @property
    def type_filter_name(self) -> filter_type:
        return self.__type_filter_name
    
    @type_filter_name.setter
    def type_filter_name(self, type_filter_name: filter_type):
        Validator.validate_type("type_filter_name", type_filter_name, filter_type)
        self.__type_filter_name = type_filter_name

    @property
    def id(self) -> str:
        return self.__id
    
    @id.setter
    def id(self, id: str):
        Validator.validate_type("id", id, str)
        self.__id = id

    @property
    def type_filter_id(self) -> filter_type:
        return self.__type_filter_id
    
    @type_filter_id.setter
    def type_filter_id(self, type_filter_id: filter_type):
        Validator.validate_type("type_filter_id", type_filter_id, filter_type)
        self.__type_filter_id = type_filter_id

    @property
    def model(self) -> str:
        return self.__model
    
    @model.setter
    def model(self, model: str):
        Validator.validate_type("model", model, str)
        self.__model = model

    @staticmethod
    def create(data: dict) -> filter:
        Validator.validate_not_none("data", data)

        model = data.get('model')

        type_filter_name = data.get('type_filter_name', 'EQUALE').upper()
        type_filter_name = getattr(filter_type, type_filter_name, filter_type.EQUALE)
        type_filter_id = data.get('type_filter_id', 'EQUALE').upper()
        type_filter_id = getattr(filter_type, type_filter_id, filter_type.EQUALE)

        filt = filter()
        filt.name = data.get('name')
        filt.id = data.get('id')
        filt.type_filter_id = type_filter_id
        filt.type_filter_name = type_filter_name
        if model is not None:
            filt.model = model

        return filt
    
    def __str__(self) -> str:
        return f"Filter(\nname: {self.name}\ntype_filter_name: {self.type_filter_name}\nid: {self.id}\ntype_filter_id: {self.type_filter_id}\n)"