from src.manager.settings_manager import settings_manager
from src.start_service import start_service
from src.data_reposity import data_reposity
import unittest


"""
Набор тестов для проверки работы старта приложения
"""
class test_start(unittest.TestCase):
    
    """
    Проверить создание инстанса start_service
    """
    def test_create_start_service(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)

        # Проверки
        assert start is not None

    """
    Проверить генерацию стартовых элементов системы
    """
    def test_start_service_create(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)

        # Действие
        result = start.create()

        # Проверки
        assert start is not None
        assert result == True
        assert start.is_error == False

    """
    Проверить состав стартовых элементов
    """
    def test_start_service_consists_range(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)
        start.create()

        # Действие
        found = list(filter(lambda x: x.unit_name == "гр", reposity.data[data_reposity.range_key()]  ))
        print(found)
        # Проверки
        assert len(found) > 1


    """
    Проверить состав стартовых элементов
    """
    def test_start_service_consists_nomenclature(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)
        start.create()

        # Действие
        found = list(filter(lambda x: x.full_name == "Пшеничная мука", reposity.data[data_reposity.nomenclature_key()]  ))

        # Проверки
        assert len(found) > 1    
        assert found[0].range is not None
        assert found[0].group is not None











