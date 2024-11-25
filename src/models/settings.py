from src.errors.validator import Validator
from src.core.format_reporting import format_reporting
from datetime import datetime
from src.logics.observe_service import observe_service
from src.core.logging_type import logging_type
from src.core.evet_type import event_type

"""
Настройки
"""
class settings:
    __organization_name: str = ""
    __inn: str = ""
    __account: str = ""
    __сorrespondent_account: str = ""
    __bik: str = ""
    __type_property: str = ""
    __report_format: format_reporting = format_reporting.JSON
    __date_block: datetime = None
    __first_start: bool = True
    __json_folder: str = "./json"
    __min_log_level: logging_type = None
    __log_file = "logs.txt"

    """
    Минимальный уровень логирования
    """
    @property
    def min_log_level(self) -> str:
        return self.__min_log_level
    
    @min_log_level.setter
    def min_log_level(self, min_log_level: str):
        try:
            if isinstance(min_log_level, str):
                min_log_level = getattr(logging_type, min_log_level)
            Validator.validate_not_none("min_log_level", min_log_level)

            self.__min_log_level = min_log_level
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.DEBUG, message = f"min_log_level set to: {min_log_level}")
        except Exception as e:
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, message = e)

    """
    Имя файла с логами
    """
    @property
    def log_file(self) -> str:
        return self.__log_file
    
    @log_file.setter
    def log_file(self, log_file: str):
        try:
            Validator.validate_type("log_file", log_file, str)
            self.__log_file = log_file
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.DEBUG, message = f"log_file set to: {log_file}")
        except Exception as e:
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, message = e)

    """
    Путь для сохранение всех json файлов
    """
    @property
    def json_folder(self) -> str:
        return self.__json_folder
    
    @json_folder.setter
    def json_folder(self, json_folder: str):
        try:
            Validator.validate_type("json_folder", json_folder, str)
            self.__json_folder = json_folder
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.DEBUG, message = f"json_folder set to: {json_folder}")
        except Exception as e:
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, message = e)    

    @property
    def organization_name(self) -> str:
        return self.__organization_name
    
    @organization_name.setter
    def organization_name(self, organization_name: str):
        try:
            Validator.validate_type("organization_name", organization_name, str)
            self.__organization_name = organization_name.strip()
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.DEBUG, message = f"organization_name set to: {organization_name}")
        except Exception as e:
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, message = e)  

    @property
    def inn(self) -> str:
        return self.__inn
    
    @inn.setter
    def inn(self, inn: str):
        try:
            Validator.validate_type("inn", inn, str)
            Validator.validate_required_length("inn", inn, 12)
            self.__inn = inn
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.DEBUG, message = f"inn set to: {inn}")
        except Exception as e:
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, message = e)  

    @property
    def account(self) -> str:
        return self.__account
    
    @account.setter
    def account(self, account: str):
        try:
            Validator.validate_type("account", account, str)
            Validator.validate_required_length("account", account, 11)
            self.__account = account
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.DEBUG, message = f"account set to: {account}")
        except Exception as e:
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, message = e)  

    @property
    def сorrespondent_account(self) -> str:
        return self.__сorrespondent_account
    
    @сorrespondent_account.setter
    def сorrespondent_account(self, сorrespondent_account: str):
        try:
            Validator.validate_type("сorrespondent_account", сorrespondent_account, str)
            Validator.validate_required_length("сorrespondent_account", сorrespondent_account, 11)
            self.__сorrespondent_account = сorrespondent_account
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.DEBUG, message = f"сorrespondent_account set to: {сorrespondent_account}")
        except Exception as e:
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, message = e)  

    @property
    def bik(self) -> str:
        return self.__bik
    
    @bik.setter
    def bik(self, bik: str):
        try:
            Validator.validate_type("bik", bik, str)
            Validator.validate_required_length("bik", bik, 9)
            self.__bik = bik
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.DEBUG, message = f"bik set to: {bik}")
        except Exception as e:
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, message = e)  

    @property
    def type_property(self) -> str:
        return self.__type_property
    
    @type_property.setter
    def type_property(self, type_property: str):
        try:
            Validator.validate_type("type_property", type_property, str)
            Validator.validate_required_length("type_property", type_property, 5)
            self.__type_property = type_property
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.DEBUG, message = f"type_property set to: {type_property}")
        except Exception as e:
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, message = e)  

    @property
    def report_format(self) -> format_reporting:
        return self.__report_format
    
    @report_format.setter
    def report_format(self, report_format: format_reporting):
        try:
            Validator.validate_type("report_format", report_format, format_reporting)
            self.__report_format = report_format
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.DEBUG, message = f"report_format set to: {report_format}")
        except Exception as e:
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, message = e)  

    @property
    def date_block(self) -> datetime:
        return self.__date_block
    
    @date_block.setter
    def date_block(self, date_block: datetime):
        try:
            if isinstance(date_block, float):
                date_block = datetime.fromtimestamp(date_block)

            Validator.validate_type("date_block", date_block, datetime)
            self.__date_block = date_block
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.DEBUG, message = f"date_block set to: {date_block}")
        except Exception as e:
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, message = e)  

    @property
    def first_start(self) -> bool:
        return self.__first_start
    
    @first_start.setter
    def first_start(self, first_start: bool):
        try:
            Validator.validate_type("first_start", first_start, bool)
            self.__first_start = first_start
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.DEBUG, message = f"first_start set to: {first_start}")
        except Exception as e:
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, message = e)  