from src.core.base_model import base_model_id
from src.errors.validator import Validator
from src.models.storage import storage_model
from src.models.nomenclature import nomenclature_model
from src.models.range import range_model

"""
Модель складского оборота
"""
class turnover_model(base_model_id):
    __storage: storage_model
    __turnover: int
    __nomenclature: nomenclature_model
    __range: range_model

    @staticmethod
    def create(
        storage: storage_model,
        turnover: int,
        nomenclature: nomenclature_model,
        range: range_model,
        name: str = ""
    ) -> None:
        turnover_m = turnover_model()
        turnover_m.storage = storage
        turnover_m.nomenclature = nomenclature
        turnover_m.turnover = turnover
        turnover_m.range = range
        turnover_m.name = name
        return turnover_m

    """
    Склад
    """
    @property
    def storage(self) -> storage_model:
        return self.__storage
    
    @storage.setter
    def storage(self, storage: storage_model):
        Validator.validate_type("storage", storage, storage_model)
        self.__storage = storage

    """
    Оборот
    """
    @property
    def turnover(self) -> int:
        return self.__turnover
    
    @turnover.setter
    def turnover(self, turnover: int):
        Validator.validate_type("turnover", turnover, int)
        self.__turnover = turnover

    """
    Номенклатура
    """
    @property
    def nomenclature(self) -> nomenclature_model:
        return self.__nomenclature
    
    @nomenclature.setter
    def nomenclature(self, nomenclature: nomenclature_model):
        Validator.validate_type("nomenclature", nomenclature, nomenclature_model)
        self.__nomenclature = nomenclature

    """
    Единица измерения
    """
    @property
    def range(self) -> range_model:
        return self.__range
    
    @range.setter
    def range(self, range: range_model):
        Validator.validate_type("range", range, range_model)
        self.__range = range


    """
    Переопределение метода для преобразования в json
    """
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "storage": self.storage.to_dict(),
            "turnover": self.turnover,
            "nomenclature": self.nomenclature.to_dict(),
            "range": self.range.to_dict(),
        }
    
    """
    Переопределение получения аттрибутов и класса
    """
    @property
    def attribute_class(self) -> dict:
        return {
            "storage": storage_model,
            "nomenclature": nomenclature_model,
            "range": range_model
            }