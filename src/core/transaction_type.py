from enum import Enum

"""
Типы транзакций
"""
class transaction_type(Enum):
    RECEIPT = "RECEIPT"
    CONSUMPTION = "CONSUMPTION"