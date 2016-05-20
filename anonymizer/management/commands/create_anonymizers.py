from __future__ import unicode_literals

"""
amonymize_data command
"""
from __future__ import with_statement

import sys
import os.path

from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import AppCommand, CommandError
from django.utils import importlib

from anonymizer import introspect


class Command(AppCommand):

    def handle_app(self, app, **options):

        anonymizers_module_parent = ".".join(app.__name__.split(".")[:-1])
        mod = importlib.import_module(anonymizers_module_parent)

        parent, discard = os.path.split(mod.__file__)  # lop off __init__.pyc
        path = os.path.join(parent, 'anonymizers.py') # and add anonymizers.

        if os.path.exists(path):
            raise CommandError("File '%s' already exists." % path)

        module = introspect.create_anonymizers_module(app)

        with open(path, "w") as fd:
            fd.write(module)
