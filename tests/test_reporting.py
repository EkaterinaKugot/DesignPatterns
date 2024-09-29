from src.start_service import start_service
from src.data_reposity import data_reposity
from src.reports.report_factory import report_factory
from src.core.format_reporting import format_reporting
from src.reports.csv_report import csv_report
from src.reports.md_report import md_report
from src.reports.json_report import json_report
from src.reports.xml_report import xml_report
from src.reports.rtf_report import rtf_report
from src.manager.settings_manager import settings_manager
from src.errors.custom_exception import TypeException
from src.models.range import range_model
from src.models.nomenclature import nomenclature_model
from src.models.recipe import recipe_model
from src.models.group import group_model
from src.reports.json_deserializer import json_deserializer
import unittest
import os 

"""
Набор тестов для проверки работы формирования отчетов
"""
class test_reporting(unittest.TestCase):

    set_manager = settings_manager()
    reposity = data_reposity()
    start = start_service(reposity, set_manager)
    start.create()

    report_csv = csv_report()
    report_md = md_report()
    report_json = json_report()
    report_xml = xml_report()
    report_rtf = rtf_report()

    __reports_path = "./tests/reports"

    def __check_folder_exists(self) -> None:
        if not (os.path.exists(self.__reports_path) and os.path.isdir(self.__reports_path)):
            os.makedirs(self.__reports_path)
    
    def __save_file(self, file_name: str, result) -> None:
        with open(os.path.join(self.__reports_path, file_name), 'w', encoding='utf-8') as f:
            f.write(result)

    
    """
    Проверка report_factory
    """
    def test_report_factory_create(self):
        # Подготовка
        set_manager = settings_manager()

        # Действие
        report = report_factory(set_manager).create(format_reporting.CSV)

        # Проверка
        assert report is not None
        assert isinstance(report, csv_report)

    """
    Проверка загрузки форматов из настроек у report_factory
    """
    def test_report_factory_load_formats(self):
        # Подготовка
        set_manager = settings_manager()
        report_f = report_factory(set_manager)

        # Действие
        report_f.load_formats_from_settings()

        # Проверка
        assert len(report_f.reports_setting) != 0

    """
    Проверка некорректно заданные атрибуты
    """
    def test_report_factory_fail(self):
        # Подготовка
        set_manager = settings_manager()
        report_f = report_factory(set_manager)

        # Проверка
        with self.assertRaises(TypeException):
            report_f.reports = ["qwrt", 1]

        with self.assertRaises(TypeException):
            report_f.reports_setting = "trtr"

    """
    Проверка работы отчета CSV для range
    """
    def test_csv_report_create_range(self):
        self.assertIsNotNone(self.reposity)
        # Действие
        self.report_csv.create(self.reposity.data[data_reposity.range_key()])

        # Проверка
        assert self.report_csv.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.range_key()}.csv"
        self.__save_file(file_name, self.report_csv.result)
    
    """
    Проверка работы отчета CSV для nomenclature
    """
    def test_csv_report_create_nomenclature(self):
        # Действие
        self.report_csv.create(self.reposity.data[data_reposity.nomenclature_key()])

        # Проверка
        assert self.report_csv.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.nomenclature_key()}.csv"
        self.__save_file(file_name, self.report_csv.result)

    """
    Проверка работы отчета CSV для group
    """
    def test_csv_report_create_group(self):
        # Действие
        self.report_csv.create(self.reposity.data[data_reposity.group_key()])

        # Проверка
        assert self.report_csv.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.group_key()}.csv"
        self.__save_file(file_name, self.report_csv.result)
        print(self.report_csv.result)
    
    """
    Проверка работы отчета CSV для recipe
    """
    def test_csv_report_create_recipe(self):
        # Действие
        self.report_csv.create(self.reposity.data[data_reposity.recipe_key()])

        # Проверка
        assert self.report_csv.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.recipe_key()}.csv"
        self.__save_file(file_name, self.report_csv.result)


    """
    Проверка работы отчета md для range
    """
    def test_md_report_create_range(self):
        # Действие
        self.report_md.create(self.reposity.data[data_reposity.range_key()])

        # Проверка
        assert self.report_md.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.range_key()}.md"
        self.__save_file(file_name, self.report_md.result)

    """
    Проверка работы отчета md для nomenclature
    """
    def test_md_report_create_nomenclature(self):
        # Действие
        self.report_md.create(self.reposity.data[data_reposity.nomenclature_key()])

        # Проверка
        assert self.report_md.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.nomenclature_key()}.md"
        self.__save_file(file_name, self.report_md.result)

    """
    Проверка работы отчета md для group
    """
    def test_md_report_create_group(self):
        # Действие
        self.report_md.create(self.reposity.data[data_reposity.group_key()])

        # Проверка
        assert self.report_md.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.group_key()}.md"
        self.__save_file(file_name, self.report_md.result)

    """
    Проверка работы отчета md для recipe
    """
    def test_md_report_create_recipe(self):
        # Действие
        self.report_md.create(self.reposity.data[data_reposity.recipe_key()])

        # Проверка
        assert self.report_md.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.recipe_key()}.md"
        self.__save_file(file_name, self.report_md.result)

    """
    Проверка работы отчета json для range
    """
    def __json_report_create_range(self):
        # Действие
        self.report_json.create(self.reposity.data[data_reposity.range_key()])

        # Проверка
        assert self.report_json.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.range_key()}.json"
        self.__save_file(file_name, self.report_json.result)


    """
    Проверка работы отчета json для nomenclature
    """
    def __json_report_create_nomenclature(self):
        # Действие
        self.report_json.create(self.reposity.data[data_reposity.nomenclature_key()])

        # Проверка
        assert self.report_json.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.nomenclature_key()}.json"
        self.__save_file(file_name, self.report_json.result)

    """
    Проверка работы отчета json для group
    """
    def __json_report_create_group(self):
        # Действие
        self.report_json.create(self.reposity.data[data_reposity.group_key()])

        # Проверка
        assert self.report_json.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.group_key()}.json"
        self.__save_file(file_name, self.report_json.result)

    """
    Проверка работы отчета json для recipe
    """
    def __json_report_create_recipe(self):
        ## Действие
        self.report_json.create(self.reposity.data[data_reposity.recipe_key()])

        # Проверка
        assert self.report_json.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.recipe_key()}.json"
        self.__save_file(file_name, self.report_json.result)

    """
    Проверка работы отчета xml для range
    """
    def test_xml_report_create_range(self):
        # Действие
        self.report_xml.create(self.reposity.data[data_reposity.range_key()])

        # Проверка
        assert self.report_xml.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.range_key()}.xml"
        self.__save_file(file_name, self.report_xml.result)


    """
    Проверка работы отчета xml для nomenclature
    """
    def test_xml_report_create_nomenclature(self):
        # Действие
        self.report_xml.create(self.reposity.data[data_reposity.nomenclature_key()])

        # Проверка
        assert self.report_xml.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.nomenclature_key()}.xml"
        self.__save_file(file_name, self.report_xml.result)

    """
    Проверка работы отчета xml для group
    """
    def test_xml_report_create_group(self):
        # Действие
        self.report_xml.create(self.reposity.data[data_reposity.group_key()])

        # Проверка
        assert self.report_xml.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.group_key()}.xml"
        self.__save_file(file_name, self.report_xml.result)

    """
    Проверка работы отчета xml для recipe
    """
    def test_xml_report_create_recipe(self):
        # Действие
        self.report_xml.create(self.reposity.data[data_reposity.recipe_key()])

        # Проверка
        assert self.report_xml.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.recipe_key()}.xml"
        self.__save_file(file_name, self.report_xml.result)

    """
    Проверка работы отчета rtf для range
    """
    def test_rtf_report_create_range(self):
        # Действие
        self.report_rtf.create(self.reposity.data[data_reposity.range_key()])

        # Проверка
        assert self.report_rtf.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.range_key()}.rtf"
        self.__save_file(file_name, self.report_rtf.result)


    """
    Проверка работы отчета rtf для nomenclature
    """
    def test_rtf_report_create_nomenclature(self):
        # Действие
        self.report_rtf.create(self.reposity.data[data_reposity.nomenclature_key()])

        # Проверка
        assert self.report_rtf.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.nomenclature_key()}.rtf"
        self.__save_file(file_name, self.report_rtf.result)

    """
    Проверка работы отчета rtf для group
    """
    def test_rtf_report_create_group(self):
        # Действие
        self.report_rtf.create(self.reposity.data[data_reposity.group_key()])

        # Проверка
        assert self.report_rtf.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.group_key()}.rtf"
        self.__save_file(file_name, self.report_rtf.result)

    """
    Проверка работы отчета rtf для recipe
    """
    def test_rtf_report_create_recipe(self):
        # Действие
        self.report_rtf.create(self.reposity.data[data_reposity.recipe_key()])

        # Проверка
        assert self.report_rtf.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.recipe_key()}.rtf"
        self.__save_file(file_name, self.report_rtf.result)

        """
    Проверка десериализации данных из JSON для group
    """
    def test_des_json_group(self):
        # Подготовка
        self.__json_report_create_group()
        file_name = "group.json"
        deserializer = json_deserializer(group_model)
        group_data = self.reposity.data[data_reposity.group_key()]

        # Действие
        objects = deserializer.deserialize(file_name)

        # Проверка
        assert len(objects) != 0

        for i, j in zip(objects, group_data):
            assert i == j

        assert objects[1] != group_data[0]

    """
    Проверка десериализации данных из JSON для range
    """
    def test_des_json_range(self):
        # Подготовка
        self.__json_report_create_range()
        file_name = "range.json"
        deserializer = json_deserializer(range_model)
        range_data = self.reposity.data[data_reposity.range_key()]

        # Действие
        objects = deserializer.deserialize(file_name)

        # Проверка
        assert len(objects) != 0

        for i, j in zip(objects, range_data):
            assert i == j

        assert objects[1] != range_data[0]

    
    """
    Проверка десериализации данных из JSON для nomenclature
    """
    def test_des_json_nomenclature(self):
        # Подготовка
        self.__json_report_create_nomenclature()
        file_name = "nomenclature.json"
        deserializer = json_deserializer(nomenclature_model)
        nomenclature_data = self.reposity.data[data_reposity.nomenclature_key()]

        # Действие
        objects = deserializer.deserialize(file_name)

        # Проверка
        assert len(objects) != 0

        for i, j in zip(objects, nomenclature_data):
            assert i == j

        assert objects[1] != nomenclature_data[0] 

    """
    Проверка десериализации данных из JSON для recipe
    """
    def test_des_json_recipe(self):
        # Подготовка
        self.__json_report_create_recipe()
        file_name = "recipe.json"
        deserializer = json_deserializer(recipe_model)
        recipe_data = self.reposity.data[data_reposity.recipe_key()]

        # Действие
        objects = deserializer.deserialize(file_name)

        # Проверка
        assert len(objects) != 0

        for i, j in zip(objects, recipe_data):
            assert i == j

        assert objects[1] != recipe_data[0] 


if __name__ == '__main__':
    unittest.main() 