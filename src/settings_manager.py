import json
import glob
from src.models.settings_model import settings
from src.abstract_logic import abstract_logic
from src.errors.validator import Validator

"""
Менеджер настроек
"""
class settings_manager(abstract_logic):
    __file_name = "settings.json"
    __settings: settings = settings()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance
    
    def convert(self) -> bool:
        path = f"./**/{self.__file_name}"
        full_name = glob.glob(path, recursive=True)[0]
        with open(full_name) as stream:
            data = json.load(stream)
        
        fields = dir(self.__settings)
        for key in data.keys():
            if key in fields:
                self.__settings.__setattr__(key, data[key])
        return True


    def open(self, file_name: str = "") -> bool:
        Validator.validate_type("file_name", file_name, str)
        
        if file_name != "":
            self.__file_name = file_name

        try:
            return self.convert()
        except Exception as ex:
            self.__settings = self.__default_setting()
            self.set_exception(ex)
            return False
    
    """
    Загруженные настройки
    """
    @property
    def current_settings(self) -> settings:
        return self.__settings
    

    """
    Набор настроек по умолчанию
    """
    def __default_setting(self) -> settings:
        _settings = settings()
        _settings.inn = "380080920202"
        _settings.organization_name = "Рога и копыта (default)"
        _settings.account = "11127400937"
        _settings.сorrespondent_account = "86127390170"
        _settings.bik = "662817992"
        _settings.type_property = "lalal"
        return _settings
    
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)