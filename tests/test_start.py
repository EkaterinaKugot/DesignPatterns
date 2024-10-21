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
        found = list(filter(lambda x: x.name == "гр", reposity.data[data_reposity.range_key()]  ))
        
        # Проверки
        assert len(found) == 1


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

    """
    Проверить создание складов
    """
    def test_start_service_consists_storage(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)
        start.create()

        # Действие
        found = list(filter(lambda x: x.name == "Склад 1", reposity.data[data_reposity.storage_key()]  ))

        # Проверки
        assert len(reposity.data[data_reposity.storage_key()]) > 0
        assert len(found) == 1

    """
    Проверить создание транзакций
    """
    def test_start_service_consists_transaction(self):
        # Подготовка
        set_manager = settings_manager()
        reposity = data_reposity()
        start = start_service(reposity, set_manager)

        # Действие
        start.create()

        # Проверки
        assert len(reposity.data[data_reposity.transaction_key()]) > 0
        assert len(reposity.data[data_reposity.transaction_key()]) == len(reposity.data[data_reposity.nomenclature_key()])
        assert reposity.data[data_reposity.transaction_key()][0].nomenclature == reposity.data[data_reposity.nomenclature_key()][0]

    """
    Проверить создание ключей
    """
    def test_keys(self):
        data = data_reposity()

        assert data.group_key() == "group"
        assert data.nomenclature_key() == "nomenclature"
        assert data.range_key() == "range"
        assert data.recipe_key() == "recipe"

if __name__ == '__main__':
    unittest.main() 








