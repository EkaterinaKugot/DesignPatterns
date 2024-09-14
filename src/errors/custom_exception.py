class CustomException(Exception):
    """Изначальный класс исключений"""
    pass

class ArgumentException(CustomException):
    """Исключение для ошибок, связанных с некоректными аргументами"""
    def __init__(self, argument_name: str, value, message: str = "Некорректный аргумент"):
        self.message = f"{message} '{argument_name}' со значением '{value}'."
        super().__init__(self.message)

class TypeException(CustomException):
    """Исключение для ошибок, связанных с типом аргумента"""
    def __init__(self, argument_name: str, value: str, required_type: int):
        self.message = f"Аргумент '{argument_name}' со значением '{value}' должен иметь тип {required_type}."
        super().__init__(self.message)

class PermissibleLengthException(CustomException):
    """Исключение для ошибок, связанных с превышением допустимой длины строки"""
    def __init__(self, argument_name: str, value: str, max_length: int,):
        self.message = f"Длина аргумента'{argument_name}' со значением '{value}' превышает допустимый лимит в {max_length} символов."
        super().__init__(self.message)

class RequiredLengthException(CustomException):
    """Исключение для ошибок, связанных с необходимой длиной строки"""
    def __init__(self, argument_name: str, value: str, required_length: int):
        self.message = f"Длина аргмента '{argument_name}' со значением '{value}' должна содержать {required_length} символов."
        super().__init__(self.message)

class PermissibleValueException(CustomException):
    """Исключение для ошибок, связанных с превышением числа"""
    def __init__(self, argument_name: str, value: int, permissible_value: int):
        self.message = f"Аргумент '{argument_name}' со значением '{value}' не должен превышать {permissible_value}."
        super().__init__(self.message)

class ElementNotFoundException(CustomException):
    """Исключение для ошибок, связанных с отсутствием файла или данных."""
    def __init__(self, element_name: str, message: str = "Директория или файл"):
        self.message = f"{message} '{element_name}' не найдены."
        super().__init__(self.message)