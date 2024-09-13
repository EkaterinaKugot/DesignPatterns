import unittest
from src.models.nomenclature_model import nomenclature
from src.models.range_model import range

class test_nomenclature(unittest.TestCase):

   """
   Проверить вариант сравнения (по коду)
   """
   def test_nomenclature_model(self):
      item1 = nomenclature()
      item1.name = "test1"

      item2 = nomenclature()
      item2.name = "test1"
      print(item1.id, item2.id)

      # Проверка
      assert item1 != item2


   """
   Проверить вариант сравнения (по наименованию)
   """
   def test_range_model(self):
      range1 = range()
      range1.name = "1"
      range2 = range()
      range2.name = "1"

      assert range1 == range2