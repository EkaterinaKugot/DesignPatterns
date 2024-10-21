import unittest
from src.models.recipe import recipe_model
from src.manager.recipe_manager import recipe_manager
from src.models.nomenclature import nomenclature_model
from src.manager.settings_manager import settings_manager
from src.start_service import start_service
from src.data_reposity import data_reposity

from src.errors.custom_exception import ArgumentException, TypeException, PermissibleLengthException
from src.errors.custom_exception import MorePermissibleValueException, RequiredLengthException, EmptyArgumentException

class test_recipe(unittest.TestCase):

    set_manager = settings_manager()
    reposity = data_reposity()
    start = start_service(reposity, set_manager)
    start.create()

    groups = reposity.data[data_reposity.group_key()]
    ranges = reposity.data[data_reposity.range_key()]
    def_nomenclatures = start.nomenclatures

    """
    Проверить создание рецепта
    """
    def test_recipe_manager(self):
        file_name = "recipe1.md" 
        manager1 = recipe_manager(self.groups, self.ranges)
        manager1.open(file_name, self.def_nomenclatures)

        assert len(manager1.recipe.nomenclatures) > 0
        assert manager1.recipe.nomenclatures[0][0].full_name == "Пшеничная мука"
        assert manager1.recipe.nomenclatures[0][0].range.name == "гр"
        assert manager1.recipe.nomenclatures[0][0].range.conversion_factor == 1
        assert manager1.recipe.nomenclatures[0][0].group.name == "Сырье"
        assert manager1.recipe.nomenclatures[0][1] == 100
        assert manager1.recipe.number_servings == 10
        assert manager1.recipe.cooking_time == "20 мин"
        assert len(manager1.recipe.cooking_steps) != 0

    """
    Проверить некорректное имя файла/директории при извлечении данных из рецептов
    """
    def test_invalid_file_dir_name(self):
        manager1 = recipe_manager(self.groups, self.ranges)
        with self.assertRaises(TypeException):
            manager1.open(123, self.def_nomenclatures)  

        with self.assertRaises(EmptyArgumentException):
            manager1.open("", self.def_nomenclatures)  

        with self.assertRaises(TypeException):
            manager1.recipe_directory = 567 

        with self.assertRaises(EmptyArgumentException):
            manager1.recipe_directory = ""

        with self.assertRaises(TypeException):
            recipe_manager(123, self.ranges)

        with self.assertRaises(TypeException):
            recipe_manager(self.groups, 123)

    """
    Проверить некорректные атрибуты recipe_model
    """
    def test_incorrect_arguments_recipe_model(self):
        rec = recipe_model()

        with self.assertRaises(TypeException):
            rec.nomenclatures = 123

        with self.assertRaises(TypeException):
            rec.nomenclatures = [456]
        
        with self.assertRaises(TypeException):
            rec.nomenclatures = [1, 1]

        with self.assertRaises(TypeException):
            rec.nomenclatures = [nomenclature_model(), 1]

        with self.assertRaises(TypeException):
            rec.number_servings = "45"

        with self.assertRaises(TypeException):
            rec.cooking_time = 999

        with self.assertRaises(EmptyArgumentException):
            rec.cooking_time = ""

        with self.assertRaises(TypeException):
            rec.cooking_steps = 44

        with self.assertRaises(EmptyArgumentException):
            rec.cooking_steps = ""

    """
    Проверить создание списка номенклатур по всем рецептам
    """
    def test_list_nomenclatures_all_recipes(self):
        list1 = recipe_manager(self.groups, self.ranges).creating_list_nomenclatures_all_recipes()

        assert len(list1) != 0

        for n in list1:
            assert isinstance(n[0], nomenclature_model)
            assert isinstance(n[1], int)


if __name__ == '__main__':
    unittest.main() 