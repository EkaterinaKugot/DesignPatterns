import unittest
from src.models.nomenclature import nomenclature_model
from src.models.range import range_model
from src.models.group import group_model
from src.models.storage import storage_model
from src.models.organization import organization_model
from src.manager.nomenclature_manager import nomenclature_manager

from src.manager.settings_manager import settings_manager

from src.errors.custom_exception import ArgumentException, TypeException, PermissibleLengthException
from src.errors.custom_exception import PermissibleValueException, RequiredLengthException, EmptyArgumentException

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
      assert range1 != range2 # Сравнение по id


   """
   Проверить создание range_model
   """
   def test_range_model(self):
      # Подготовка
      base_range = range_model.create("гр", 1)
      new_range = range_model.create("кг", 1000, base_range)

      # Проверка
      assert new_range.name == "кг" and new_range.conversion_factor == 1000
      assert new_range.base_range.name == "гр" and new_range.base_range.conversion_factor == 1

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
      base_range = range_model.create("гр", 1)
      n1.range = range_model.create("кг", 500, base_range)

      # Проверка
      assert n1.full_name == "test1"
      assert n1.range.name == "кг" and n1.range.conversion_factor == 500
      assert n1.range.base_range.name == "гр" and n1.range.base_range.conversion_factor == 1 

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
         range_model().name = 123

      with self.assertRaises(TypeException):
         range_model().conversion_factor = "qwer"

      base_range = range_model.create("грамм", 1000)
      with self.assertRaises(PermissibleValueException):
         range_model.create("кг", 1, base_range)


   """
   Проверить некорректный коэффициентом пересчета range_model
   """
   def test_conversion_factor_range_fail(self):
      base_range = range_model.create("грамм", 1000)
      
      with self.assertRaises(PermissibleValueException):
         new_range = range_model.create("кг", 1, base_range)

   """
   Проверка создания nomenclature в nomenclature_model
   """
   def test_create_nomenclature(self):
      # Подготовка
      ingredient = "Ванилин"
      nomenclature = nomenclature_manager.create(ingredient, range_model.create("гр", 5))

      assert isinstance(nomenclature, nomenclature_model)
      assert nomenclature.full_name == ingredient
      assert nomenclature.group.name == "Сырье"
      assert nomenclature.range.name == "гр"
      assert nomenclature.range.conversion_factor == 5


if __name__ == '__main__':
    unittest.main() 





