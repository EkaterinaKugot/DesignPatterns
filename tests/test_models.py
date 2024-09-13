import unittest
from src.models.nomenclature_model import nomenclature
from src.models.range_model import range
from src.models.group_nomenclature_model import group_nomenclature
from src.models.storage_model import storage
from src.models.organization_model import organization
from src.settings_manager import settings_manager

class test_models(unittest.TestCase):

   """
   Проверить варианты сравнения
   """
   def test_equal(self):
      # Подготовка
      n1 = nomenclature()
      n1.full_name = "test1"

      n2 = nomenclature()
      n2.full_name = "test1"

      g_n1 = group_nomenclature()
      g_n1.name = "g_n"

      g_n2 = group_nomenclature()
      g_n2.name = "g_n"

      st1 = storage()
      st2 = storage()

      range1 = range()
      range1.name = "1"
      range2 = range()
      range2.name = "1"
      
      # Проверка
      assert n1 != n2 # Сравнение по id с full_name
      assert g_n1 != g_n2 # Сравнение по id с name
      assert st1 != st2 # Сравнение по id без name
      assert range1 == range2 # Сравнение по name


   """
   Проверить создание range_model
   """
   def test_range_model(self):
      # Подготовка
      base_range = range("грамм", 1)
      new_range = range("кг", 1000, base_range)

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
      company = organization(manager.current_settings)

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
      n1 = nomenclature()
      n1.full_name = "test1"
      n1.range = range("кг", 500, range())

      # Проверка
      assert n1.full_name == "test1"
      assert n1.range.unit_name == "кг" and n1.range.conversion_factor == 500
      assert n1.range.base_range.unit_name == "грамм" and n1.range.base_range.conversion_factor == 1





