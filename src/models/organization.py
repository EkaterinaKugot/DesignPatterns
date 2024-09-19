from src.core.base_model import base_model_name
from src.models.settings import settings

class organization_model(base_model_name):
    def __init__(self, settings: settings):
        super().__init__()
        self.inn = settings.inn
        self.bik = settings.bik
        self.account = settings.account
        self.type_property = settings.type_property