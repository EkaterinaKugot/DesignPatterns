from src.core.base_model import base_model_id
from src.errors.validator import Validator
from src.core.transaction_type import transaction_type
from src.models.storage import storage_model
from src.models.nomenclature import nomenclature_model
from src.models.range import range_model
from datetime import datetime

"""
Модель складской транзакции
"""
class transaction_model(base_model_id):
    __storage: storage_model
    __nomenclature: nomenclature_model
    __quantity: int
    __type_transaction: transaction_type
    __range: range_model
    __period: datetime

    @staticmethod
    def create(
        storage: storage_model,
        nomenclature: nomenclature_model,
        quantity: int,
        type_transaction: transaction_type,
        range: range_model,
        period: datetime,
        name: str = ""
    ) -> None:
        transaction = transaction_model()
        transaction.storage = storage
        transaction.nomenclature = nomenclature
        transaction.quantity = quantity
        transaction.type_transaction = type_transaction
        transaction.range = range
        transaction.period = period
        transaction.name = name
        return transaction

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
    Количество
    """
    @property
    def quantity(self) -> int:
        return self.__quantity
    
    @quantity.setter
    def quantity(self, quantity: int):
        Validator.validate_type("quantity", quantity, int)
        Validator.validate_more_permissible_value("quantity", quantity, 0)
        self.__quantity = quantity

    """
    Тип транзакции
    """
    @property
    def type_transaction(self) -> transaction_type:
        return self.__type_transaction
    
    @type_transaction.setter
    def type_transaction(self, type_transaction: transaction_type):
        Validator.validate_type("type_transaction", type_transaction, transaction_type)
        self.__type_transaction = type_transaction

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
    Период
    """
    @property
    def period(self) -> datetime:
        return self.__period
    
    @period.setter
    def period(self, period: datetime):
        Validator.validate_type("period", period, datetime)
        self.__period = period

    """
    Переопределение метода для преобразования в json
    """
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "storage": self.storage.to_dict(),
            "nomenclature": self.nomenclature.to_dict(),
            "quantity": self.quantity,
            "type_transaction": self.type_transaction.value,
            "range": self.range.to_dict(),
            "period": self.period,
        }
    
    """
    Переопределение получения аттрибутов и класса
    """
    @property
    def attribute_class(self) -> dict:
        return {
            "storage": storage_model,
            "nomenclature": nomenclature_model,
            "type_transaction": transaction_type,
            "range": range_model
            }
