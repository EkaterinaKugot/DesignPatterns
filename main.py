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
from src.logics.recipe_service import recipe_service
from src.logics.turnover_service import turnover_service
from src.reposity_manager import reposity_manager
from src.logics.transaction_service import transaction_service
from src.errors.logger import Logger
from src.core.logging_type import logging_type

from flask import abort, request
from datetime import datetime

app = connexion.FlaskApp(__name__)

manager = settings_manager()
manager.open("settings.json")
rep_manager = reposity_manager(manager)

reposity = data_reposity()
start = start_service(reposity, manager)
start.create()

factory = process_factory(manager)

nom_service = nomenclature_service(manager)
rec_service = recipe_service(manager)
tur_service = turnover_service(manager)
tran_service = transaction_service(manager)

logger = Logger(manager)

# http://127.0.0.1:8080/api/ui/

"""
Api для получения списка всех форматов для построения отчетов
"""
@app.route("/api/report/formats", methods=["GET"])
def formats():
    observe_service.raise_event(
        event_type.LOGGING, 
        log_type=logging_type.INFO, 
        message="Getting a list of all formats for building reports"
    )
    return [{"name":item.name, "value":item.value} for item in format_reporting]

"""
Api для получения списка всех форматов фильтрации
"""
@app.route("/api/type_filter", methods=["GET"])
def get_type_filter():
    observe_service.raise_event(
        event_type.LOGGING, 
        log_type=logging_type.INFO, 
        message="Getting a list of all filtering formats"
    )
    return [{"name":item.name, "value":item.value} for item in filter_type]

"""
Api для получения списка моделей
"""
@app.route("/api/report/models", methods=['GET'])
def models():
    observe_service.raise_event(
        event_type.LOGGING, 
        log_type=logging_type.INFO, 
        message="Getting a list of models"
    )
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
    observe_service.raise_event(
        event_type.LOGGING, 
        log_type=logging_type.INFO, 
        message="Getting a report by range"
    )
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
    observe_service.raise_event(
        event_type.LOGGING, 
        log_type=logging_type.INFO, 
        message="Getting a report on nomenclature groups"
    )
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
    observe_service.raise_event(
        event_type.LOGGING, 
        log_type=logging_type.INFO, 
        message="Getting a report on nomenclatures"
    )
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
    observe_service.raise_event(
        event_type.LOGGING, 
        log_type=logging_type.INFO, 
        message="Getting a recipe report"
    )
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
    observe_service.raise_event(
        event_type.LOGGING, 
        log_type=logging_type.INFO, 
        message="Getting a report on storage"
    )
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
    observe_service.raise_event(
        event_type.LOGGING, 
        log_type=logging_type.INFO, 
        message="Getting a transaction report"
    )
    return report.result

"""
Api для получения отчета по оборотам
"""
@app.route("/api/report/turnover/<format>", methods=["GET"])
def report_turnover(format: str):
    process_turnover = factory.create("turnover")
    turnovers = process_turnover.processor(reposity.data[ data_reposity.transaction_key() ])
    
    format = format.upper()
    inner_format = format_reporting(format)
    report = report_factory(manager).create(inner_format)
    report.create(turnovers)
    observe_service.raise_event(
        event_type.LOGGING, 
        log_type=logging_type.INFO, 
        message="Getting a turnover report"
    )
    return report.result

"""
Api для получения отчета по оборотно-сальдовой ведомости
"""
@app.route("/api/report/tbs/<format>", methods=["GET"])
def report_tbs(format: str):
    try:
        data = reposity.data[data_reposity.transaction_key()]
        if not data:
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, 
                                        message="Error in report_tbs: There is no data to filter by model")
            abort(404)

        start_date = request.args.get('start_date')
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ")
        except Exception as e: 
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, 
                                        message=f"Error in report_tbs: {str(e)}")
            abort(500)

        end_date = request.args.get('end_date')
        storage_name = request.args.get('storage_name')

        period_filter: filter = filter.create({"end_period": end_date})
        storage_filter: filter = filter.create({"name": storage_name}, "storage")

        prototype = filter_prototype(data)
        prototype.create(period_filter)
        prototype.create(storage_filter)

        if not prototype.data:
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, 
                                        message="Error in report_tbs: There is no data to filter by model")
            abort(404)

        process_tbs = factory.create("tbs")
        tbs = process_tbs.processor(prototype.data, start_date)

        format = format.upper()
        inner_format = format_reporting(format)
        report = report_factory(manager).create(inner_format)
        report.create([tbs])

        observe_service.raise_event(event_type.LOGGING, log_type=logging_type.INFO, 
                                        message="Tbs report has been successfully created")
        return report.result
    except Exception as e:
        observe_service.raise_event(
            event_type.LOGGING, 
            log_type=logging_type.ERROR, 
            message=f"Error in report_tbs: {str(e)}"
        )
        abort(500)

