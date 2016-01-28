import decimal
import random
import sys
from collections import defaultdict
from datetime import datetime
from multiprocessing import Pool
from uuid import uuid4

from anonymizer import replacers
from django.db import connection, transaction
from faker import Faker, data
from faker.utils import bothify, uk_postcode

randrange = random.SystemRandom().randrange

alphanumeric = ""
for i in range(ord('A'), ord('Z')+1):
    alphanumeric += chr(i)
for i in range(ord('a'), ord('z')+1):
    alphanumeric += chr(i)
for i in range(ord('0'), ord('9')+1):
    alphanumeric += chr(i)

general_chars = alphanumeric + " _-"


class DjangoFaker(object):
    """
    Class that provides fake data, using Django specific knowledge to ensure
    acceptable data for Django models.
    """
    faker = Faker()

    def __init__(self):
        self.init_values = {}
        self.unique_suffixes = defaultdict(int)

    def _prep_init(self, field):
        if field in self.init_values:
            return

        field_vals = set(x[0] for x in field.model._default_manager.values_list(field.name))
        self.init_values[field] = field_vals

    def get_allowed_value(self, source, field):
        retval = source()
        if field is None:
            return retval

        # Enforce unique.  Ensure we don't set the same values, as either
        # any of the existing values, or any of the new ones we make up.
        unique = getattr(field, 'unique', None)
        if unique:
            self._prep_init(field)
            used = self.init_values[field]
            for i in xrange(0, 20):
                if retval in used:
                    retval = source()
                else:
                    break

            if retval in used:
                raise Exception("Cannot generate unique data for field %s. Last value tried %s" % (field, retval))
            used.add(retval)

        # Enforce max_length
        max_length = getattr(field, 'max_length', None)
        if max_length is not None:
            retval = retval[:max_length]

        return retval

    ### Public interace ##
    def uuid(self, field=None):
        retval = str(uuid4())
        max_length = getattr(field, 'max_length', None)
        if max_length is not None:
            retval = retval[:max_length]
        return retval

    def varchar(self, field=None):
        """
        Returns a chunk of text, of maximum length 'max_length'
        """
        assert field is not None, "The field parameter must be passed to the 'varchar' method."
        max_length = field.max_length
        def source():
            length = random.choice(range(1, max_length + 1))
            return "".join(random.choice(general_chars) for i in xrange(length))
        return self.get_allowed_value(source, field)

    def simple_pattern(self, pattern, field=None):
        """
        Use a simple pattern to make the field - # is replaced with a random number,
        ? with a random letter.
        """
        source = lambda: bothify(pattern)
        return self.get_allowed_value(source, field)

    def bool(self, field=None):
        """
        Returns a random boolean
        """
        source = lambda: bool(randrange(0, 2))
        return self.get_allowed_value(source, field)

    def integer(self, field=None):
        source = lambda: random.randint(-1000000, 1000000)
        return self.get_allowed_value(source, field)

    def positive_integer(self, field=None):
        source = lambda: random.randint(0, 1000000)
        return self.get_allowed_value(source, field)

    def small_integer(self, field=None):
        source = lambda: random.randint(-32768, +32767)
        return self.get_allowed_value(source, field)

    def positive_small_integer(self, field=None):
        source = lambda: random.randint(0, 32767)
        return self.get_allowed_value(source, field)

    def datetime(self, field=None, val=None):
        """
        Returns a random datetime. If 'val' is passed, a datetime within two
        years of that date will be returned.
        """
        if val is None:
            source = lambda: datetime.fromtimestamp(randrange(1, 2100000000))
        else:
            source = lambda: datetime.fromtimestamp(int(val.strftime("%s")) +
                                                    randrange(-365*24*3600*2, 365*24*3600*2))
        return self.get_allowed_value(source, field)

    def date(self, field=None, val=None):
        """
        Like datetime, but truncated to be a date only
        """
        d = self.datetime(field=field, val=val)
        return d.date()

    def decimal(self, field=None, val=None):
        source = lambda: decimal.Decimal(random.randrange(0, 100000))/(10**field.decimal_places)
        return self.get_allowed_value(source, field)

    def uk_postcode(self, field=None):
        return self.get_allowed_value(uk_postcode, field)

    def uk_county(self, field=None):
        source = lambda: random.choice(data.UK_COUNTIES)
        return self.get_allowed_value(source, field)

    def uk_country(self, field=None):
        source = lambda: random.choice(data.UK_COUNTRIES)
        return self.get_allowed_value(source, field)

    def lorem(self, field=None, val=None):
        """
        Returns lorem ipsum text. If val is provided, the lorem ipsum text will
        be the same length as the original text, and with the same pattern of
        line breaks.
        """
        if val is not None:
            def generate(length):
                # Get lorem ipsum of a specific length.
                collect = ""
                while len(collect) < length:
                    collect += self.faker.lorem()
                collect = collect[:length]
                return collect

            # We want to match the pattern of the text - linebreaks
            # in the same places.
            def source():
                parts = val.split("\n")
                for i, p in enumerate(parts):
                    # Replace each bit with lorem ipsum of the same length
                    parts[i] = generate(len(p))
                return "\n".join(parts)
        else:
            source = self.faker.lorem
        return self.get_allowed_value(source, field)

    def unique_lorem(self, field=None, val=None):
        """
        Returns lorem ipsum text guaranteed to be unique. First uses lorem function
        then adds a unique integer suffix.
        """
        lorem_text = self.lorem(field, val)
        max_length = getattr(field, 'max_length', None)

        suffix_str = str(self.unique_suffixes[field])
        unique_text = lorem_text + suffix_str
        if max_length is not None:
            # take the last max_length chars
            unique_text = unique_text[-max_length:]
        self.unique_suffixes[field] += 1
        return unique_text

    def choice(self, field=None):
        assert field is not None, "The field parameter must be passed to the 'choice' method."
        choices = [c[0] for c in field.choices]
        source = lambda: random.choice(choices)
        return self.get_allowed_value(source, field)

    ## Other attributes provided by 'Faker':

    # username
    # first_name
    # last_name
    # name
    # email
    # full_address
    # phonenumber
    # street_address
    # city
    # state
    # zip_code
    # company

    def __getattr__(self, name):
        # we delegate most calls to faker, but add checks
        source = getattr(self.faker, name)

        def func(*args, **kwargs):
            field = kwargs.get('field', None)
            return self.get_allowed_value(source, field)
        return func


