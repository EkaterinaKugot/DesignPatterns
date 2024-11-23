from datetime import datetime
from src.core.abstract_logic import abstract_logic
from src.core.logging_type import logging_type
from src.core.evet_type import event_type
from src.logics.observe_service import observe_service
from src.manager.settings_manager import settings_manager
from src.errors.validator import Validator
from src.errors.custom_exception import FileWriteException

"""
Логер
"""
class Logger(abstract_logic):
    __settings_manager: settings_manager = None

    def __init__(self, manager: settings_manager):
        super().__init__()
        Validator.validate_type("manager", manager, settings_manager)
        self.__settings_manager = manager

        self.__write()

        observe_service.append(self)    

    def __write(self, message: str = None) -> bool:
        if message is None:
            message = f"\n=== Logging started at {datetime.now()} ===\n<Time>, <Type>, <Message>\n"
        Validator.validate_type("message", message, str)

        full_path = self.__settings_manager.current_settings.log_file
        try:
            with open(full_path, "a", encoding="utf-8") as file:
                file.write(message)
            return True
        except:
            return False
            

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def handle_event(self, type: event_type, **kwargs):
        super().handle_event(type, **kwargs)

        if type == event_type.LOGGING:
            log_type: logging_type = kwargs.get("log_type")
            Validator.validate_type("log_type", log_type, logging_type)

            message = kwargs.get("message", "Exception")
            Validator.validate_type("message", message, str)

            if log_type.value >= self.__settings_manager.current_settings.min_log_level.value:
                time = datetime.now()
                message = f"{time}, {log_type.name}, Message: {message}\n"

                if not self.__write(message):
                    FileWriteException("message", self.__settings_manager.current_settings.log_file)

