from django.core.management import CommandError
from django.core.management.base import AppCommand

from anonymizer.utils import get_anonymizers


class Command(AppCommand):

    def add_arguments(self, parser):
        parser.add_argument('args', metavar='app_label', nargs='+',
                            help='One or more app names.')

    def handle_app_config(self, app_config, **options):
        anonymizers = get_anonymizers(app_config)
        models = set()
        errors = []
        for klass in anonymizers:
            models.add(klass.model)
            instance = klass()
            try:
                instance.validate()
            except ValueError as e:
                errors.append(unicode(e))

        for model in app_config.get_models():
            if model._meta.abstract or model._meta.proxy:
                continue

            if model not in models:
                errors.append(u'need anonymizer for %s' % model)

        if errors:
            raise CommandError('%d errors\n%s' % (len(errors), '\n'.join(errors)))
        return 0
