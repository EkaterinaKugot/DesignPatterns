import unittest
from src.start_service import start_service
from src.data_reposity import data_reposity
from src.manager.settings_manager import settings_manager
from src.models.transaction import transaction_model
from src.core.transaction_type import transaction_type
from src.processors.process_factory import process_factory

from datetime import datetime, timedelta
import random
import time
import os

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

    """
    Проверка расчета оборотов
    """
    def test_turnover_process_processor(self):
        # Подготовка
        process_turnover = self.factory.create('turnover')

        storage = self.reposity.data[data_reposity.storage_key()][0]
        nomenclature1 = self.reposity.data[data_reposity.nomenclature_key()][0]
        range1 = self.reposity.data[data_reposity.range_key()][0]

        transactions = self.creatу_artificial_transactions(storage, nomenclature1)
        
        # Действие
        turnovers = process_turnover.processor(transactions)
        found = [turnovers[key] for key in turnovers if key == (storage.id, nomenclature1.id, range1.id)]

        # Проверка
        assert len(turnovers) > 0
        assert len(found) == 1
        assert found[0].turnover == 125

    """
    Проверка расчета оборотов date_block
    """
    def test_date_block_process_processor(self):
        # Подготовка
        process_turnover = self.factory.create('date_block')

        storage = self.reposity.data[data_reposity.storage_key()][0]
        nomenclature1 = self.reposity.data[data_reposity.nomenclature_key()][0]

        self.set_manager.current_settings.json_folder = "./tests/reports"

        transactions = self.creatу_artificial_transactions(storage, nomenclature1)
        self.set_manager.current_settings.date_block = datetime.now() + timedelta(minutes=10)
        
        # Действие
        turnovers = process_turnover.processor(transactions)
        path = os.path.join(self.set_manager.current_settings.json_folder , process_turnover.file_name) 

        # Проверка
        assert turnovers
        assert isinstance(path, str)

        # Подготовка
        self.set_manager.current_settings.date_block = datetime(1900, 1, 2)

        # Действие
        turnovers = process_turnover.processor(transactions)

        # Проверка
        assert turnovers
        assert not os.path.exists(path)

    """
    Проверка расчета оборотов до date_block и после с замером времени
    """
    def test_processor(self):
        # Подготовка
        process_date_block = self.factory.create('date_block')
        self.set_manager.current_settings.json_folder = "./tests/reports"
        self.set_manager.current_settings.date_block = datetime.now()
        process_date_block.file_name = "test_date_block.json"
        path = os.path.join(self.set_manager.current_settings.json_folder , process_date_block.file_name) 

        try:
            os.remove(path)
        except:
            pass
        
        count_tr = 20000
        transactions = self.creatу_more_transactions(count_tr)

        # Расчет до date_block 
        assert process_date_block.processor(transactions)

        # Подготовка к расчету с date_block
        process_turnover = self.factory.create('turnover')
        process_turnover.file_name = "test_date_block.json"

        # Действие. Расчет c date_block
        start_time_with = time.time()
        turnovers_with = process_turnover.processor(transactions)
        elapsed_time_with = time.time() - start_time_with

        turnovers_val_with = list(turnovers_with.values())

        # Промежуточная проверка
        assert len(turnovers_val_with) != 0

        # Подготовка к расчету без date_block
        self.set_manager.current_settings.date_block = datetime(1900, 1, 1)
        os.remove(path)

        # Действие. Расчет без date_block
        start_time_without = time.time()
        turnovers_without = process_turnover.processor(transactions)
        elapsed_time_without = time.time() - start_time_without

        turnovers_val_without = list(turnovers_without.values())

        print("\n")
        print(f"Всего транзакций: {count_tr}. Из них {int(count_tr - count_tr // 1.2)} не входят в date_block.")
        print("Время с рассчитанным date_block:", elapsed_time_with)
        print("Время без date_block:", elapsed_time_without, "\n")

        # Проверка
        assert len(turnovers_val_without) != 0
        assert len(turnovers_val_with) == len(turnovers_val_without)
        assert turnovers_val_with[0] != turnovers_val_without[0]
        
        for t1, t2 in zip(turnovers_val_with, turnovers_val_without):
            assert t1.turnover == t2.turnover

    def creatу_more_transactions(self, c_tur: int = 1500):
        transactions = []
        nomenclatures = self.reposity.data[data_reposity.nomenclature_key()]
        storage = self.reposity.data[data_reposity.storage_key()][0]

        count_iter = c_tur  // len(nomenclatures)
        for i in range(count_iter):
            for nomenclature in nomenclatures:
                range1 = nomenclature.range

                date = datetime.now() - timedelta( minutes=(count_iter-i) * len(nomenclatures) )
                if i * len(nomenclatures) > c_tur // 1.2:
                    date = datetime.now() + timedelta( minutes=i * len(nomenclatures) )
                
                random_quantity = random.randint(10, 300)
                random_transaction_type = random.choice(list(transaction_type)) 

                transaction = transaction_model.create(
                    storage,
                    nomenclature,
                    float(random_quantity),
                    random_transaction_type,
                    range1,
                    date
                )
                transactions.append(transaction)
        return transactions


    def creatу_artificial_transactions(self, storage, nomenclature1):
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
        return transactions


