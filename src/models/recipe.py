from src.core.base_model import base_model_name
from src.errors.validator import Validator
from src.models.nomenclature import nomenclature_model
import os
import re

"""
Модель рецепта
"""
class recipe_model(base_model_name):
    __nomenclatures: list[nomenclature_model] = None
    __number_servings: int = 0
    __cooking_time: str = None
    __cooking_steps: str = None

    def __init__(self, file_name: str = "") -> None:
        Validator.validate_type("file_name", file_name, str)
        if len(file_name) != 0:
            self.file_name = file_name
            ingredients, gram = nomenclature_model.extract_columns_from_table(file_name)
            self.__nomenclatures = nomenclature_model.create_list_nomenclature(ingredients, gram)
            data_recipe = self.__get_data_recipe(file_name)
            fields = dir(recipe_model)
            for key in data_recipe.keys():
                if key in fields:
                    self.__setattr__(key, data_recipe[key])


    def __get_data_recipe(self, file_name: str) -> dict:
        directory: str = "./src/docs"
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
                recipe_text = file.read()

        name_pattern = re.compile(r'^#\s*(.*)', re.MULTILINE)
        servings_pattern = re.compile(r'(\d+)\s*порций')
        time_pattern = re.compile(r'Время приготовления:\s*`(\d+ мин)`')
        steps_pattern = re.compile(r'\d+\.\s*(.*?)(?=\n\d+\.|$)', re.DOTALL)

        name_match = name_pattern.search(recipe_text)
        servings_match = servings_pattern.search(recipe_text)
        time_match = time_pattern.search(recipe_text)
        steps_match = steps_pattern.findall(recipe_text)

        name = str(name_match.group(1)) if name_match else "Не найдено"
        servings = int(servings_match.group(1)) if servings_match else 0
        time = str(time_match.group(1)) if time_match else "Не указано"
        steps = ' '.join(steps_match).replace('\n', ' ').strip() if steps_match else "Не указано"

        return {
            'name': name,
            'number_servings': servings,
            'cooking_time': time,
            'cooking_steps': steps
        }
    

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
            Validator.validate_type("nomenclatures", n, nomenclature_model)
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
