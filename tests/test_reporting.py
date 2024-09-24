from src.start_service import start_service
from src.data_reposity import data_reposity
from src.reports.csv_report import csv_report
from src.reports.report_factory import report_factory
from src.core.format_reporting import format_reporting
from src.reports.md_report import md_report
from src.manager.settings_manager import settings_manager
import unittest

"""
Набор тестов для проверки работы формирования отчетов
"""
class test_reporting(unittest.TestCase):

    """
    Проверка работы отчета CSV
    """
    def test_csv_report_create(self):
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
    
    """
    Проверка работы отчета CSV
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

    def test_report_factory_create(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)
        start.create()

        # Действие
        report = report_factory().create(format_reporting.CSV)

        # Проверка
        assert report is not None
        assert isinstance(report, csv_report)

    """
    Проверка работы отчета md
    """
    def test_md_report_create_nomenclature(self):
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


if __name__ == '__main__':
    unittest.main() 