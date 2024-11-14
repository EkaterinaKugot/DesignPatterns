from src.core.abstract_processor import abstract_processor
from src.models.transaction import transaction_model
from src.errors.validator import Validator
from src.manager.settings_manager import settings_manager
from src.models.tbs import tbs_model
from src.processors.calculation_process import calculation_process
from src.core.transaction_type import transaction_type
from datetime import datetime

class tbs_process(abstract_processor):

    def __init__(self, manager: settings_manager) -> None:
        super().__init__(manager)

    """
    Переопределение метода расчета оборотно-сальдовой ведомости
    """
    def processor(self, transactions: list[transaction_model], start_date: datetime) -> tbs_model:
        receipt = []
        consumption = []
        opening_remainder = []
        remainder = []

        opening_turnovers: dict = {}
        turnovers: dict = {}
        for transaction in transactions:
            if transaction.period <= start_date:
                calculation_process.processor(opening_turnovers, transaction)
            calculation_process.processor(turnovers, transaction)

            if transaction.type_transaction == transaction_type.RECEIPT:
                receipt.append(transaction)
            elif transaction.type_transaction == transaction_type.CONSUMPTION:
                consumption.append(transaction)

        opening_remainder = list(opening_turnovers.values())
        remainder = list(turnovers.values())

        tbs = tbs_model.create(opening_remainder, receipt, consumption, remainder)
        return tbs