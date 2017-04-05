import importlib

from anonymizer.base import Anonymizer


def get_anonymizers(app_config):
    anonymizers_module = app_config.name + '.anonymizers'
    mod = importlib.import_module(anonymizers_module)

    anonymizers = []
    for value in mod.__dict__.values():
        if value is Anonymizer:
            continue

        is_anonymizer = False
        try:
            if issubclass(value, Anonymizer) and value.model is not None:
                is_anonymizer = True
        except TypeError:
            continue

        if is_anonymizer:
            anonymizers.append(value)

    anonymizers.sort(key=lambda c: c.order)
    return anonymizers
