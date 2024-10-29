from abc import ABC, abstractmethod
from src.errors.validator import Validator
import glob

"""
Абстрактный класс для обработки логики
"""
class abstract_logic(ABC):
    __error_text: str = ""

    @property
    def error_text(self) -> str:
        return self.__error_text.strip()
    
    @error_text.setter
    def error_text(self, message: str):
        self.__error_text = message.strip()
    
    @property
    def is_error(self) -> bool:
        return self.error_text != ""

    def _inner_set_exception(self, ex: Exception):
        self.__error_text = f"Ошибка! Исключение {ex}"

    """
    Абстрактны метод для загрузки и обработки исключений
    """
    @abstractmethod
    def set_exception(self, ex: Exception):
        pass

    @staticmethod
    def file_search(file_name: str) -> str:
        Validator.validate_type("file_name", file_name, str)

        path = f"./**/{file_name}"
        full_path = glob.glob(path, recursive=True)

        Validator.validate_not_none("full_path", full_path)
        Validator.validate_empty_argument("full_path", full_path)

        return full_path[0]
