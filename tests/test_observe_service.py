import unittest
from src.start_service import start_service
from src.data_reposity import data_reposity
from src.manager.settings_manager import settings_manager
from src.processors.turnover_process import turnover_process
from src.core.evet_type import event_type
from src.logics.observe_service import observe_service
from src.manager.date_block_manager import date_block_manager
from src.logics.nomenclature_service import nomenclature_service
from src.logics.recipe_service import recipe_service
from src.logics.turnover_service import turnover_service
from src.logics.transaction_service import transaction_service
from src.reposity_manager import reposity_manager

from datetime import datetime, timedelta
import os

"""
Набор тестов для nomenclature_service
"""
class test_observe_service(unittest.TestCase):

    set_manager = settings_manager()
    rep_manager = reposity_manager(set_manager)
    reposity = data_reposity()
    start = start_service(reposity, set_manager)
    start.create()

    set_manager.current_settings.json_folder = "./tests/reports"

    nom_service = nomenclature_service(set_manager)
    rec_service = recipe_service(set_manager)
    tur_service = turnover_service(set_manager)
    tran_service = transaction_service(set_manager)

    """
    Проверка смены даты блокировки
    """
    def test_change_date_block(self):
        # Подготовка
        new_date_block = datetime.now() + timedelta(minutes=1)
        self.set_manager.current_settings.date_block = new_date_block

        data = self.reposity.data[data_reposity.transaction_key()]
        path = os.path.join(
            self.set_manager.current_settings.json_folder,
            turnover_process(self.set_manager).file_name
        )

        # Действия
        observe_service.raise_event(event_type.CHANGE_DATE_BLOCK, date_block=new_date_block, data=data)
        turnovers = date_block_manager.read(path)

        # Проверка
        assert len(turnovers) == len(self.reposity.data[ data_reposity.nomenclature_key() ])

    """
    Проверка получения номенклатуры по id
    """
    def test_get_nomenclature(self):
        # Подготовка
        data = self.reposity.data[data_reposity.nomenclature_key()]
        nomenclature_id = data[0].id

        # Действие
        nom_data = self.nom_service.get_nomenclature(data, nomenclature_id)
        
        # Проверка
        assert len(nom_data) == 1
        assert nom_data[0] == data[0]

    """
    Проверка добавления номенклатуры
    """
    def test_put_nomenclature(self):
        # Подготовка
        len_nom = len(self.reposity.data[data_reposity.nomenclature_key()])

        nomenclature = {
            "full_name": "Перец",
            "group": {
                "id": self.reposity.data[data_reposity.group_key()][1].id,
                "name": "Сырье"
            },
            "name": "",
            "range": {
                "base_range": None,
                "conversion_factor": 1,
                "id": self.reposity.data[data_reposity.range_key()][0].id,
                "name": "гр"
            }
        }

        # Действие
        nomenclature_exists = self.nom_service.put_nomenclature(nomenclature, self.reposity.data)

        # Проверка
        assert not nomenclature_exists
        assert len(self.reposity.data[data_reposity.nomenclature_key()]) - len_nom == 1
        assert self.reposity.data[data_reposity.nomenclature_key()][-1].full_name == "Перец"

    """
    Проверка удаления номенклатуры
    """
    def test_delete_nomenclature(self):
        # Подготовка
        data = self.reposity.data[data_reposity.nomenclature_key()]

        nomenclature = {
            "full_name": "Сахар",
            "group": {
                "id": self.reposity.data[data_reposity.group_key()][1].id,
                "name": "Сырье"
            },
            "id": self.reposity.data[data_reposity.nomenclature_key()][1].id,
            "name": "",
            "range": {
                "base_range": None,
                "conversion_factor": 1,
                "id": self.reposity.data[data_reposity.range_key()][0].id,
                "name": "гр"
            }
        }

        # Действие
        result = self.nom_service.delete_nomenclature(nomenclature, data)

        # Проверка
        assert result

    
    """
    Проверка изменения номенклатуры
    """
    def test_change_nomenclature(self):
        # Подготовка

        nomenclature = {
            "full_name": "Мука",
            "group": {
                "id": self.reposity.data[data_reposity.group_key()][1].id,
                "name": "Сырье"
            },
            "id": self.reposity.data[data_reposity.nomenclature_key()][0].id,
            "name": "",
            "range": {
                "base_range": None,
                "conversion_factor": 1,
                "id": self.reposity.data[data_reposity.range_key()][0].id,
                "name": "гр"
            }
        }


        # Действия
        observe_service.raise_event(event_type.CHANGE_NOMENCLATURE, nomenclature=nomenclature, data=self.reposity.data)

        path = os.path.join(
            self.set_manager.current_settings.json_folder,
            turnover_process(self.set_manager).file_name
        )
        turnovers = date_block_manager.read(path)

        # Проверка
        assert self.reposity.data[data_reposity.nomenclature_key()][0].full_name == "Мука"
        assert self.reposity.data[data_reposity.recipe_key()][0].nomenclatures[0][0].full_name == "Мука"
        assert list(turnovers.values())[0].nomenclature.full_name == "Мука"
        assert self.reposity.data[data_reposity.transaction_key()][0].nomenclature.full_name == "Мука"

    """
    Проверка сохранения и восстановлени reposity.data без изменения
    """
    def test_save_restore_without_changing(self):
        # Подготовка
        len_nomenclatures = len(self.reposity.data[data_reposity.nomenclature_key()])
        path = os.path.join(
            self.set_manager.current_settings.json_folder,
            self.rep_manager.file_name
        )
        # Действия 
        observe_service.raise_event(event_type.SAVE_DATA_REPOSITY, data=self.reposity.data)

        # Проверка
        assert os.path.exists(path)

        # Действия 
        observe_service.raise_event(event_type.RESTORE_DATA_REPOSITY, data=self.reposity.data)

        assert len_nomenclatures == len(self.reposity.data[data_reposity.nomenclature_key()])

    """
    Проверка сохранения и восстановлени reposity.data с добавлением номенклатуры
    """
    def test_save_restore_with_changing(self):
        # Подготовка
        len_nomenclatures = len(self.reposity.data[data_reposity.nomenclature_key()])
        path = os.path.join(
            self.set_manager.current_settings.json_folder,
            self.rep_manager.file_name
        )

        nomenclature = {
            "full_name": "Перец",
            "group": {
                "id": self.reposity.data[data_reposity.group_key()][1].id,
                "name": "Сырье"
            },
            "name": "",
            "range": {
                "base_range": None,
                "conversion_factor": 1,
                "id": self.reposity.data[data_reposity.range_key()][0].id,
                "name": "гр"
            }
        }
        # Действия 
        self.nom_service.put_nomenclature(nomenclature, self.reposity.data)
        observe_service.raise_event(event_type.SAVE_DATA_REPOSITY, data=self.reposity.data)

        # Проверка
        assert os.path.exists(path)

        # Действия 
        observe_service.raise_event(event_type.RESTORE_DATA_REPOSITY, data=self.reposity.data)

        assert len(self.reposity.data[data_reposity.nomenclature_key()]) - len_nomenclatures == 1



        