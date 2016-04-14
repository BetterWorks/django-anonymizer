import decimal
import uuid
import zlib
from datetime import date, datetime, timedelta

import six
from anonymizer import Anonymizer, introspect
from anonymizer.tests import models as test_models
from django.apps import apps
from django.test import TestCase

from six.moves import xrange


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
        ('name', "name"),
        ('email', "email"),
        ('username', "username"),
        ('address', "full_address"),
        ('o1_id', "SKIP"),
        ('lorem', "lorem"),
        ('similar_lorem', "lorem"),
        ('unique_lorem', "lorem"),
        ('some_varchar', "varchar"),
        ('birthday', "datetime"),
        ('age', "positive_small_integer"),
        ('icon', UNKNOWN_FIELD),
        ('some_datetime', "datetime"),
        ('some_date', "date"),
        ('sex', "choice"),
        ('price', "decimal"),
        ('binary', UNKNOWN_FIELD),
        ('uuid', UNKNOWN_FIELD),
        ('boolean', "bool"),
        ('small_integer', "small_integer"),
        ('positive_small_integer', "positive_small_integer"),
        ('postcode', "varchar"),
        ('country', "varchar"),
        ('first_name', "first_name"),
        ('similar_email', "email"),
        ('similar_email_other', "email"),
        ('phonenumber', "phonenumber"),
        ('last_name', "last_name"),
        ('street_address', "full_address"),
        ('state', "state"),
        ('zip_code', "zip_code"),
        ('company', "varchar"),
        ('similar_datetime', "datetime"),
        ('similar_date', "date"),
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

        instances = (test_models.EverythingModel(
            id=x,
            o1=self.o1,
            username="intial%d" % x,
            lorem='hello world',
            similar_lorem='Hello, world!',
            unique_lorem='Hello, world! #%d' % x,
            birthday=self.now + timedelta(365 * x),
            age=x,
            some_datetime=self.now,
            some_date=self.today,
            sex='X',
            price=decimal.Decimal("1.23"),
            binary=compress(x),
            uuid=str(uuid.uuid4()),
            boolean=True,
            small_integer=-1,
            positive_small_integer=1,
            postcode='12345-12345',
            country='Qatar',
            first_name='Joe',
            last_name='Schmoe',
            similar_email='monkey@betterworks.com',
            similar_email_other='joe@other.com',
            phonenumber='(555) 555-5555',
            street_address='123 Maple Street',
            state='CA',
            zip_code=94063,
            company='BetterWorks',
            similar_datetime=self.now,
            similar_date=self.today,
            ) for x in xrange(1, self.NUM_ITEMS + 1))

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
                ('address', "full_address"),
                ('lorem', "lorem"),
                ('similar_lorem', "similar_lorem"),
                ('unique_lorem', "unique_lorem"),
                ('some_varchar', "varchar"),
                ('birthday', "datetime"),
                ('age', "positive_small_integer"),
                ('some_datetime', "datetime"),
                ('some_date', "date"),
                ('sex', "choice"),
                ('price', "decimal"),
                ('binary', lambda anon, obj, field, val: compress(decompress(val) * -1)),
                ('boolean', "bool"),
                ('uuid', "uuid"),
                ('small_integer', "small_integer"),
                ('positive_small_integer', "positive_small_integer"),
                ('postcode', "postcode"),
                ('country', "country"),
                ('first_name', "first_name"),
                ('last_name', "last_name"),
                ('similar_email', "similar_email"),
                ('similar_email_other', "similar_email"),
                ('phonenumber', "phonenumber"),
                ('street_address', "street_address"),
                ('state', "state"),
                ('zip_code', "zip_code"),
                ('company', "company"),
                ('similar_datetime', "similar_datetime"),
                ('similar_date', "similar_date"),
            ]

        EverythingAnonmyizer().run(parallel=0)
        instances = test_models.EverythingModel.objects.all()
        self.assertEqual(len(instances), self.NUM_ITEMS)
        for o in instances:
            # check everything has been changed
            self.assertFalse(o.username.startswith('initial'))

            # test for DjangoFaker.choice
            self.assertTrue(o.sex in ('M', 'F'))

            self.assertIsNotNone(o.some_datetime)
            self.assertNotEqual(o.some_datetime, self.now)

            self.assertIsNotNone(o.some_date)
            self.assertNotEqual(o.some_date, self.today)

            self.assertEqual(decompress(o.binary), o.id * -1)
