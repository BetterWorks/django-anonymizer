"""
anonymize_data command
"""

from __future__ import print_function

import sys
import time

from django.core.management.base import AppCommand, CommandError
from django.db import connection
from django.utils import six

from anonymizer.utils import get_anonymizers


class Command(AppCommand):

    def add_arguments(self, parser):
        parser.add_argument('args', metavar='app_label', nargs='+',
                            help='One or more app names.')
        parser.add_argument('--chunksize', default=2000, type=int)
        parser.add_argument('--parallel', default=4, type=int)
        parser.add_argument('--confirmed', default=False, help='Skip confirm prompt')

    def handle_app_config(self, app_config, **options):
        if not options['confirmed']:
            self.stdout.write(
                'This will do an in-place anonymization of "%s"' % connection.settings_dict['NAME']
            )
            confirm = six.moves.input('Are you sure you want to continue? [Y/N] ')

            if confirm not in ('Y', 'N'):
                raise CommandError('NOOP: Please enter "Y" or "N".')
            if confirm == 'N':
                self.stdout.write('Action aborted.')
                sys.exit()

        chunksize = options['chunksize']
        parallel = options['parallel']

        anonymizers = get_anonymizers(app_config)
        instances = []
        for klass in anonymizers:
            instance = klass()
            instance.validate()
            instances.append(instance)

        for instance in instances:
            self.stdout.write('Running %s.%s... ' % (instance.__class__.__module__,
                                                     instance.__class__.__name__), ending='')
            self.stdout.flush()
            start = time.time()
            instance.run(chunksize=chunksize, parallel=parallel)
            duration = time.time() - start
            self.stdout.write('took %0.2f seconds' % duration)
