import json
import os

class settings:
    _organization_name = ""
    _inn = ""
    _director_name = ""


    @property
    def organization_name(self):
        return self._organization_name
    
    @organization_name.setter
    def organization_name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Некорректно передан параметр!")
        self._organization_name = value

    @property
    def inn(self):
        return self._inn
    
    @inn.setter
    def inn(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Некорректно передан параметр!")
        self._inn = value

    @property
    def director_name(self):
        return self._director_name
    
    @director_name.setter
    def director_name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Некорректно передан параметр!")
        self._director_name = value

class settings_manager:
    __file_name = "settings.json"
    __settings: settings = settings()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance

    def open(self, file_name: str = ""):
        if not isinstance(file_name, str):
            raise TypeError("Некорректно передан параметр!")
        
        if file_name != "":
            self.__file_name = file_name

        try:
            full_name = f"{os.curdir}{os.sep}{self.__file_name}"
            stream = open(full_name)
            data = json.load(stream)
            stream.close()
            
            fields = dir(self.__settings)
            for key in data.keys():
                if key in fields:
                    self.__settings.__setattr__(key, data[key])
            return True
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

manager1 = settings_manager()
manager1.open("settings.json")
print(f"settings1: {manager1.settings.inn}")

manager2 = settings_manager()
# manager2.open("set.json")
print(f"settings2: {manager2.settings.inn}")

