import unittest
from src.start_service import start_service
from src.data_reposity import data_reposity
from src.logics.process_factory import turnover_process
from src.models.turnover import turnover_model
from src.manager.settings_manager import settings_manager
from src.errors.custom_exception import TypeException
from datetime import datetime

"""
Набор тестов для фильтрации
"""
class test_process(unittest.TestCase):

    set_manager = settings_manager()
    reposity = data_reposity()
    start = start_service(reposity, set_manager)
    start.create()

    """
    Проверка создания процесса для обработки оборотов
    """
    def test_turnover_process(self):
        # Подготовка
        start_date: datetime = datetime(2024, 1, 1)
        end_date: datetime = datetime(2024, 12, 30)
        storage = self.reposity.data[data_reposity.storage_key()][0]
        nomenclature = self.reposity.data[data_reposity.nomenclature_key()][0]
        turnovers = [turnover_model.create(storage, 100, nomenclature, nomenclature.range)]

        # Действие
        turnover = turnover_process(start_date, end_date)
        turnover.turnovers = turnovers

        # Проверка
        assert turnover.start_date == start_date
        assert turnover.end_date == end_date
        assert turnover.turnovers == turnovers

    """
    Проверка валидации атрибутов
    """
    def test_turnover_process_fail(self):
        # Подготовка
        start_date: datetime = datetime(2024, 1, 1)
        end_date: datetime = datetime(2024, 12, 30)
        turnover = turnover_process(start_date, end_date)
        
        # Проверка
        with self.assertRaises(TypeException):
            turnover_process(123, end_date)

        with self.assertRaises(TypeException):
            turnover_process(start_date, "str")

        
        with self.assertRaises(TypeException):
            turnover.turnovers = {}


    """
    Проверка расчета оборотов
    """
    def test_turnover_process_create(self):
        # Подготовка
        start_date: datetime = datetime(2024, 1, 1)
        end_date: datetime = datetime(2024, 12, 30)
        process_turnover = turnover_process(start_date, end_date)

        transactions = self.reposity.data[data_reposity.transaction_key()]
        storage = self.reposity.data[data_reposity.storage_key()][0]
        nomenclature = self.reposity.data[data_reposity.nomenclature_key()][0]
        
        # Действие
        process_turnover.create(transactions)
        found = list(filter(lambda item: item.storage == storage and item.nomenclature == nomenclature, process_turnover.turnovers))

        # Проверка
        assert len(process_turnover.turnovers) > 0
        assert len(found) == 1
        assert found[0].turnover == 350


