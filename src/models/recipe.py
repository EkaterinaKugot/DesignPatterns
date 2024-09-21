from src.core.base_model import base_model_name
from src.errors.validator import Validator
from src.models.nomenclature import nomenclature_model

"""
Модель рецепта
"""
class recipe_model(base_model_name):
    __nomenclatures: list[nomenclature_model] = None
    __number_servings: int = 0
    __cooking_time: str = None
    __cooking_steps: str = None

    """
    Номенклатуры
    """
    @property
    def nomenclatures(self) -> nomenclature_model:
        return self.__nomenclatures
    
    @nomenclatures.setter
    def nomenclatures(self, nomenclatures: list[nomenclature_model]):
        Validator.validate_type("nomenclatures", nomenclatures, list)
        for n in nomenclatures:
            Validator.validate_type("nomenclature", n, nomenclature_model)
        self.__nomenclatures = nomenclatures

    """
    Количество порций
    """
    @property
    def number_servings(self) -> int:
        return self.__number_servings
    
    @number_servings.setter
    def number_servings(self, number_servings: int):
        Validator.validate_type("number_servings", number_servings, int)
        self.__number_servings = number_servings

    """
    Время приготовления
    """
    @property
    def cooking_time(self) -> str:
        return self.__cooking_time
    
    @cooking_time.setter
    def cooking_time(self, cooking_time: str):
        Validator.validate_type("cooking_time", cooking_time, str)
        Validator.validate_empty_length("cooking_time", cooking_time)
        self.__cooking_time = cooking_time

    """
    Шаги приготовления
    """
    @property
    def cooking_steps(self) -> str:
        return self.__cooking_steps
    
    @cooking_steps.setter
    def cooking_steps(self, cooking_steps: str):
        Validator.validate_type("cooking_steps", cooking_steps, str)
        Validator.validate_empty_length("cooking_steps", cooking_steps)
        self.__cooking_steps = cooking_steps
