from enum import Enum

"""
Форматы отчетов
"""
class format_reporting(Enum):
    CSV = "CSV"
    MARKDOWN = "MARKDOWN"
    JSON = "JSON"
    XML = "XML"
    RTF = "RTF"