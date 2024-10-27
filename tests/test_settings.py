import unittest
from src.manager.settings_manager import settings_manager
from src.models.settings import settings
from src.reports.json_report import json_report
from src.errors.custom_exception import TypeException, RequiredLengthException, ArgumentException

"""
Набор тестов для проверки работы с настройками
"""
class test_settings(unittest.TestCase):
    
   """
   Проверить открытие и загрузку настроек с ошибкой
   """
   def test_settings_manager_open_fail(self):
      # Подготовка
      manager1 = settings_manager()

      # Действие
      result = manager1.open("../123.json")

      # Проверки
      assert manager1.is_error == True

   """
   Проверить открытие и загрузку настроек
   """
   def test_settings_manager_open(self):
      # Подготовка
      manager1 = settings_manager()

      # Действие
      result = manager1.open("../settings.json")

      # Проверки 
      assert result is True

   """
   Проверить работу шаблона singletone
   """
   def test_settings_manager_singletone(self):
      # Подготовка
      manager1 = settings_manager()
      result = manager1.open("../settings.json")

      # Действие
      manager2 = settings_manager()

      # Проверки
      assert manager1.current_settings.inn == manager2.current_settings.inn
      assert manager1.current_settings.organization_name == manager2.current_settings.organization_name   

   """
   Проверить получение класса формата отчета
   """
   def test_get_report_class(self):
      # Подготовка
      manager = settings_manager()

      report_class = manager.get_report_class()

      # Проверки
      assert isinstance(report_class, json_report)
 

   """
   Проверить некорректное имя файла с настройками
   """
   def test_file_name_fail(self):
      # Подготовка
      manager1 = settings_manager()

      with self.assertRaises(TypeException):
            manager1.open(123)

   """
   Проверить некорректный формат отчета
   """
   def test_format_report_fail(self):
      # Подготовка
      manager1 = settings_manager()

      with self.assertRaises(TypeException):
            manager1.get_report_class(123)

   """
   Проверить некорректный тип атрибутов
   """
   def test_type_attributes_fail(self):
      # Подготовка
      sets = settings()

      with self.assertRaises(TypeException):
            sets.inn = 123

      with self.assertRaises(TypeException):
            sets.organization_name = 456

      with self.assertRaises(TypeException):
            sets.account = 123

      with self.assertRaises(TypeException):
            sets.сorrespondent_account = 789

      with self.assertRaises(TypeException):
            sets.bik = 0
            
      with self.assertRaises(TypeException):
            sets.type_property = 543

      with self.assertRaises(TypeException):
            sets.report_format = "kate"

   """
   Проверить некорректную длину атрибутов
   """
   def test_length_attributes_fail(self):
      # Подготовка
      sets = settings()

      with self.assertRaises(RequiredLengthException):
            sets.inn = "12"

      with self.assertRaises(RequiredLengthException):
            sets.account = "56"

      with self.assertRaises(RequiredLengthException):
            sets.сorrespondent_account = "78"

      with self.assertRaises(RequiredLengthException):
            sets.bik = "90"
            
      with self.assertRaises(RequiredLengthException):
            sets.type_property = "qw"

if __name__ == '__main__':
    unittest.main()   