class Anonymizer(object):
    """
    Base class for all anonymizers. When executed with the ``run()`` method,
    it will anonymize the data for a specific model.
    """

    model = None
    # attributes is a dictionary of {attribute_name: replacer}, where replacer is
    # a callable that takes as arguments this Anonymizer instance, the object to
    # be altered, the field to be altered, and the current field value, and
    # returns a replacement value.

    # This signature is designed to be useful for making lambdas that call the
    # 'faker' instance provided on this class, but it can be used with any
    # function.

    attributes = None

    # To impose an order on Anonymizers within a module, this can be set - lower
    # values are done first.
    order = 0

    faker = DjangoFaker()

    def get_queryset(self):
        """
        Returns the QuerySet to be manipulated
        """
        if self.model is None:
            raise Exception("'model' attribute must be set")
        qs = (self.model._default_manager.get_queryset()
                                         .select_related(None)
                                         .order_by('pk'))
        return qs

    def get_queryset_chunk_iterator(self, chunksize):
        queryset = self.get_queryset()
        num_rows = queryset.count()

        index = 0
        while index < num_rows:
            yield queryset[index:index + chunksize]
            index += chunksize

    def get_attributes(self):
        if self.attributes is None:
            raise Exception("'attributes' attribute must be set")
        return self.attributes

    def alter_object(self, obj):
        """
        Alters all the attributes in an individual object.

        If it returns False, the object will not be saved
        """
        attributes = self.get_attributes()
        for attname, replacer in attributes:
            if replacer == "SKIP":
                continue
            self.alter_object_attribute(obj, attname, replacer)

    def alter_object_attribute(self, obj, attname, replacer):
        """
        Alters a single attribute in an object.
        """
        currentval = getattr(obj, attname)
        field = obj._meta.get_field_by_name(attname)[0]
        if isinstance(replacer, str):
            # 'email' is shortcut for: replacers.email
            replacer = getattr(replacers, replacer)
        elif not callable(replacer):
            raise Exception("Expected callable or string to be passed, got %r." % replacer)

        replacement = replacer(self, obj, field, currentval)

        setattr(obj, attname, replacement)

    def run(self, chunksize=2000, parallel=4):
        self.validate()
        print '\n' + self.model.__name__
        sys.stdout.write('.')

        chunks = self.get_queryset_chunk_iterator(chunksize)

        if parallel == 0:
            for objs in chunks:
                _run(self, objs)
        else:
            connection.close()
            pool = Pool(processes=parallel)
            futures = [pool.apply_async(_run, (self, objs))
                       for objs in chunks]
            for future in futures:
                future.get()
                sys.stdout.write('.')
            pool.close()
            pool.join()

        print ''

    def validate(self):
        attributes = self.get_attributes()
        model_attrs = set(f.attname for f in self.model._meta.fields)
        given_attrs = set(name for name,replacer in attributes)
        if model_attrs != given_attrs:
            msg = ""
            missing_attrs = model_attrs - given_attrs
            if missing_attrs:
                msg += "The following fields are missing: %s. " % ", ".join(missing_attrs)
                msg += "Add the replacer \"SKIP\" to skip these fields."
            extra_attrs = given_attrs - model_attrs
            if extra_attrs:
                msg += "The following non-existent fields were supplied: %s." % ", ".join(extra_attrs)
            raise ValueError("The attributes list for %s does not match the complete list of fields for that model. %s" % (self.model.__name__, msg))

    def create_replacer_attributes(self):
        replacer_attrs = []
        for attr in self.attributes:
            if attr[1] != 'SKIP':
                replacer_attrs.append(attr[0])
        return replacer_attrs

    def create_query(self, replacer_attrs):
        query = 'UPDATE %s SET ' % self.model._meta.db_table
        for attr in replacer_attrs:
            query += '%s = ?, ' % attr
        query = query[:-2] + ' where %s = ?' % self.model._meta.pk.column
        # django expects %s, not ?, but we use %s to generate the query
        return query.replace('?', '%s')

    def create_query_args(self, updates, replacer_attrs):
        all_args = []
        for k, v in updates.iteritems():
            args = [v[attr] for attr in replacer_attrs]
            # pk is always the last argument in this query
            args.append(k)
            all_args.append(tuple(args))
        return all_args


def _run(anonymizer, objs):
    values = {}
    for obj in objs.iterator():
        retval = anonymizer.alter_object(obj)
        if retval is False:
            continue
        updates = {}
        for attname, replacer in anonymizer.get_attributes():
            if replacer == "SKIP":
                continue
            updates[attname] = getattr(obj, attname)

        values[obj.pk] = updates

    replacer_attr = anonymizer.create_replacer_attributes()
    query = anonymizer.create_query(replacer_attr)
    query_args = anonymizer.create_query_args(values, replacer_attr)

    with transaction.atomic():
        with connection.cursor() as cursor:
            if connection.vendor == 'postgresql':
                cursor.execute('SET CONSTRAINTS ALL DEFERRED')
            cursor.executemany(query, query_args)

    sys.stdout.write('.')
    sys.stdout.flush()
