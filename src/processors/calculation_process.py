from src.core.abstract_processor import abstract_processor
from src.models.transaction import transaction_model
from src.manager.settings_manager import settings_manager
from src.models.turnover import turnover_model
from src.logics.type_transaction_service import type_transaction_service

class calculation_process(abstract_processor):

    def __init__(self, manager: settings_manager) -> None:
        super().__init__(manager)

    """
    Переопределение метода расчета оборотов
    """
    @staticmethod
    def processor(turnovers: dict, transaction: transaction_model):
        quantity = 0
        turnover_exists = False 
        current_key = (transaction.storage.id, transaction.nomenclature.id, transaction.range.id)
        if current_key in turnovers.keys():
            quantity = turnovers[current_key].turnover
            turnover_exists = True
            
        cond_transaction = type_transaction_service(transaction.type_transaction)
        quantity = cond_transaction.transaction(quantity, transaction.quantity)
            
        if turnover_exists:
            turnovers[current_key].turnover = int(quantity)
        else:
            turnover = turnover_model.create(transaction.storage, int(quantity), transaction.nomenclature, transaction.range)
            turnovers[current_key] = turnover