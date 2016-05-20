from __future__ import unicode_literals

import re

from django.db.models import EmailField
from django.db.models.loading import get_models

field_replacers = {
    'AutoField': '"SKIP"',
    'ForeignKey': '"SKIP"',
    'ManyToManyField': '"SKIP"',
    'OneToOneField': '"SKIP"',
    'SlugField': '"SKIP"', # we probably don't want to change slugs
    'DateField': '"date"',
    'DateTimeField': '"datetime"',
    'BooleanField': '"bool"',
    'NullBooleanField': '"bool"',
    'IntegerField': '"integer"',
    'SmallIntegerField': '"small_integer"',
    'PositiveIntegerField': '"positive_integer"',
    'PositiveSmallIntegerField': '"positive_small_integer"',
    'DecimalField': '"decimal"',
}

# NB - order matters. 'address' is more generic so should be at the end.
charfield_replacers = [
    (r'(\b|_)full_name\d*', '"name"'),
    (r'(\b|_)first_name\d*', '"first_name"'),
    (r'(\b|_)last_name\d*', '"last_name"'),
    (r'(\b|_)user_name\d*', '"username"'),
    (r'(\b|_)username\d*', '"username"'),
    (r'(\b|_)name\d*', '"name"'),
    (r'(\b|_)email\d*', '"email"'),
    (r'(\b|_)town\d*', '"city"'),
    (r'(\b|_)city\d*', '"city"'),
    (r'(\b|_)county\d*', '"uk_county"'),
    (r'(\b|_)post_code\d*', '"uk_postcode"'),
    (r'(\b|_)postcode\d*', '"uk_postcode"'),
    (r'(\b|_)postal_code\d*', '"uk_postcode"'),
    (r'(\b|_)zip\d*', '"zip_code"'),
    (r'(\b|_)zipcode\d*', '"zip_code"'),
    (r'(\b|_)zip_code\d*', '"zip_code"'),
    (r'(\b|_)telephone\d*', '"phonenumber"'),
    (r'(\b|_)phone\d*', '"phonenumber"'),
    (r'(\b|_)mobile\d*', '"phonenumber"'),
    (r'(\b|_)tel\d*\b', '"phonenumber"'),
    (r'(\b|_)state\d*\b', '"state"'),
    (r'(\b|_)address\d*', '"full_address"'),
    (r'(\b|_)street\d*', '"street_address"'),
]

def get_replacer_for_field(field):
    # Some obvious ones:
    if isinstance(field, EmailField):
        return '"email"'

    # Use choices, if available.
    choices = getattr(field, 'choices', None)
    if choices is not None and len(choices) > 0:
        return '"choice"'

    field_type = field.get_internal_type()
    if field_type == "CharField" or field_type == "TextField":
        # Guess by the name

        # First, go for complete match
        for pattern, result in charfield_replacers:
            if re.match(pattern + "$", field.attname):
                return result

        # Then, go for a partial match.
        for pattern, result in charfield_replacers:
            if re.search(pattern, field.attname):
                return result

        # Nothing matched.
        if field_type == "TextField":
            return '"lorem"'

        # Just try some random chars
        return '"varchar"'


    try:
        r = field_replacers[field_type]
    except KeyError:
        r = "UNKNOWN_FIELD"

    return r

attribute_template = "        ('%(attname)s', %(replacer)s),"
class_template = """
class %(modelname)sAnonymizer(Anonymizer):

    model = %(modelname)s

    attributes = [
%(attributes)s
    ]
"""

def create_anonymizer(model):
    attributes = []
    fields = model._meta.fields
    # For the faker.name/username/email magic to work as expected and produce
    # consistent sets of names/email addreses, they must be accessed in the same
    # order. This will usually not be a problem, but if duplicate names are
    # produced and the field is unique=True, the logic in DjangoFaker for
    # getting new values from the 'source' means that the order will become out
    # of sync. To avoid this, we put fields with 'unique=True' at the beginning
    # of the list. Usually this will only be the username.
    sort_key = lambda f: not getattr(f, 'unique', False)
    fields.sort(key=sort_key)

    for f in fields:
        replacer = get_replacer_for_field(f)
        attributes.append(attribute_template % {'attname': f.attname,
                                                'replacer': replacer })
    return class_template % {'modelname':model.__name__,
                             'attributes': "\n".join(attributes) }


def create_anonymizers_module(app):
    model_names = []
    imports = []
    output = []
    output.append("")
    imports.append("from anonymizer import Anonymizer")
    for model in get_models(app):
        model_names.append(model.__name__)
        output.append(create_anonymizer(model))

    imports.insert(0, "from %s import %s" % (app.__name__, ", ".join(model_names)))

    return "\n".join(imports) + "\n".join(output)
