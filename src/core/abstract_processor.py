from abc import ABC, abstractmethod
from src.errors.validator import Validator
from src.models.transaction import transaction_model


"""
Абстрактный класс для процессов транзакции
"""
class abstract_processor:
    
    @abstractmethod
    def processor(self, transactions: list[transaction_model]):
        pass

    @abstractmethod
    def creater(data: dict):
        pass