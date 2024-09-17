from src.abstract_reference import abstract_reference
from src.models.settings_model import settings

class organization(abstract_reference):
    def __init__(self, settings: settings):
        super().__init__()
        self.inn = settings.inn
        self.bik = settings.bik
        self.account = settings.account
        self.type_property = settings.type_property

    """
    Режим сравнения (по id)
    """
    def __eq__(self, other) -> bool:
        return super().__eq__(other)
    
    def __ne__(self, other) -> bool:
        return super().__ne__(other)