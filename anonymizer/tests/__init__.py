from datetime import datetime, timedelta, date
import decimal
import os
import sys

from django.conf import settings
from django.utils import unittest
from django.test import TestCase

from anonymizer import Anonymizer, introspect
from anonymizer.tests import models as test_models


class TestIntrospect(TestCase):

    def test_eveything(self):
        mod = introspect.create_anonymizers_module(test_models)
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
    ]
"""
        self.assertEqual(mod.strip(), expected.strip())

class TestAnonymizer(TestCase):

    # Nice high count, so that our handling of unique constraint with test data
    # will likely be tested.
    NUM_ITEMS = 1000

    def setUp(self):
        self.o1 = test_models.Other.objects.create()
        for x in range(0, self.NUM_ITEMS):
            d = datetime.now() + timedelta(365*x)
            test_models.EverythingModel.objects.create(o1=self.o1,
                                                       username="intial%d" % x,
                                                       birthday=d,
                                                       age=x,
                                                       some_datetime=datetime.now(),
                                                       some_date=date.today(),
                                                       sex='X',
                                                       price=decimal.Decimal("1.23"),
                                                       )

    def test_eveything(self):
        # Test for as much as possible in one test.
        assert test_models.EverythingModel.objects.count() == self.NUM_ITEMS
        assert test_models.EverythingModel._meta.get_field_by_name('username')[0].unique == True

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
            ]

        EverythingAnonmyizer().run()
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

