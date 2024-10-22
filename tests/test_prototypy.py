import unittest
from src.logics.filter_prototype import filter_prototype
from src.dto.filter import filter
from src.start_service import start_service
from src.data_reposity import data_reposity
from src.core.filter_type import filter_type
from src.manager.settings_manager import settings_manager

"""
Набор тестов для фильтрации
"""
class test_prototypy(unittest.TestCase):

    set_manager = settings_manager()
    reposity = data_reposity()
    start = start_service(reposity, set_manager)
    start.create()

    """
    Проверка фильтрации номенклатур по равенсту id
    """
    def test_id_equale(self):
        # Подготовка
        if len(self.reposity.data[data_reposity.nomenclature_key()]) == 0:
            raise Exception("Нет данных!") 
        
        data = self.reposity.data[data_reposity.nomenclature_key()]
        item = data[0]

        item_filter = filter()
        item_filter.id = str(item.id)
        prototype = filter_prototype(data)

        # Действие
        prototype.create(item_filter)

        # Проверка
        assert len(prototype.data) == 1
        assert prototype.data[0] == item

    """
    Проверка фильтрации номенклатур по вхождению в id
    """
    def test_id_like(self):
        # Подготовка
        if len(self.reposity.data[data_reposity.nomenclature_key()]) == 0:
            raise Exception("Нет данных!") 
        
        data = self.reposity.data[data_reposity.nomenclature_key()]
        item = data[0]

        item_filter = filter()
        item_filter.id = str(item.id)[:3]
        item_filter.type_filter_id = filter_type.LIKE
        prototype = filter_prototype(data)

        # Действие
        prototype.create(item_filter)

        # Проверка
        assert len(prototype.data) >= 1
        assert prototype.data[0] == item

    """
    Проверка фильтрации номенклатур по равенсту имени
    """
    def test_nomenclature_name_equale(self):
        # Подготовка
        if len(self.reposity.data[data_reposity.nomenclature_key()]) == 0:
            raise Exception("Нет данных!") 
        
        data = self.reposity.data[data_reposity.nomenclature_key()]
        item = data[0]

        item_filter = filter()
        item_filter.name = item.full_name
        prototype = filter_prototype(data)

        # Действие
        prototype.create(item_filter)

        # Проверка
        assert len(prototype.data) == 1
        assert prototype.data[0] == item

    """
    Проверка фильтрации номенклатур по вхождению в имя
    """
    def test_nomenclature_name_like(self):
        # Подготовка
        if len(self.reposity.data[data_reposity.nomenclature_key()]) == 0:
            raise Exception("Нет данных!") 
        
        data = self.reposity.data[data_reposity.nomenclature_key()]

        item_filter = filter()
        item_filter.name = "чн"
        item_filter.type_filter_name = filter_type.LIKE
        prototype = filter_prototype(data)

        # Действие
        prototype.create(item_filter)

        # Проверка
        assert len(prototype.data) > 1

    
    """
    Проверка фильтрации групп номенклатур по равенсту имени
    """
    def test_group_name_equale(self):
        # Подготовка
        if len(self.reposity.data[data_reposity.group_key()]) == 0:
            raise Exception("Нет данных!") 
        
        data = self.reposity.data[data_reposity.group_key()]
        item = data[0]

        item_filter = filter()
        item_filter.name = item.name
        prototype = filter_prototype(data)

        # Действие
        prototype.create(item_filter)

        # Проверка
        assert len(prototype.data) == 1
        assert prototype.data[0] == item

    """
    Проверка фильтрации групп номенклатур по вхождению в имя
    """
    def test_group_name_like(self):
        # Подготовка
        if len(self.reposity.data[data_reposity.group_key()]) == 0:
            raise Exception("Нет данных!") 
        
        data = self.reposity.data[data_reposity.group_key()]

        item_filter = filter()
        item_filter.name = "р"
        item_filter.type_filter_name = filter_type.LIKE
        prototype = filter_prototype(data)

        # Действие
        prototype.create(item_filter)

        # Проверка
        assert len(prototype.data) >= 1

    """
    Проверка фильтрации единиц измерения по равенсту имени
    """
    def test_range_name_equale(self):
        # Подготовка
        if len(self.reposity.data[data_reposity.range_key()]) == 0:
            raise Exception("Нет данных!") 
        
        data = self.reposity.data[data_reposity.range_key()]
        item = data[0]

        item_filter = filter()
        item_filter.name = item.name
        prototype = filter_prototype(data)

        # Действие
        prototype.create(item_filter)

        # Проверка
        assert len(prototype.data) == 2
        assert prototype.data[0] == item

    """
    Проверка фильтрации единиц измерения по вхождению в имя
    """
    def test_range_name_like(self):
        # Подготовка
        if len(self.reposity.data[data_reposity.range_key()]) == 0:
            raise Exception("Нет данных!") 
        
        data = self.reposity.data[data_reposity.range_key()]

        item_filter = filter()
        item_filter.name = "ш"
        item_filter.type_filter_name = filter_type.LIKE
        prototype = filter_prototype(data)

        # Действие
        prototype.create(item_filter)

        # Проверка
        assert len(prototype.data) == 1

    """
    Проверка фильтрации рецептов по равенсту имени
    """
    def test_recipe_name_equale(self):
        # Подготовка
        if len(self.reposity.data[data_reposity.recipe_key()]) == 0:
            raise Exception("Нет данных!") 
        
        data = self.reposity.data[data_reposity.recipe_key()]
        item = data[0]

        item_filter = filter()
        item_filter.name = item.name
        prototype = filter_prototype(data)

        # Действие
        prototype.create(item_filter)

        # Проверка
        assert len(prototype.data) == 1
        assert prototype.data[0] == item

    """
    Проверка фильтрации рецептов по вхождению в имя
    """
    def test_recipe_name_like(self):
        # Подготовка
        if len(self.reposity.data[data_reposity.recipe_key()]) == 0:
            raise Exception("Нет данных!") 
        
        data = self.reposity.data[data_reposity.recipe_key()]

        item_filter = filter()
        item_filter.name = "НИ"
        item_filter.type_filter_name = filter_type.LIKE
        prototype = filter_prototype(data)

        # Действие
        prototype.create(item_filter)

        # Проверка
        assert len(prototype.data) == 2
    