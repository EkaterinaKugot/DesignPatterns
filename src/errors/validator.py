from src.errors.custom_exception import ArgumentException, TypeException, PermissibleLengthException, EmptyArgumentException
from src.errors.custom_exception import PermissibleValueException, RequiredLengthException
class Validator:
    @staticmethod
    def validate_type(argument_name: str, value, required_type):
        """Проверяет тип аргумента"""
        if not isinstance(value, required_type):
            raise TypeException(argument_name, value, required_type)

    @staticmethod
    def validate_permissible_length(argument_name: str, value: str, max_length: int):
        """Проверяет допустимую длину строки"""
        if len(value) > max_length:
            raise PermissibleLengthException(argument_name, value, max_length)
    
    @staticmethod
    def validate_required_length(argument_name: str, value: str, required_length: int):
        """Проверяет, что строка необходимой длины"""
        if len(value) != required_length:
            raise RequiredLengthException(argument_name, value, required_length)
        
    @staticmethod
    def validate_permissible_value(argument_name: str, value: int, permissible_value: int):
        """Проверяет, что число не превышает допустимое значение"""
        if value > permissible_value:
            raise PermissibleValueException(argument_name, value, permissible_value)

    @staticmethod
    def validate_not_none(argument_name: str, value):
        """Проверяет, что значение не равно None"""
        if value is None:
            raise ArgumentException(argument_name)
        
    @staticmethod
    def validate_empty_argument(argument_name: str, value):
        """Проверяет не пуст ли аргумент"""
        if len(value) == 0:
            raise EmptyArgumentException(argument_name)
        