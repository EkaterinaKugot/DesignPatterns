from src.manager.settings_manager import settings_manager
from src.errors.validator import Validator
from src.core.abstract_logic import abstract_logic
from src.core.abstract_processor import abstract_processor
from src.processors.turnover_process import turnover_process
from src.processors.date_block_processor import date_block_processor
from src.processors.calculation_process import calculation_process

class process_factory(abstract_logic):
    __settings_manager: settings_manager = None

    def __init__(self, manager: settings_manager):
        self.__processes = {}

        Validator.validate_type("manager", manager, settings_manager)
        self.__settings_manager = manager

        self.register_process('turnover', turnover_process)
        self.register_process('date_block', date_block_processor)
        self.register_process('calculation', calculation_process)

    def register_process(self, process_name: str, process_class) -> None:
        """Регистрирует новый процесс в фабрике."""
        self.__processes[process_name] = process_class

    def create(self, process_name: str) -> abstract_processor:
        """Возвращает экземпляр зарегистрированного процесса."""
        process_class = self.__processes.get(process_name)
        Validator.validate_not_none("process_class", process_class)
        return process_class(self.__settings_manager)
    
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)