from src.core import abstract_logic
from src.data_reposity import data_reposity
from src.errors.validator import Validator
from src.models.group import group_model
from src.models.range import range_model
from src.models.recipe import recipe_model
from src.models.nomenclature import nomenclature_model
from src.settings_manager import settings_manager
from src.models.settings import settings
import os


class start_service(abstract_logic):
    __reposity: data_reposity = None
    __settings_manager: settings_manager = None
    __recipe_directory: str = "./src/docs"

    def __init__(self, reposity: data_reposity, manager: settings_manager) -> None:
        super.__init__()
        Validator.validate_type("reposity", reposity, data_reposity)
        Validator.validate_type("manager", manager, settings_manager)
        self.__reposity = reposity
        self.__settings_manager = manager

    """
    Единица измерения
    """
    @property
    def recipe_directory(self) -> str:
        return self.__recipe_directory
    
    @recipe_directory.setter
    def recipe_directory(self, recipe_directory: str):
        Validator.validate_type("recipe_directory", recipe_directory, str)
        self.__recipe_directory = recipe_directory

    """
    Текущие настройки
    """
    @property 
    def settings(self) -> settings:
        return self.__settings_manager.settings

    """
    Сформировать группы номенклатуры
    """
    def __create_nomenclature_groups(self): 
        list = [group_model.default_group_cold(), group_model.default_group_source()]
        self.__reposity.data[data_reposity.group_key()] = list


    """
    Сформировать номенклатуры
    """
    def __create_nomenclature(self): 
        ingredients, gram = nomenclature_model.process_markdown_files(self.recipe_directory)
        list = nomenclature_model.create_list_nomenclature(ingredients, gram)
        self.__reposity.data[data_reposity.nomenclature_key()] = list

    """
    Сформировать единицы измерения
    """
    def __create_range(self): 
        list = []
        list.append(range_model("кг", 1000, range_model()))
        list.append(range_model("шт", 10, range_model("шт", 1)))
        self.__reposity.data[data_reposity.range_key()] = list

    """
    Сформировать рецепты
    """
    def __create_receipts(self): 
        list = []
        md_files = [f for f in os.listdir(self.recipe_directory) if f.endswith('.md')]
        for md_file in md_files:
            list.append(recipe_model(md_file))
        self.__reposity.data[data_reposity.recipe_key()] = list
    
    """
    Первый старт
    """
    def create(self):
        self.__create_nomenclature_groups()
        self.__create_nomenclature()
        self.__create_range()
        self.__create_receipts()

    """
    Перегрузка абстрактного метода
    """
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)