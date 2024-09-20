from src.core.base_model import base_model_id
from src.models.group import group_model
from src.models.range import range_model
from src.errors.validator import Validator
from src.errors.custom_exception import ArgumentException
import os
import re

class nomenclature_model(base_model_id):
    __full_name: str = ""
    __group: group_model = None
    __range: range_model = None

    @property
    def full_name(self) -> str:
        return self.__full_name
    
    @full_name.setter
    def full_name(self, full_name: str):
        Validator.validate_type("full_name", full_name, str)
        Validator.validate_permissible_length("full_name", full_name, 255)
        self.__full_name = full_name.strip()

    """
    Группа номенклатуры
    """
    @property
    def group(self) -> group_model:
        return self.__group
    
    @group.setter
    def group(self, group: group_model):
        Validator.validate_type("group", group, group_model)
        self.__group = group

    """
    Единица измерения
    """
    @property
    def range(self) -> range_model:
        return self.__range
    
    @range.setter
    def range(self, range: range_model):
        Validator.validate_type("range", range, range_model)
        self.__range = range

    """
    Функция для извлечения данных из таблицы markdown
    """
    @staticmethod
    def extract_columns_from_table(file_name: str, directory: str = "./src/docs"):
        Validator.validate_type("file_name", file_name, str)
        Validator.validate_empty_length("file_name", file_name)

        Validator.validate_type("directory", directory, str)
        Validator.validate_empty_length("directory", directory)

        file_path = os.path.join(directory, file_name)

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
    Функция для обработки всех рецептов с расширением .md
    """
    @staticmethod
    def process_markdown_files(directory: str = "./src/docs") -> list[list[str], list[list[int, str]]]:
        Validator.validate_type("directory", directory, str)
        Validator.validate_empty_length("directory", directory)
        md_files = [f for f in os.listdir(directory) if f.endswith('.md')]

        ingredients = []
        gram = []

        for md_file in md_files:
            column1, column2 = nomenclature_model.extract_columns_from_table(md_file, directory)
            ingredients.extend(column1)
            gram.extend(column2)

        return ingredients, gram
    
    """
    Функция для создания списка номенклатур
    """
    @staticmethod
    def create_list_nomenclature(ingredients: list[str], gram: list[list[int, str]]) -> list:
        for ingredient, g in zip(ingredients, gram):
            Validator.validate_type("ingredient", ingredient, str)
            Validator.validate_type("gram", g[0], int)
            Validator.validate_type("gram", g[1], str)
        list = []
        for ingredient, g in zip(ingredients, gram):
            nomenclature = nomenclature_model()
            nomenclature.full_name = ingredient
            nomenclature.group = group_model.default_group_source()
            nomenclature.range = range_model(g[1], g[0])
            list.append(nomenclature)
        return list