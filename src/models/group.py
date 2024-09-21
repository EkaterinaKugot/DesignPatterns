from src.core.base_model import base_model_name

class group_model(base_model_name):
    
    @staticmethod
    def default_group_source():
        item = group_model()
        item.name = "Сырье"
        return item
    
    @staticmethod
    def default_group_cold():
        item = group_model()
        item.name = "Заморозка"
        return item