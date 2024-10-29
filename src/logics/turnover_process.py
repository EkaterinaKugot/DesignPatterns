from src.core.abstract_processor import abstract_processor
from src.models.transaction import transaction_model
from src.models.turnover import turnover_model
from src.logics.transaction_service import transaction_service

class turnover_process(abstract_processor):

    """
    Переопределение метода расчета оборотов
    """
    def processor(self, transactions: list[transaction_model]) -> list:
        turnovers: list[turnover_model] = [] 
        for transaction in transactions:
            quantity = 0
            idx = -1
            for i, tur in enumerate(turnovers):
                if transaction.nomenclature == tur.nomenclature and \
                    transaction.storage == tur.storage:
                    quantity = tur.turnover
                    idx = i
                    break
            
            cond_transaction = transaction_service(transaction.type_transaction)
            quantity = cond_transaction.transaction(quantity, transaction.quantity)
            if idx != -1:
                turnovers[idx].turnover = int(quantity)
            else:
                turnover = turnover_model.create(transaction.storage, int(quantity), transaction.nomenclature, transaction.range)
                turnovers.append(turnover)

        return turnovers