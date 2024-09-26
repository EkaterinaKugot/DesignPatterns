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
import unittest
import os 

"""
Набор тестов для проверки работы формирования отчетов
"""
class test_reporting(unittest.TestCase):

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
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)
        start.create()

        report = csv_report()

        # Действие
        report.create(reposity.data[data_reposity.range_key()])

        # Проверка
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.range_key()}.csv"
        self.__save_file(file_name, report.result)
    
    """
    Проверка работы отчета CSV для nomenclature
    """
    def test_csv_report_create_nomenclature(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)
        start.create()

        report = csv_report()

        # Действие
        report.create(reposity.data[data_reposity.nomenclature_key()])

        # Проверка
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.nomenclature_key()}.csv"
        self.__save_file(file_name, report.result)

    """
    Проверка работы отчета CSV для group
    """
    def test_csv_report_create_group(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)
        start.create()

        report = csv_report()

        # Действие
        report.create(reposity.data[data_reposity.group_key()])

        # Проверка
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.group_key()}.csv"
        self.__save_file(file_name, report.result)
    
    """
    Проверка работы отчета CSV для recipe
    """
    def test_csv_report_create_recipe(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)
        start.create()

        report = csv_report()

        # Действие
        report.create(reposity.data[data_reposity.recipe_key()])

        # Проверка
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.recipe_key()}.csv"
        self.__save_file(file_name, report.result)


    """
    Проверка работы отчета md для range
    """
    def test_md_report_create_range(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)
        start.create()

        report = md_report()

        # Действие
        report.create(reposity.data[data_reposity.range_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.range_key()}.md"
        self.__save_file(file_name, report.result)

    """
    Проверка работы отчета md для nomenclature
    """
    def test_md_report_create_nomenclature(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)
        start.create()

        report = md_report()

        # Действие
        report.create(reposity.data[data_reposity.nomenclature_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.nomenclature_key()}.md"
        self.__save_file(file_name, report.result)

    """
    Проверка работы отчета md для group
    """
    def test_md_report_create_group(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)
        start.create()

        report = md_report()

        # Действие
        report.create(reposity.data[data_reposity.group_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.group_key()}.md"
        self.__save_file(file_name, report.result)

    """
    Проверка работы отчета md для recipe
    """
    def test_md_report_create_recipe(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)
        start.create()

        report = md_report()

        # Действие
        report.create(reposity.data[data_reposity.recipe_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.recipe_key()}.md"
        self.__save_file(file_name, report.result)

    """
    Проверка работы отчета json для range
    """
    def test_json_report_create_range(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)
        start.create()

        report = json_report()

        # Действие
        report.create(reposity.data[data_reposity.range_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.range_key()}.json"
        self.__save_file(file_name, report.result)


    """
    Проверка работы отчета json для nomenclature
    """
    def test_json_report_create_nomenclature(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)
        start.create()

        report = json_report()

        # Действие
        report.create(reposity.data[data_reposity.nomenclature_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.nomenclature_key()}.json"
        self.__save_file(file_name, report.result)

    """
    Проверка работы отчета json для group
    """
    def test_json_report_create_group(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)
        start.create()

        report = json_report()

        # Действие
        report.create(reposity.data[data_reposity.group_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.group_key()}.json"
        self.__save_file(file_name, report.result)

    """
    Проверка работы отчета json для recipe
    """
    def test_json_report_create_recipe(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)
        start.create()

        report = json_report()

        # Действие
        report.create(reposity.data[data_reposity.recipe_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.recipe_key()}.json"
        self.__save_file(file_name, report.result)

    """
    Проверка работы отчета xml для range
    """
    def test_xml_report_create_range(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)
        start.create()

        report = xml_report()

        # Действие
        report.create(reposity.data[data_reposity.range_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.range_key()}.xml"
        self.__save_file(file_name, report.result)


    """
    Проверка работы отчета xml для nomenclature
    """
    def test_xml_report_create_nomenclature(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)
        start.create()

        report = xml_report()

        # Действие
        report.create(reposity.data[data_reposity.nomenclature_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.nomenclature_key()}.xml"
        self.__save_file(file_name, report.result)

    """
    Проверка работы отчета xml для group
    """
    def test_xml_report_create_group(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)
        start.create()

        report = xml_report()

        # Действие
        report.create(reposity.data[data_reposity.group_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.group_key()}.xml"
        self.__save_file(file_name, report.result)

    """
    Проверка работы отчета xml для recipe
    """
    def test_xml_report_create_recipe(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)
        start.create()

        report = xml_report()

        # Действие
        report.create(reposity.data[data_reposity.recipe_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.recipe_key()}.xml"
        self.__save_file(file_name, report.result)

    """
    Проверка работы отчета rtf для range
    """
    def test_rtf_report_create_range(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)
        start.create()

        report = rtf_report()

        # Действие
        report.create(reposity.data[data_reposity.range_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.range_key()}.rtf"
        self.__save_file(file_name, report.result)


    """
    Проверка работы отчета rtf для nomenclature
    """
    def test_rtf_report_create_nomenclature(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)
        start.create()

        report = rtf_report()

        # Действие
        report.create(reposity.data[data_reposity.nomenclature_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.nomenclature_key()}.rtf"
        self.__save_file(file_name, report.result)

    """
    Проверка работы отчета rtf для group
    """
    def test_rtf_report_create_group(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)
        start.create()

        report = rtf_report()

        # Действие
        report.create(reposity.data[data_reposity.group_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.group_key()}.rtf"
        self.__save_file(file_name, report.result)

    """
    Проверка работы отчета rtf для recipe
    """
    def test_rtf_report_create_recipe(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)
        start.create()

        report = rtf_report()

        # Действие
        report.create(reposity.data[data_reposity.recipe_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.recipe_key()}.rtf"
        self.__save_file(file_name, report.result)




if __name__ == '__main__':
    unittest.main() 