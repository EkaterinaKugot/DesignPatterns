from src.errors.validator import Validator
"""
Настройки
"""
class settings:
    __organization_name = ""
    __inn = ""
    __account = ""
    __сorrespondent_account = ""
    __bik = ""
    __type_property = ""


    @property
    def organization_name(self):
        return self.__organization_name
    
    @organization_name.setter
    def organization_name(self, organization_name: str):
        Validator.validate_type("organization_name", organization_name, str)
        self.__organization_name = organization_name.strip()

    @property
    def inn(self):
        return self.__inn
    
    @inn.setter
    def inn(self, inn: str):
        Validator.validate_type("inn", inn, str)
        Validator.validate_required_length("inn", inn, 12)
        self.__inn = inn

    @property
    def account(self):
        return self.__account
    
    @account.setter
    def account(self, account: str):
        Validator.validate_type("account", account, str)
        Validator.validate_required_length("account", account, 11)
        self.__account = account

    @property
    def сorrespondent_account(self):
        return self.__сorrespondent_account
    
    @сorrespondent_account.setter
    def сorrespondent_account(self, сorrespondent_account: str):
        Validator.validate_type("сorrespondent_account", сorrespondent_account, str)
        Validator.validate_required_length("сorrespondent_account", сorrespondent_account, 11)
        self.__сorrespondent_account = сorrespondent_account

    @property
    def bik(self):
        return self.__bik
    
    @bik.setter
    def bik(self, bik: str):
        Validator.validate_type("bik", bik, str)
        Validator.validate_required_length("bik", bik, 9)
        self.__bik = bik

    @property
    def type_property(self):
        return self.__type_property
    
    @type_property.setter
    def type_property(self, type_property: str):
        Validator.validate_type("type_property", type_property, str)
        Validator.validate_required_length("type_property", type_property, 5)
        self.__type_property = type_property