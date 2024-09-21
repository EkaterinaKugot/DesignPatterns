import unittest
from src.nomenclature_manager import nomenclature_manager
from src.models.nomenclature import nomenclature_model
from src.models.range import range_model

class test_nomenclature(unittest.TestCase):
    """
    Проверка создания nomenclature в nomenclature_model
    """
    def test_create_nomenclature(self):
        # Подготовка
        ingredient = "Ванилин"
        nomenclature = nomenclature_manager.create(ingredient, range_model("гр", 5))

        assert isinstance(nomenclature, nomenclature_model)
        assert nomenclature.full_name == ingredient
        assert nomenclature.group.name == "Сырье"
        assert nomenclature.range.unit_name == "гр"
        assert nomenclature.range.conversion_factor == 5

if __name__ == '__main__':
    unittest.main()