"""
Api для получения номенклатуры по id
"""
@app.route("/api/nomenclature/<id>", methods=["GET"])
def get_nomenclature(id: str):
    try:
        data = reposity.data[data_reposity.nomenclature_key()]

        if not data:
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, 
                                        message="Error in get_nomenclature: There is no data to filter by model")
            abort(404)

        nom_data = nom_service.get_nomenclature(data, id)

        if not nom_data:
            return {}

        report = report_factory(manager).create_default()
        report.create(nom_data)

        observe_service.raise_event(event_type.LOGGING, log_type=logging_type.INFO, 
                                        message="Nomenclature successfully received")
        return report.result
    except Exception as e:
        observe_service.raise_event(
            event_type.LOGGING, 
            log_type=logging_type.ERROR, 
            message=f"Error in get_nomenclature: {str(e)}"
        )
        abort(500)

"""
Api для добавления номенклатуры
"""
@app.route("/api/put_nomenclature", methods=["PUT"])
def put_nomenclature():
    try:
        new_nomenclature = request.json

        if not new_nomenclature:
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, 
                                        message="Error in put_nomenclature: Invalid data to add")
            abort(400)

        nomenclature_exists = nom_service.put_nomenclature(new_nomenclature, reposity.data)
        if nomenclature_exists: 
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.INFO, 
                                        message="Such a nomenclature already exists")
            return "Such a nomenclature already exists"
        else:
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.INFO, 
                                        message="Nomenclature successfully added")
            return "Nomenclature successfully added"
    except Exception as e:
        observe_service.raise_event(
            event_type.LOGGING, 
            log_type=logging_type.ERROR, 
            message=f"Error in put_nomenclature: {str(e)}"
        )
        abort(500)
    
"""
Api для добавления номенклатуры
"""
@app.route("/api/delete_nomenclature", methods=["DELETE"])
def delete_nomenclature():
    try:
        del_nomenclature = request.json
        data = reposity.data[data_reposity.nomenclature_key()]

        if not del_nomenclature:
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, 
                                        message="Error in delete_nomenclature: Invalid data to delete")
            abort(400)

        observe_service.raise_event(event_type.DELETE_NOMENCLATURE, nomenclature=del_nomenclature, data=data)
        observe_service.raise_event(event_type.LOGGING, log_type=logging_type.INFO, 
                                        message="Nomenclature successfully removed")
        return "Nomenclature successfully removed"
    except Exception as e:
        observe_service.raise_event(
            event_type.LOGGING, 
            log_type=logging_type.ERROR, 
            message=f"Error in delete_nomenclature: {str(e)}"
        )
        abort(500)
"""
Api для изменения номенклатуры
"""
@app.route("/api/change_nomenclature", methods=["PATCH"])
def change_nomenclature():
    try:
        change_nomenclature = request.json

        if not change_nomenclature:
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, 
                                        message="Error in change_nomenclature: Invalid data to change")
            abort(400)

        observe_service.raise_event(event_type.CHANGE_NOMENCLATURE, nomenclature=change_nomenclature, data=reposity.data)
        observe_service.raise_event(event_type.LOGGING, log_type=logging_type.INFO, 
                                        message="Nomenclature successfully changed")
        return "Nomenclature successfully changed"
    except Exception as e:
        observe_service.raise_event(
            event_type.LOGGING, 
            log_type=logging_type.ERROR, 
            message=f"Error in change_nomenclature: {str(e)}"
        )
        abort(500)

"""
Api для получения даты блокировки
"""
@app.route("/api/get_date_block", methods=["GET"])
def get_date_block():
    try:
        observe_service.raise_event(event_type.LOGGING, log_type=logging_type.INFO, 
                                        message="Getting the blocking date")
        return str(manager.current_settings.date_block)
    except Exception as e:
        observe_service.raise_event(
            event_type.LOGGING, 
            log_type=logging_type.ERROR, 
            message=f"Error in get_date_block: {str(e)}"
        )
        abort(500)

"""
Api для получения фильтрованных данных по модели
"""
@app.route("/api/filter/<model>", methods=["POST"])
def filter_data(model: str):
    try:
        if model not in data_reposity.keys():
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, 
                                        message=f"Error in filter_data: This model was not found: {model}")
            abort(400)

        request_data = request.get_json()
        item_filter = filter.create(request_data)

        data = reposity.data[model]
        if not data:
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, 
                                        message=f"Error in filter_data: There is no data to filter by model")
            abort(404)

        prototype = filter_prototype(data)
        prototype.create(item_filter)

        if not prototype.data:
            return {}

        report = report_factory(manager).create_default()
        report.create(prototype.data)
        observe_service.raise_event(event_type.LOGGING, log_type=logging_type.INFO, 
                                        message=f"The {model} report has been successfully created")
        return report.result
    except Exception as e:
        observe_service.raise_event(
            event_type.LOGGING, 
            log_type=logging_type.ERROR, 
            message=f"Error in filter_data: {str(e)}"
        )
        abort(500)

