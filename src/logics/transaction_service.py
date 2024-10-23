from src.errors.validator import Validator
from src.core.transaction_type import transaction_type

"""
Класс для выполнения типов транзакций
"""
class transaction_service:

    def __init__(self, transaction_type_element: transaction_type):
        Validator.validate_type("transaction_type_element", transaction_type_element, transaction_type)
        self.transaction = getattr(self, transaction_type_element.value.lower())

    def receipt(self, turnover: int, quantity: float) -> int:
        Validator.validate_type("turnover", turnover, int)
        Validator.validate_type("quantity", quantity, float)

        result = turnover + quantity
        return result
    
    def consumption(self, turnover: int, quantity: float) -> int:
        Validator.validate_type("turnover", turnover, int)
        Validator.validate_type("quantity", quantity, float)

        result = turnover - quantity
        return result