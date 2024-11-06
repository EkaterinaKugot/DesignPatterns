import connexion
from src.core.format_reporting import format_reporting
from src.core.filter_type import filter_type
from src.reports.report_factory import report_factory
from src.data_reposity import data_reposity
from src.manager.settings_manager import settings_manager
from src.start_service import start_service
from src.processors.process_factory import process_factory
from src.dto.filter import filter
from src.logics.filter_prototype import filter_prototype
from src.core.evet_type import event_type
from src.logics.observe_service import observe_service
from src.logics.nomenclature_service import nomenclature_service

from flask import abort, request
from datetime import datetime

app = connexion.FlaskApp(__name__)
manager = settings_manager()
manager.open("settings.json")
reposity = data_reposity()
start = start_service(reposity, manager)
start.create()

factory = process_factory(manager)

nom_service = nomenclature_service(manager)

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
    process_turnover = factory.create("turnover")
    turnovers = process_turnover.processor(reposity.data[ data_reposity.transaction_key()  ])
    
    format = format.upper()
    inner_format = format_reporting(format)
    report = report_factory(manager).create(inner_format)
    report.create(turnovers)

    return report.result

"""
Api для получения номенклатуры по id
"""
@app.route("/api/nomenclature/<id>", methods=["GET"])
def get_nomenclature(id: str):
    data = reposity.data[data_reposity.nomenclature_key()]

    if not data:
        abort(404)

    nom_data = nom_service.get_nomenclature(data, id)

    if not nom_data:
        return {}

    report = report_factory(manager).create_default()
    report.create(nom_data)

    return report.result

"""
Api для добавления номенклатуры
"""
@app.route("/api/put_nomenclature", methods=["PUT"])
def put_nomenclature():
    new_nomenclature = request.json

    if not new_nomenclature:
        abort(400)

    nomenclature_exists = nom_service.put_nomenclature(new_nomenclature, reposity.data)
    if nomenclature_exists: 
        return "Such a nomenclature already exists"
    else:
        return "Nomenclature successfully added"
    
"""
Api для добавления номенклатуры
"""
@app.route("/api/delete_nomenclature", methods=["DELETE"])
def delete_nomenclature():
    del_nomenclature = request.json
    data = reposity.data[data_reposity.nomenclature_key()]

    if not del_nomenclature:
        abort(400)

    observe_service.raise_event(event_type.DELETE_NOMENCLATURE, nomenclature=del_nomenclature, data=data)
    return "Nomenclature removed"

"""
Api для добавления номенклатуры
"""
@app.route("/api/change_nomenclature", methods=["PATCH"])
def change_nomenclature():
    change_nomenclature = request.json

    if not change_nomenclature:
        abort(400)

    observe_service.raise_event(event_type.CHANGE_NOMENCLATURE, nomenclature=change_nomenclature, data=reposity.data)
    return "Nomenclature changed"

"""
Api для получения даты блокировки
"""
@app.route("/api/get_date_block", methods=["GET"])
def get_date_block():
    return str(manager.current_settings.date_block)

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
    data = reposity.data[data_reposity.transaction_key()]
    if not data:
        abort(404)

    request_data = request.get_json()
    storage = request_data.get("storage")
    nomenclature = request_data.get("nomenclature")

    if storage is None or nomenclature is None:
         abort(400)
    
    storage_filter: filter = filter.create(storage, "storage")
    nomenclature_filter: filter = filter.create(nomenclature, "nomenclature")

    # Фультруем transaction
    prototype = filter_prototype(data)
    prototype.create(storage_filter)
    prototype.create(nomenclature_filter)

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
    data = reposity.data[data_reposity.transaction_key()]
    if not data:
        abort(404)

    request_data = request.get_json()
    period = request_data.get("period")

    if period is None:
         abort(400)

    period_filter: filter = filter.create(period)
    prototype_period = filter_prototype(data)
    prototype_period.create(period_filter)

    storage = request_data.get("storage")
    nomenclature = request_data.get("nomenclature")

    if storage is None or nomenclature is None:
         abort(400)

    process_turnover = factory.create("turnover")
    turnovers = process_turnover.processor(prototype_period.data)
    
    if not turnovers:
        return {}

    storage_filter: filter = filter.create(storage, "storage")
    nomenclature_filter: filter = filter.create(nomenclature, "nomenclature")

    # Фультруем turnover
    prototype = filter_prototype(list(turnovers.values()))
    prototype.create(storage_filter)
    prototype.create(nomenclature_filter)

    if not prototype.data:
        return {}

    report.create(prototype.data)

    return report.result

"""
Api для изменения даты блокировки
"""
@app.route("/api/post_date_block", methods=["POST"])
def change_date_block():
    request_data = request.get_json()
    new_date_block = request_data.get("date_block")

    try:
        new_date_block = datetime.strptime(new_date_block, "%Y-%m-%dT%H:%M:%SZ")
    except:
        abort(500)

    if new_date_block != manager.current_settings.date_block:
        manager.current_settings.date_block = new_date_block

        # Рассчитываем обороты
        data = reposity.data[data_reposity.transaction_key()]
        if not data:
            abort(404)

        observe_service.raise_event(event_type.CHANGE_DATE_BLOCK, date_block=new_date_block, data=data)

    return "Ok"

if __name__ == "__main__":
    app.add_api("swagger.yaml")
    app.run(port = 8080)

