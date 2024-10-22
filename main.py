import connexion
from src.core.format_reporting import format_reporting
from src.core.filter_type import filter_type
from src.errors.validator import Validator
from src.reports.report_factory import report_factory
from src.data_reposity import data_reposity
from src.manager.settings_manager import settings_manager
from src.start_service import start_service
from flask import abort, request
from datetime import datetime
from src.dto.filter import filter
from src.logics.filter_prototype import filter_prototype
from src.logics.process_factory import turnover_process

app = connexion.FlaskApp(__name__)
manager = settings_manager()
manager.open("settings.json")
reposity = data_reposity()
start = start_service(reposity, manager)
start.create()

# http://127.0.0.1:8080/api/ui/

"""
Api для получения списка всех форматов для построения отчетов
"""
@app.route("/api/report/formats", methods=["GET"])
def formats():
    return [{"name":item.name, "value":item.value} for item in format_reporting]

"""
Api для получения списка всех форматов фильтрации
"""
@app.route("/api/type_filter", methods=["GET"])
def get_type_filter():
    return [{"name":item.name, "value":item.value} for item in filter_type]

"""
Api для получения списка моделей
"""
@app.route("/api/report/models", methods=['GET'])
def models():
    return data_reposity.keys()

"""
Api для получения отчета по единицам измерения
"""
@app.route("/api/report/range/<format>", methods=["GET"])
def report_range(format: str):
    format = format.upper()
    inner_format = format_reporting(format)
    report = report_factory(manager).create(inner_format)
    report.create( reposity.data[ data_reposity.range_key()  ] )

    return report.result


"""
Api для получения отчета по группам номенклатур
"""
@app.route("/api/report/group/<format>", methods=["GET"])
def report_group(format: str):
    format = format.upper()
    inner_format = format_reporting(format)
    report = report_factory(manager).create(inner_format)
    report.create( reposity.data[ data_reposity.group_key()  ] )

    return report.result


"""
Api для получения отчета по номенклатурам
"""
@app.route("/api/report/nomenclature/<format>", methods=["GET"])
def report_nomenclature(format: str):
    format = format.upper()
    inner_format = format_reporting(format)
    report = report_factory(manager).create(inner_format)
    report.create( reposity.data[ data_reposity.nomenclature_key()  ] )

    return report.result


"""
Api для получения отчета по рецептам
"""
@app.route("/api/report/recipe/<format>", methods=["GET"])
def report_recipe(format: str):
    format = format.upper()
    inner_format = format_reporting(format)
    report = report_factory(manager).create(inner_format)
    report.create( reposity.data[ data_reposity.recipe_key()  ] )

    return report.result

"""
Api для получения отчета по складам
"""
@app.route("/api/report/storage/<format>", methods=["GET"])
def report_storage(format: str):
    format = format.upper()
    inner_format = format_reporting(format)
    report = report_factory(manager).create(inner_format)
    report.create( reposity.data[ data_reposity.storage_key()  ] )

    return report.result

"""
Api для получения отчета по транзакциям
"""
@app.route("/api/report/transaction/<format>", methods=["GET"])
def report_transaction(format: str):
    format = format.upper()
    inner_format = format_reporting(format)
    report = report_factory(manager).create(inner_format)
    report.create( reposity.data[ data_reposity.transaction_key()  ] )

    return report.result

"""
Api для получения отчета по оборотам
"""
@app.route("/api/report/turnover/<format>", methods=["GET"])
def report_turnover(format: str):
    process_turnover = turnover_process()
    turnovers = process_turnover.create(reposity.data[ data_reposity.transaction_key()  ])
    
    format = format.upper()
    inner_format = format_reporting(format)
    report = report_factory(manager).create(inner_format)
    report.create(turnovers)

    return report.result

"""
Api для получения фильтрованных данных по модели
"""
@app.route("/api/filter/<model>", methods=["POST"])
def filter_data(model: str):

    if model not in data_reposity.keys():
        abort(400)

    request_data = request.get_json()
    item_filter = filter.create(request_data)

    data = reposity.data[model]
    if not data:
        abort(404)

    prototype = filter_prototype(data)
    prototype.create(item_filter)

    if not prototype.data:
        return {}

    report = report_factory(manager).create_default()
    report.create(prototype.data)

    return report.result

"""
Api для получения фильтрованных данных по транзакциям
"""
@app.route("/api/transaction/filter", methods=["POST"])
def filter_transaction():
    report = report_factory(manager).create_default()
    possible_models = [data_reposity.storage_key(), data_reposity.nomenclature_key()]
    data = reposity.data[data_reposity.transaction_key()]
    if not data:
        abort(404)

    request_data = request.get_json()
    model = request_data.get("model")
    if model is None or model == "" or model not in possible_models:
        report.create(data)
        return report.result
    
    item_filter: filter = filter.create(request_data)

    data_model = reposity.data[model]
    if not data_model:
        abort(404)

    # Фультруем transaction
    prototype = filter_prototype(data)
    prototype.filtering_internal_model(item_filter, data_model)

    if not prototype.data:
        return {}

    
    report.create(prototype.data)

    return report.result

"""
Api для получения фильтрованных данных по складским оборотам
"""
@app.route("/api/turnover/filter", methods=["POST"])
def filter_turnover():
    report = report_factory(manager).create_default()
    possible_models = [data_reposity.storage_key(), data_reposity.nomenclature_key()]
    data = reposity.data[data_reposity.transaction_key()]
    if not data:
        abort(404)

    request_data = request.get_json()
    start_period = request_data.get("start_period")
    end_period = request_data.get("end_period")

    try:
        start_period = datetime.strptime(start_period, "%Y-%m-%dT%H:%M:%SZ")
        end_period = datetime.strptime(end_period, "%Y-%m-%dT%H:%M:%SZ")
    except:
        pass

    process_turnover = turnover_process(start_period, end_period)
    turnovers = process_turnover.create(data)
    
    if not turnovers:
        return {}

    model = request_data.get("model")
    if model is None or model == "" or model not in possible_models:
        report.create(turnovers)
        return report.result
    
    item_filter: filter = filter.create(request_data)

    data_model = reposity.data[model]
    if not data_model:
        abort(404)

    # Фультруем turnover
    prototype = filter_prototype(turnovers)
    prototype.filtering_internal_model(item_filter, data_model)

    if not prototype.data:
        return {}

    report.create(prototype.data)

    return report.result

if __name__ == "__main__":
    app.add_api("swagger.yaml")
    app.run(port = 8080)

