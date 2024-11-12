from src.core.abstract_logic import abstract_logic
from src.data_reposity import data_reposity
from src.errors.validator import Validator
from src.models.group import group_model
from src.models.range import range_model
from src.models.nomenclature import nomenclature_model
from src.models.settings import settings
from src.manager.settings_manager import settings_manager
from src.manager.recipe_manager import recipe_manager
from src.models.storage import storage_model
from src.models.transaction import transaction_model
from src.core.transaction_type import transaction_type
from src.core.evet_type import event_type
from src.logics.observe_service import observe_service
from src.reports.report_factory import report_factory
from src.core.format_reporting import format_reporting
from src.errors.custom_exception import FileWriteException
import os
from datetime import datetime
import random
import json

class start_service(abstract_logic):
    __reposity: data_reposity = None
    __settings_manager: settings_manager = None
    __nomenclatures: list = []
    __file_name: str = "data_reposity.json"
    

    def __init__(self, reposity: data_reposity, manager: settings_manager) -> None:
        super().__init__()
        Validator.validate_type("reposity", reposity, data_reposity)
        Validator.validate_type("manager", manager, settings_manager)
        self.__reposity = reposity
        self.__settings_manager = manager

        observe_service.append(self)

    """
    Текущие настройки
    """
    @property 
    def settings(self) -> settings:
        return self.__settings_manager.current_settings
    
    """
    Номенклатуры
    """
    @property 
    def nomenclatures(self) -> list:
        return self.__nomenclatures
    
    @nomenclatures.setter
    def nomenclatures(self, nomenclatures: list[list[nomenclature_model, int]]):
        Validator.validate_type("nomenclatures", nomenclatures, list)
        self.__nomenclatures = nomenclatures

    """
    Сформировать группы номенклатуры
    """
    def __create_nomenclature_groups(self): 
        list = [group_model.default_group_cold(), group_model.default_group_source()]
        self.__reposity.data[data_reposity.group_key()] = list

    """
    Сформировать единицы измерения
    """
    def __create_range(self): 
        list = []
        base_gramm = range_model.create("гр", 1)
        list.append(base_gramm)
        list.append(range_model.create("шт", 1))
        list.append(range_model.create("кг", 1000, base_gramm))
        self.__reposity.data[data_reposity.range_key()] = list

    """
    Сформировать номенклатуры
    """
    def __create_nomenclature(self): 
        groups = self.__reposity.data[data_reposity.group_key()]
        ranges = self.__reposity.data[data_reposity.range_key()]
        self.nomenclatures = recipe_manager(groups, ranges).creating_list_nomenclatures_all_recipes()

        list = []
        for data in self.nomenclatures:
            if data[0] not in list:
                list.append(data[0])

        self.__reposity.data[data_reposity.nomenclature_key()] = list

    """
    Сформировать рецепты
    """
    def __create_receipts(self): 
        groups = self.__reposity.data[data_reposity.group_key()]
        ranges = self.__reposity.data[data_reposity.range_key()]
        def_nomenclatures = self.nomenclatures

        recipe_list = []
        md_files = [f for f in os.listdir(recipe_manager(groups, ranges).recipe_directory) if f.endswith('.md')]
        for md_file in md_files:
            manager = recipe_manager(groups, ranges)
            manager.open(md_file, def_nomenclatures)
            recipe_list.append(manager.recipe)
        self.__reposity.data[data_reposity.recipe_key()] = recipe_list

    """
    Сформировать склады
    """
    def __create_storage(self): 
        list = []
        list.append(storage_model.create("Красноказачья 7", "Склад 1"))
        self.__reposity.data[data_reposity.storage_key()] = list

    """
    Сформировать транзакции
    """
    def __create_transaction(self): 
        list1 = []
        nomenclatures: list[list[nomenclature_model, int]] = self.nomenclatures
        for nomenclature in nomenclatures:
            nom = nomenclature[0]
            range = nom.range
            
            random_quantity = random.randint(10, 300)
            random_transaction_type = random.choice(list(transaction_type))
            list1.append(
                transaction_model.create(
                    self.__reposity.data[data_reposity.storage_key()][0],
                    nom,
                    float(random_quantity),
                    random_transaction_type,
                    range,
                    datetime.now()
                )
            )
        self.__reposity.data[data_reposity.transaction_key()] = list1

    """
    Первый старт
    """
    def create(self):
        try:
            if self.settings.first_start:
                self.__create_nomenclature_groups()
                self.__create_range()
                self.__create_nomenclature()
                self.__create_receipts()
                self.__create_storage()
                self.__create_transaction()
            else:
                self.__restore_data()
            return True
        except:
            return False
        
    """
    Восстановить данные
    """
    def __restore_data(self): 
        pass

    """
    Сохранить данные
    """
    def __save_data(self): 
        file_path = os.path.join(
            self.__settings_manager.current_settings.json_folder, self.__file_name
        )
        if os.path.exists(file_path):
            os.remove(file_path)

        result = {}
        report = report_factory(self.__settings_manager).create(format_reporting.JSON)
        for key, data in self.__reposity.data.items():
            report.create(data)
            result[key] = json.loads(report.result)

        try:
            if len(result) != 0:
                data = json.dumps(result, indent=4, ensure_ascii=False)
                with open(file_path , 'w', encoding='utf-8') as f:
                    f.write(data)
        except:
            FileWriteException("data_reposity", self.__file_name)

    """
    Перегрузка абстрактного метода
    """
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def handle_event(self, type: event_type, **kwargs):
        super().handle_event(type, **kwargs)

        if type == event_type.SAVE_DATA_REPOSITY:
            self.__save_data()
        elif type == event_type.RESTORE_DATA_REPOSITY:
            self.__restore_data()