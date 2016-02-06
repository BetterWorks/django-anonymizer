"""
anonymize_data command
"""

import importlib

from anonymizer import Anonymizer
from django.core.management.base import AppCommand


class Command(AppCommand):

    def add_arguments(self, parser):
        parser.add_argument('args', metavar='app_label', nargs='+',
                            help='One or more app names.')
        parser.add_argument('--chunksize', default=2000, type=int)
        parser.add_argument('--parallel', default=4, type=int)

    def handle_app_config(self, app_config, **options):
        chunksize = options['chunksize']
        parallel = options['parallel']
        anonymizers_module = ".".join(
            app_config.models_module.__name__.split(".")[:-1] +
            ["anonymizers"])
        mod = importlib.import_module(anonymizers_module)

        anonymizers = []
        for k, v in mod.__dict__.items():
            is_anonymizer = False
            if 'Anonymizer' in k:
                is_anonymizer = True
            try:
                if issubclass(v, Anonymizer):
                    is_anonymizer = True
            except TypeError:
                pass

            if v is Anonymizer:
                is_anonymizer = False

            if k.startswith('_'):
                is_anonymizer = False

            if is_anonymizer:
                v().validate()
                anonymizers.append(v)

        anonymizers.sort(key=lambda c: c.order)
        for a in anonymizers:
            a().run(chunksize, parallel)
