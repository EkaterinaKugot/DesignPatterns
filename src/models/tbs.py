from src.core.base_model import base_model_id
from src.errors.validator import Validator

"""
Модель оборотно-сальдовой ведомости
"""
class tbs_model(base_model_id):
    __opening_remainder: list = None
    __receipt: list = None
    __consumption: list = None
    __remainder: list = None

    @staticmethod
    def create(
        opening_remainder: list,
        receipt: list,
        consumption: list,
        remainder: list,
        name: str = ""
    ) -> None:
        tbs = tbs_model()
        tbs.opening_remainder = opening_remainder
        tbs.receipt = receipt
        tbs.consumption = consumption
        tbs.remainder = remainder
        tbs.name = name
        return tbs

    """
    Начальные остатки
    """
    @property
    def opening_remainder(self) -> list:
        return self.__opening_remainder
    
    @opening_remainder.setter
    def opening_remainder(self, opening_remainder: list):
        Validator.validate_type("opening_remainder", opening_remainder, list)
        self.__opening_remainder = opening_remainder

    """
    Приход
    """
    @property
    def receipt(self) -> list:
        return self.__receipt
    
    @receipt.setter
    def receipt(self, receipt: list):
        Validator.validate_type("receipt", receipt, list)
        self.__receipt = receipt

    """
    Расход
    """
    @property
    def consumption(self) -> list:
        return self.__consumption
    
    @consumption.setter
    def consumption(self, consumption: list):
        Validator.validate_type("consumption", consumption, list)
        self.__consumption = consumption

    """
    Остатки
    """
    @property
    def remainder(self) -> list:
        return self.__remainder
    
    @remainder.setter
    def remainder(self, remainder: list):
        Validator.validate_type("remainder", remainder, list)
        self.__remainder = remainder

    """
    Переопределение метода для преобразования в json
    """
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "opening_remainder": self.opening_remainder,
            "receipt": self.receipt,
            "consumption": self.consumption,
            "remainder": self.remainder,
        }