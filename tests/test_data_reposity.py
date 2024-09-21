import unittest
from src.data_reposity import data_reposity

class test_data_reposity(unittest.TestCase):
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