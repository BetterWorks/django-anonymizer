"""
amonymize_data command
"""

import importlib
import os.path

from anonymizer import introspect
from django.core.management.base import AppCommand, CommandError


class Command(AppCommand):

    def handle_app(self, app, **options):

        anonymizers_module_parent = ".".join(app.__name__.split(".")[:-1])
        mod = importlib.import_module(anonymizers_module_parent)

        parent, discard = os.path.split(mod.__file__)  # lop off __init__.pyc
        path = os.path.join(parent, 'anonymizers.py')  # and add anonymizers.

        if os.path.exists(path):
            raise CommandError("File '%s' already exists." % path)

        module = introspect.create_anonymizers_module(app)

        with open(path, "w") as fd:
            fd.write(module)
