from src.models.recipe import recipe_model
from src.models.nomenclature import nomenclature_model
from src.manager.nomenclature_manager import nomenclature_manager
from src.core.abstract_logic import abstract_logic
from src.models.group import group_model
from src.models.range import range_model
from src.errors.validator import Validator
from src.errors.custom_exception import ArgumentException
from src.core.abstract_report import abstract_report
from src.core.evet_type import event_type
import os
import re

class recipe_manager(abstract_logic):
    __recipe_directory: str = "./src/docs"

    def __init__(self, groups: list[group_model], ranges: list[range_model]) -> None:
        Validator.validate_type("groups", groups, list)
        Validator.validate_empty_argument("groups", groups)
        Validator.validate_type("ranges", ranges, list)
        Validator.validate_empty_argument("ranges", ranges)

        self.__recipe: recipe_model = recipe_model()
        self.groups = groups
        self.ranges = ranges

    """
    Рецепт
    """
    @property
    def recipe(self) -> recipe_model:
        return self.__recipe
    
    """
    Путь к рецептам
    """
    @property
    def recipe_directory(self) -> str:
        return self.__recipe_directory
    
    @recipe_directory.setter
    def recipe_directory(self, recipe_directory: str):
        Validator.validate_type("recipe_directory", recipe_directory, str)
        Validator.validate_empty_argument("recipe_directory", recipe_directory)
        self.__recipe_directory = recipe_directory

    def open(self, file_name: str, def_nomenclatures: list[list[nomenclature_model, int]]) -> None:
        Validator.validate_type("file_name", file_name, str)
        Validator.validate_empty_argument("file_name", file_name)

        ingredients, gram = self.__extract_columns_from_table(file_name)

        list = self.__create_list_nomenclature(ingredients, gram, def_nomenclatures)
        self.recipe.nomenclatures = list

        data_recipe = self.__get_data_recipe(file_name)

        fields = abstract_report.get_class_fields(recipe_model, True)
        for key in data_recipe.keys():
            if key in fields:
                self.recipe.__setattr__(key, data_recipe[key])

    """
    Функция для извлечения данных из таблицы markdown
    """
    def __extract_columns_from_table(
        self,
        file_name: str
    ) -> list[list[str], list[list[int, str]]]:
        file_path = os.path.join(self.recipe_directory, file_name)

        with open(file_path, 'r', encoding='utf-8') as file:
                content = file.readlines()

        table_lines = [line for line in content if '|' in line]
        
        if len(table_lines) < 3:
            return [], []
        
        data_lines = table_lines[2:]
        column1 = []
        column2 = []

        for line in data_lines:
            columns = re.split(r'\s*\|\s*', line.strip('| \n'))
            if len(columns) >= 2:
                column1.append(columns[0])

                gram = []
                tmp_gram = columns[1].split(" ")
                if tmp_gram[0].isdigit():
                    gram.append(int(tmp_gram[0]))
                else:
                    raise ArgumentException("tmp_gram[0]", tmp_gram[0])
                gram.append(tmp_gram[1])

                column2.append(gram)

        return column1, column2
    
    """
    Функция для создания списка номенклатур
    """
    def __create_list_nomenclature(
        self, 
        ingredients: list[str], 
        gram: list[list[int, str]],
        def_nomenclatures: list[list[nomenclature_model, int]] = None
    ) -> list[list[nomenclature_model, int]]:
        list1: list[list[nomenclature_model, int]] = []
        if def_nomenclatures is None:
            self.__create_default_nomenclature(ingredients, gram, list1)
        else:
            for ingredient, g in zip(ingredients, gram):
                for nom in def_nomenclatures:
                    if ingredient == nom[0].full_name and nom[1] == g[0]:
                        list1.append(nom)
                        break
        return list1

    """
    Функция для заполнения стандартного списка номенклатур
    """
    def __create_default_nomenclature(
        self,
        ingredients: list[str], 
        gram:list[list[int, str]],
        list1: list
    ) -> None:
        name_nomenclature = {}
        for ingredient, g in zip(ingredients, gram):
            is_range = False
            for r in self.ranges:
                if r.name == g[1]:
                    range = r
                    is_range = True
                    break
            if ingredient in name_nomenclature.keys():
                nomenclature = name_nomenclature[ingredient]
            elif is_range:
                nomenclature = nomenclature_manager.create(ingredient, range, self.groups[1])
                name_nomenclature[ingredient] = nomenclature
            else:
                ArgumentException("range", range)
            list1.append([nomenclature, g[0]])
    
    """
    Функция для обработки создания списка номенклатур по всем рецептам
    """
    def creating_list_nomenclatures_all_recipes(self) -> list[list[nomenclature_model, int]]:
        md_files = [f for f in os.listdir(self.recipe_directory) if f.endswith('.md')]

        ingredients = []
        gram = []

        for md_file in md_files:
            column1, column2 = self.__extract_columns_from_table(md_file)
            ingredients.extend(column1)
            gram.extend(column2)

        list = self.__create_list_nomenclature(ingredients, gram)

        return list

    """
    Получение данных из файла с рецептом
    """
    def __get_data_recipe(self, file_name: str) -> dict:
        file_path = os.path.join(self.recipe_directory, file_name)
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

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def handle_event(self, type: event_type, **kwargs):
        super().handle_event(type, **kwargs)
