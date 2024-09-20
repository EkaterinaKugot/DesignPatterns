import unittest
from src.models.nomenclature import nomenclature_model
from src.models.range import range_model
from src.models.group import group_model
from src.models.storage import storage_model
from src.models.organization import organization_model
from src.models.recipe import recipe_model

from src.settings_manager import settings_manager

from src.errors.custom_exception import ArgumentException, TypeException, PermissibleLengthException
from src.errors.custom_exception import PermissibleValueException, RequiredLengthException, EmptyLengthException

class test_models(unittest.TestCase):

   """
   Проверить варианты сравнения
   """
   def test_equal(self):
      # Подготовка
      n1 = nomenclature_model()
      n1.full_name = "test1"

      n2 = nomenclature_model()
      n2.full_name = "test1"

      g_n1 = group_model()
      g_n1.name = "g_n1"

      g_n2 = group_model()
      g_n2.name = "g_n2"

      st1 = storage_model()
      st1.name = "123"
      st2 = storage_model()
      st2.name = "123"

      range1 = range_model()
      range1.name = "1"
      range2 = range_model()
      range2.name = "1"
      
      # Проверка
      assert n1 != n2 # Сравнение по id с full_name
      assert g_n1 != g_n2 # Сравнение неравных name
      assert st1 != st2 # Сравнение по id name
      assert range1 == range2 # Сравнение равных name


   """
   Проверить создание range_model
   """
   def test_range_model(self):
      # Подготовка
      base_range = range_model("грамм", 1)
      new_range = range_model("кг", 1000, base_range)

      # Проверка
      assert new_range.unit_name == "кг" and new_range.conversion_factor == 1000
      assert new_range.base_range.unit_name == "грамм" and new_range.base_range.conversion_factor == 1

   """
   Проверить создание organization_model
   """
   def test_organization_model(self):
      # Подготовка
      manager = settings_manager()
      manager.open("settings.json")
      company = organization_model(manager.current_settings)

      # Проверка
      assert company.inn == manager.current_settings.inn
      assert company.bik == manager.current_settings.bik
      assert company.account == manager.current_settings.account
      assert company.type_property == manager.current_settings.type_property

   """
   Проверить создание nomenclature_model
   """
   def test_nomenclature_model(self):
      # Подготовка
      n1 = nomenclature_model()
      n1.full_name = "test1"
      n1.range = range_model("кг", 500, range_model())

      # Проверка
      assert n1.full_name == "test1"
      assert n1.range.unit_name == "кг" and n1.range.conversion_factor == 500
      assert n1.range.base_range.unit_name == "грамм" and n1.range.base_range.conversion_factor == 1 
   
   """
   Проверить извлечение данных из таблицы markdown
   """
   def test_extract_columns_from_table(self):
      file_name = "recipe1.md" 
      ingredients, gram = nomenclature_model.extract_columns_from_table(file_name)

      test_ingredients = ["Пшеничная мука", "Сахар", "Сливочное масло", "Яйцо", "Ванилин"]
      test_gram = [[100, "гр"], [80, "гр"], [70, "гр"], [1, "шт"], [5, "гр"],]

      assert len(ingredients) != 0 
      assert len(gram) != 0 
      assert len(gram) == len(ingredients)
      assert ingredients == test_ingredients
      assert gram == test_gram 

   """
   Проверить создание спика номенклатур
   """
   def test_create_list_nomenclature(self):
      ingredients, gram = nomenclature_model.process_markdown_files()

      assert len(ingredients) != 0 
      assert len(gram) != 0 
      assert len(gram) == len(ingredients)

      list1 = nomenclature_model.create_list_nomenclature(ingredients, gram)

      assert len(list1) != 0
      assert isinstance(list1, list)

      for nom in list1:
          assert isinstance(nom, nomenclature_model)

   """
   Проверить статические методы group_model
   """
   def test_staticmethod_group_model(self):
      group1 = group_model.default_group_source()
      group2 = group_model.default_group_cold()

      assert isinstance(group1, group_model)
      assert isinstance(group2, group_model)

      assert group1.name == "Сырье"
      assert group2.name == "Заморозка"

   """
   Проверить создание recipe_model
   """
   def test_recipe_model(self):
      rec = recipe_model("recipe2.md")

      assert len(rec.nomenclatures) != 0
      for nom in rec.nomenclatures:
          assert isinstance(nom, nomenclature_model)

      nom0 = rec.nomenclatures[0]
      assert nom0.full_name == "Пшеничная мука"
      assert nom0.group.name == "Сырье"
      assert nom0.range.unit_name == "гр" and nom0.range.conversion_factor == 250

      assert rec.number_servings == 12
      assert rec.cooking_time == "30 мин"
      assert len(rec.cooking_steps) != 0

   
   """
   Проверить создание пустого recipe_model
   """
   def test_empty_recipe_model(self):
      rec = recipe_model("")

      assert rec.nomenclatures is None
      assert rec.number_servings == 0
      assert rec.cooking_time is None
      assert rec.cooking_steps is None


   """
   Проверить некорректные типы у атрибутов nomenclature_model
   """
   def test_type_nomenclature_fail(self):
      # Подготовка
      n1 = nomenclature_model()

      with self.assertRaises(TypeException):
            n1.full_name = 123
      
      with self.assertRaises(TypeException):
            n1.name = 567

      with self.assertRaises(TypeException):
            n1.group = 890

      with self.assertRaises(TypeException):
            n1.range = "wert"

   """
   Проверить некорректную длину у атрибутов nomenclature_model
   """
   def test_length_nomenclature_fail(self):
      # Подготовка
      n1 = nomenclature_model()

      with self.assertRaises(PermissibleLengthException):
            n1.full_name = "e" * 256
      
      with self.assertRaises(PermissibleLengthException):
            n1.name = "t" * 100

   """
   Проверить некорректный тип у атрибутов range_model
   """
   def test_type_range_fail(self):
      with self.assertRaises(TypeException):
         base_range = range_model(678, 1)

      with self.assertRaises(TypeException):
         base_range = range_model("грамм", "ooo")

   """
   Проверить некорректный коэффициентом пересчета range_model
   """
   def test_conversion_factor_range_fail(self):
      base_range = range_model("грамм", 1000)
      
      with self.assertRaises(PermissibleValueException):
          new_range = range_model("кг", 1, base_range)

   """
   Проверить некорректное имя файла/директории при извлечении данных из рецептов
   """
   def test_invalid_file_name(self):
      with self.assertRaises(TypeException):
         c1, c2 = nomenclature_model.extract_columns_from_table(123)

      with self.assertRaises(TypeException):
         c1, c2 = nomenclature_model.extract_columns_from_table("recipe1.md", 340)

      with self.assertRaises(EmptyLengthException):
         c1, c2 = nomenclature_model.extract_columns_from_table("")

      with self.assertRaises(EmptyLengthException):
         c1, c2 = nomenclature_model.extract_columns_from_table("recipe1.md", "")

      with self.assertRaises(TypeException):
         c1, c2 = nomenclature_model.process_markdown_files(123)

      with self.assertRaises(EmptyLengthException):
         c1, c2 = nomenclature_model.process_markdown_files("")

      with self.assertRaises(TypeException):
         recipe_model(789)

   """
   Проверить некорректные аргументы при создании списка номенклатур
   """
   def test_incorrect_arguments_list_nomenclature(self):
      cor_ingredients = ["Яйцо"]
      cor_gram = [[100, "гр"]]

      incor_ingredients = [567]
      incor_gram1 = [[dict(), "гр"]]
      incor_gram2 = [[1, dict()]]

      with self.assertRaises(TypeException):
         c1, c2 = nomenclature_model.create_list_nomenclature(incor_ingredients, cor_gram)
      
      with self.assertRaises(TypeException):
         c1, c2 = nomenclature_model.create_list_nomenclature(cor_ingredients, incor_gram1)

      with self.assertRaises(TypeException):
         c1, c2 = nomenclature_model.create_list_nomenclature(cor_ingredients, incor_gram2)

   """
   Проверить некорректные атрибуты recipe_model
   """
   def test_incorrect_arguments_recipe_model(self):
      rec = recipe_model("")

      with self.assertRaises(TypeException):
         rec.nomenclatures = 123

      with self.assertRaises(TypeException):
         rec.nomenclatures = [456]

      with self.assertRaises(TypeException):
         rec.number_servings = "45"

      with self.assertRaises(TypeException):
         rec.cooking_time = 999

      with self.assertRaises(EmptyLengthException):
         rec.cooking_time = ""

      with self.assertRaises(TypeException):
         rec.cooking_steps = 44

      with self.assertRaises(EmptyLengthException):
         rec.cooking_steps = ""


if __name__ == '__main__':
    unittest.main() 





