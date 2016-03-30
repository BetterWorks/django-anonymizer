from datetime import datetime, timedelta, date
import decimal
import six
import zlib

from django.apps import apps
from django.test import TestCase
from six.moves import xrange

from anonymizer import Anonymizer, introspect
from anonymizer.tests import models as test_models


def compress(num):
    return zlib.compress(six.text_type(num).encode('ascii'))


def decompress(raw):
    return int(zlib.decompress(raw))


class TestIntrospect(TestCase):

    def test_introspect(self):
        config = apps.get_app_config('tests')
        mod = introspect.create_anonymizers_module(config)
        expected = """
from anonymizer.tests.models import Other, EverythingModel
from anonymizer import Anonymizer

class OtherAnonymizer(Anonymizer):

    model = Other

    attributes = [
        ('id', "SKIP"),
    ]


class EverythingModelAnonymizer(Anonymizer):

    model = EverythingModel

    attributes = [
        ('id', "SKIP"),
        ('username', "username"),
        ('name', "name"),
        ('email', "email"),
        ('address_city', "city"),
        ('address_post_code', "uk_postcode"),
        ('address', "full_address"),
        ('o1_id', "SKIP"),
        ('something', "lorem"),
        ('something_else', "lorem"),
        ('some_varchar', "varchar"),
        ('birthday', "datetime"),
        ('age', "positive_small_integer"),
        ('icon', UNKNOWN_FIELD),
        ('some_datetime', "datetime"),
        ('some_date', "date"),
        ('sex', "choice"),
        ('price', "decimal"),
        ('binary', UNKNOWN_FIELD),
    ]
"""
        self.assertEqual(mod.strip(), expected.strip())


class TestAnonymizer(TestCase):

    # Nice high count, so that our handling of unique constraint with test data
    # will likely be tested.
    NUM_ITEMS = 1000

    def setUp(self):
        self.o1 = test_models.Other.objects.create()
        self.now = datetime.now()
        self.today = date.today()

        instances = (test_models.EverythingModel(id=x,
                                                 o1=self.o1,
                                                 username="intial%d" % x,
                                                 birthday=self.now + timedelta(365 * x),
                                                 age=x,
                                                 some_datetime=self.now,
                                                 some_date=self.today,
                                                 sex='X',
                                                 price=decimal.Decimal("1.23"),
                                                 binary=compress(x),
                                                 )
                     for x in xrange(1, self.NUM_ITEMS + 1))

        test_models.EverythingModel.objects.bulk_create(instances)

    def test_anonymizer(self):
        # Test for as much as possible in one test.
        assert test_models.EverythingModel.objects.count() == self.NUM_ITEMS
        assert test_models.EverythingModel._meta.get_field('username').unique is True

        class EverythingAnonmyizer(Anonymizer):
            model = test_models.EverythingModel

            attributes = [
                ('id', "SKIP"),
                ('o1_id', "SKIP"),
                ('icon', "SKIP"),
                ('username', 'username'),
                ('name', "name"),
                ('email', "email"),
                ('address_city', "city"),
                ('address_post_code', "uk_postcode"),
                ('address', "full_address"),
                ('something', "lorem"),
                ('something_else', "similar_lorem"),
                ('some_varchar', "varchar"),
                ('birthday', "datetime"),
                ('age', "positive_small_integer"),
                ('some_datetime', "datetime"),
                ('some_date', "date"),
                ('sex', "choice"),
                ('price', "decimal"),
                ('binary', lambda anon, obj, field, val: compress(decompress(val) * -1))
            ]

        EverythingAnonmyizer().run(parallel=0)
        objs = test_models.EverythingModel.objects.all()
        self.assertEqual(len(objs), self.NUM_ITEMS)
        for o in objs:
            # check everything has been changed
            self.assertFalse(o.username.startswith('initial'))

            # Check for corresponding user names/emails.  This works if username
            # is first in the list, as recommended and as introspection
            # generates.
            self.assertTrue(o.email.startswith(o.username))

            # test for DjangoFaker.choice
            self.assertTrue(o.sex in ('M', 'F'))

            self.assertIsNotNone(o.some_datetime)
            self.assertNotEqual(o.some_datetime, self.now)

            self.assertIsNotNone(o.some_date)
            self.assertNotEqual(o.some_date, self.today)

            self.assertEqual(decompress(o.binary), o.id * -1)
