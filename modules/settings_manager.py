import json
import glob
from modules.settings import settings

class settings_manager:
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
        if not isinstance(file_name, str):
            raise TypeError("Некорректно передан параметр!")
        
        if file_name != "":
            self.__file_name = file_name

        try:
            self.convert()
        except:
            self.__settings = self.__default_setting()
            return False

    #Настройки
    @property
    def settings(self):
        return self.__settings
    
    def __default_setting(self):
        data = settings()
        data.inn = "3545252"
        data.organization_name = "Рога и копыта"
        data.director_name = "Kate"
        return data