"""
Api для получения фильтрованных данных по транзакциям
"""
@app.route("/api/transaction/filter", methods=["POST"])
def filter_transaction():
    try:
        report = report_factory(manager).create_default()
        data = reposity.data[data_reposity.transaction_key()]
        if not data:
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, 
                                        message=f"Error in filter_transaction: There is no data to filter by model")
            abort(404)

        request_data = request.get_json()
        storage = request_data.get("storage")
        nomenclature = request_data.get("nomenclature")

        if storage is None or nomenclature is None:
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, 
                                        message=f"Error in filter_transaction: This model was not found")
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
        observe_service.raise_event(event_type.LOGGING, log_type=logging_type.INFO, 
                                        message=f"The transaction report has been successfully created")
        return report.result
    except Exception as e:
        observe_service.raise_event(
            event_type.LOGGING, 
            log_type=logging_type.ERROR, 
            message=f"Error in filter_transaction: {str(e)}"
        )
        abort(500)
"""
Api для получения фильтрованных данных по складским оборотам
"""
@app.route("/api/turnover/filter", methods=["POST"])
def filter_turnover():
    try:
        report = report_factory(manager).create_default()
        data = reposity.data[data_reposity.transaction_key()]
        if not data:
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, 
                                        message=f"Error in filter_turnover: There is no data to filter by model")
            abort(404)

        request_data = request.get_json()
        period = request_data.get("period")

        if period is None:
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, 
                                        message=f"Error in filter_turnover: This model was not found")
            abort(400)

        period_filter: filter = filter.create(period)
        prototype_period = filter_prototype(data)
        prototype_period.create(period_filter)

        storage = request_data.get("storage")
        nomenclature = request_data.get("nomenclature")

        if storage is None or nomenclature is None:
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.ERROR, 
                                        message=f"Error in filter_turnover: This model was not found")
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

        observe_service.raise_event(event_type.LOGGING, log_type=logging_type.INFO, 
                                        message=f"The turnover report has been successfully created")
        return report.result
    except Exception as e:
        observe_service.raise_event(
            event_type.LOGGING, 
            log_type=logging_type.ERROR, 
            message=f"Error in filter_turnover: {str(e)}"
        )
        abort(500)

"""
Api для изменения даты блокировки
"""
@app.route("/api/post_date_block", methods=["POST"])
def change_date_block():
    try:
        request_data = request.get_json()
        new_date_block = request_data.get("date_block")

        try:
            new_date_block = datetime.strptime(new_date_block, "%Y-%m-%dT%H:%M:%SZ")
        except Exception as e:
            observe_service.raise_event(
                event_type.LOGGING, 
                log_type=logging_type.ERROR, 
                message=f"Error in change_date_block: {str(e)}"
            )
            abort(500)

        if new_date_block != manager.current_settings.date_block:

            # Рассчитываем обороты
            data = reposity.data[data_reposity.transaction_key()]
            if not data:
                abort(404)

            observe_service.raise_event(event_type.CHANGE_DATE_BLOCK, date_block=new_date_block, data=data)

        observe_service.raise_event(event_type.LOGGING, log_type=logging_type.INFO, 
                                        message=f"Block date changed")
        return "Block date changed"
    except Exception as e:
        observe_service.raise_event(
            event_type.LOGGING, 
            log_type=logging_type.ERROR, 
            message=f"Error in change_date_block: {str(e)}"
        )
        abort(500)

"""
Api для сохранения текущих данных
"""
@app.route("/api/data_reposity/save", methods=["POST"])
def save_data_reposity():
        try:
            observe_service.raise_event(event_type.SAVE_DATA_REPOSITY, data=reposity.data)
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.INFO, 
                                        message=f"Data saved successfully")
            return "Data saved successfully"
        except Exception as e:
            observe_service.raise_event(
                event_type.LOGGING, 
                log_type=logging_type.ERROR, 
                message=f"Error in save_data_reposity: {str(e)}"
            )
            abort(500)

"""
Api для восстановления данных
"""
@app.route("/api/data_reposity/restore", methods=["POST"])
def restore_data_reposity():
        try:
            observe_service.raise_event(event_type.RESTORE_DATA_REPOSITY, data=reposity.data)
            observe_service.raise_event(event_type.LOGGING, log_type=logging_type.INFO, 
                                        message=f"Data restored successfully")
            return "Data restored successfully"
        except Exception as e:
            observe_service.raise_event(
                event_type.LOGGING, 
                log_type=logging_type.ERROR, 
                message=f"Error in save_data_reposity: {str(e)}"
            )
            abort(500)

if __name__ == "__main__":
    app.add_api("swagger.yaml")
    app.run(host="0.0.0.0", port = 8080)

