import unittest
from src.start_service import start_service
from src.data_reposity import data_reposity
from src.logics.turnover_process import turnover_process
from src.models.turnover import turnover_model
from src.manager.settings_manager import settings_manager
from src.errors.custom_exception import TypeException
from src.models.transaction import transaction_model
from src.core.transaction_type import transaction_type
from datetime import datetime
import random

"""
Набор тестов для фильтрации
"""
class test_process(unittest.TestCase):

    set_manager = settings_manager()
    reposity = data_reposity()
    start = start_service(reposity, set_manager)
    start.create()

    """
    Проверка расчета оборотов
    """
    def test_turnover_process_create(self):
        # Подготовка
        process_turnover = turnover_process()

        storage = self.reposity.data[data_reposity.storage_key()][0]
        nomenclature1 = self.reposity.data[data_reposity.nomenclature_key()][0]

        transactions = []
        nomenclatures = self.reposity.data[data_reposity.nomenclature_key()]
        for nomenclature in nomenclatures:
            range = nomenclature.range

            random_quantity = random.randint(10, 300)
            random_transaction_type = random.choice(list(transaction_type)) 

            if nomenclature1 == nomenclature:
                transactions.append(
                    transaction_model.create(
                        storage,
                        nomenclature,
                        float(150),
                        transaction_type.RECEIPT,
                        range,
                        datetime.now()
                    )
                )
                transaction = transaction_model.create(
                    storage,
                    nomenclature,
                    float(25),
                    transaction_type.CONSUMPTION,
                    range,
                    datetime.now()
                )
            else:
                transaction = transaction_model.create(
                    storage,
                    nomenclature,
                    float(random_quantity),
                    random_transaction_type,
                    range,
                    datetime.now()
                )
            transactions.append(transaction)
        
        # Действие
        turnovers = process_turnover.processor(transactions)
        found = list(filter(lambda item: item.storage == storage and item.nomenclature == nomenclature1, turnovers))
        print(found[0].turnover)

        # Проверка
        assert len(turnovers) > 0
        assert len(found) == 1
        assert found[0].turnover == 125


