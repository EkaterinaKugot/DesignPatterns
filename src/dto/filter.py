from src.errors.validator import Validator
from src.core.filter_type import filter_type
from datetime import datetime, timedelta


"""
Фильтр
"""
class filter:
    __name: str = ""
    __type_filter_name = filter_type.EQUALE

    __id: str = ""
    __type_filter_id = filter_type.EQUALE

    __model: str = ""
    __period: list[datetime] = None

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

    @property
    def period(self) -> list:
        return self.__period
    
    @period.setter
    def period(self, period: list):
        Validator.validate_type("period", period, list)
        Validator.validate_more_permissible_value("end_period", period[1], period[0])
        self.__period = period

    @staticmethod
    def create(data: dict, model: str = "") -> filter:
        Validator.validate_not_none("data", data)

        type_filter_name = data.get('type_filter_name', 'EQUALE').upper()
        type_filter_name = getattr(filter_type, type_filter_name, filter_type.EQUALE)
        type_filter_id = data.get('type_filter_id', 'EQUALE').upper()
        type_filter_id = getattr(filter_type, type_filter_id, filter_type.EQUALE)

        filt = filter()
        filt.name = data.get('name', "")
        filt.id = data.get('id', "")
        filt.type_filter_id = type_filter_id
        filt.type_filter_name = type_filter_name
        if model is not None:
            filt.model = model
        
        start_period = data.get('start_period')
        end_period = data.get('end_period')
        try:
            start_period = datetime.strptime(start_period, "%Y-%m-%dT%H:%M:%SZ")
            end_period = datetime.strptime(end_period, "%Y-%m-%dT%H:%M:%SZ")
            filt.period = [start_period, end_period]
        except:
            pass

        return filt
    
    def __str__(self) -> str:
        return f"Filter(\nname: {self.name}\ntype_filter_name: {self.type_filter_name}\nid: {self.id}\ntype_filter_id: {self.type_filter_id}\n)"