import unittest
from src.models.recipe import recipe_model
from src.manager.recipe_manager import recipe_manager
from src.models.nomenclature import nomenclature_model

from src.errors.custom_exception import ArgumentException, TypeException, PermissibleLengthException
from src.errors.custom_exception import MorePermissibleValueException, RequiredLengthException, EmptyArgumentException

class test_recipe(unittest.TestCase):

    """
    Проверить создание рецепта
    """
    def test_recipe_manager(self):
        file_name = "recipe1.md" 
        manager1 = recipe_manager()
        manager1.open(file_name)

        assert len(manager1.recipe.nomenclatures) != 0
        assert manager1.recipe.nomenclatures[0].full_name == "Пшеничная мука"
        assert manager1.recipe.nomenclatures[0].range.name == "гр"
        assert manager1.recipe.nomenclatures[0].range.conversion_factor == 100
        assert manager1.recipe.nomenclatures[0].group.name == "Сырье"
        assert manager1.recipe.number_servings == 10
        assert manager1.recipe.cooking_time == "20 мин"
        assert len(manager1.recipe.cooking_steps) != 0

    """
    Проверить некорректное имя файла/директории при извлечении данных из рецептов
    """
    def test_invalid_file_dir_name(self):
        manager1 = recipe_manager()
        with self.assertRaises(TypeException):
            manager1.open(123)  

        with self.assertRaises(EmptyArgumentException):
            manager1.open("")  

        with self.assertRaises(TypeException):
            manager1.recipe_directory = 567 

        with self.assertRaises(EmptyArgumentException):
            manager1.recipe_directory = ""

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
        list1 = recipe_manager().creating_list_nomenclatures_all_recipes()

        assert len(list1) != 0

        for n in list1:
            assert isinstance(n, nomenclature_model)


if __name__ == '__main__':
    unittest.main() 