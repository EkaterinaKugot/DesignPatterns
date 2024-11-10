from src.core.abstract_logic import abstract_logic
from src.errors.validator import Validator
from src.core.evet_type import event_type

class observe_service:
    observers: list[abstract_logic] = []

    @staticmethod
    def append(service: abstract_logic):
        if service is None:
            return

        Validator.validate_type("service", service, abstract_logic)

        items = list(map(lambda x: type(x).__name__, observe_service.observers))
        found = type(service).__name__ in items
        if not found:
            observe_service.observers.append(service)

    @staticmethod
    def raise_event(type: event_type, **kwargs):
        for instance in observe_service.observers:
            if instance is not None:
                instance.handle_event(type, **kwargs)

    