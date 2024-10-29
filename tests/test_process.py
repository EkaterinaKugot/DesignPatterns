import unittest
from src.start_service import start_service
from src.data_reposity import data_reposity
from src.processors.turnover_process import turnover_process
from src.manager.settings_manager import settings_manager
from src.models.transaction import transaction_model
from src.core.transaction_type import transaction_type
from src.processors.process_factory import process_factory
from src.processors.date_block_processor import date_block_processor
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
    set_manager.current_settings.date_block = datetime(1900, 1, 1)

    factory = process_factory(set_manager)
    factory.register_process('turnover', turnover_process)
    factory.register_process('date_block', date_block_processor)

    """
    Проверка расчета оборотов
    """
    def test_turnover_process_create(self):
        # Подготовка
        process_turnover = self.factory.create('turnover')

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
        found = [turnovers[key] for key in turnovers if key == (storage.id, nomenclature1.id)]

        # Проверка
        assert len(turnovers) > 0
        assert len(found) == 1
        assert found[0].turnover == 125


