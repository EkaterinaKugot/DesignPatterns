from src.errors.validator import Validator
from src.models.nomenclature import nomenclature_model
from src.models.group import group_model
from src.models.range import range_model
from src.core.abstract_logic import abstract_logic
from src.core.evet_type import event_type

class nomenclature_manager(abstract_logic):

    @staticmethod
    def create(
        ingredient: list[str],
        range: range_model,
        group: group_model = group_model.default_group_source(), 
    ) -> nomenclature_model:
        nomenclature = nomenclature_model()
        nomenclature.full_name = ingredient
        nomenclature.group = group
        nomenclature.range = range
        return nomenclature
    
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)
    
    def handle_event(self, type: event_type, **kwargs):
        super().handle_event(type, kwargs)