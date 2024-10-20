from src.core.base_model import base_model_id
from src.errors.validator import Validator

"""
Модель склада
"""
class storage_model(base_model_id):
    __address: str = ""

    """
    Адрес (местоположение)
    """
    @property
    def address(self) -> str:
        return self.__address
    
    @address.setter
    def address(self, address: str):
        Validator.validate_type("address", address, str)
        Validator.validate_empty_argument("address", address)
        self.__address = address.strip()

    """
    Переопределение метода для преобразования в json
    """
    def to_dict(self):
        return {
            "address": self.address,
            "id": self.id,
            "name": self.name,
        }