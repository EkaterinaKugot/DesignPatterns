import unittest
from src.settings_manager import settings_manager

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
       print(manager1.error_text)
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

       

if __name__ == '__main__':
    unittest.main()   

