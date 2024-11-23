from enum import Enum

"""
Типы событий
"""
class event_type(Enum):
    DELETE_NOMENCLATURE = 1
    CHANGE_NOMENCLATURE = 2
    GET_NOMENCLATURE = 3
    PUT_NOMENCLATURE = 4
    SAVE_DATA_REPOSITY = 5
    RESTORE_DATA_REPOSITY = 6
    CHANGE_DATE_BLOCK = 7
    LOGGING = 8