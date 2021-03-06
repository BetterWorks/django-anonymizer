"""
anonymize_data command
"""

from __future__ import print_function

import time

from django.core.management.base import AppCommand

from anonymizer.utils import get_anonymizers


class Command(AppCommand):

    def add_arguments(self, parser):
        parser.add_argument('args', metavar='app_label', nargs='+',
                            help='One or more app names.')
        parser.add_argument('--chunksize', default=2000, type=int)
        parser.add_argument('--parallel', default=4, type=int)

    def handle_app_config(self, app_config, **options):
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
