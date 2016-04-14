# Pre-built replacers.


def uuid(anon, obj, field, val):
    """
    Returns a random uuid string
    """
    return anon.faker.uuid(field=field)


def varchar(anon, obj, field, val):
    """
    Returns random data for a varchar field.
    """
    return anon.faker.varchar(field=field)


def bool(anon, obj, field, val):
    """
    Returns a random boolean value (True/False)
    """
    return anon.faker.bool(field=field)


def integer(anon, obj, field, val):
    """
    Returns a random integer (for a Django IntegerField)
    """
    return anon.faker.integer(field=field)


def positive_integer(anon, obj, field, val):
    """
    Returns a random positive integer (for a Django PositiveIntegerField)
    """
    return anon.faker.positive_integer(field=field)


def small_integer(anon, obj, field, val):
    """
    Returns a random small integer (for a Django SmallIntegerField)
    """
    return anon.faker.small_integer(field=field)


def positive_small_integer(anon, obj, field, val):
    """
    Returns a positive small random integer (for a Django PositiveSmallIntegerField)
    """
    return anon.faker.positive_small_integer(field=field)


def datetime(anon, obj, field, val):
    """
    Returns a random datetime
    """
    return anon.faker.datetime(field=field)


def date(anon, obj, field, val):
    """
    Returns a random date
    """
    return anon.faker.date(field=field)


def decimal(anon, obj, field, val):
    """
    Returns a random decimal
    """
    return anon.faker.decimal(field=field)


def postcode(anon, obj, field, val):
    """
    Generates a random postcode (not necessarily valid, but it will look like one).
    """
    return anon.faker.postcode(field=field)


def country(anon, obj, field, val):
    """
    Returns a randomly selected country.
    """
    return anon.faker.country(field=field)


def username(anon, obj, field, val):
    """
    Generates a random username
    """
    return anon.faker.user_name(field=field)


def first_name(anon, obj, field, val):
    """
    Returns a random first name
    """
    return anon.faker.first_name(field=field)


def last_name(anon, obj, field, val):
    """
    Returns a random second name
    """
    return anon.faker.last_name(field=field)


def name(anon, obj, field, val):
    """
    Generates a random full name (using first name and last name)
    """
    return anon.faker.name(field=field)


def email(anon, obj, field, val):
    """
    Generates a random email address.
    """
    return anon.faker.email(field=field)


def similar_email(anon, obj, field, val):
    """
    Generate a random email address using the same domain.
    """
    return val if 'betterworks.com' in val else '@'.join([anon.faker.user_name(field=field), val.split('@')[-1]])


def full_address(anon, obj, field, val):
    """
    Generates a random full address, using newline characters between the lines.
    Resembles a US address
    """
    return anon.faker.address(field=field)


def phonenumber(anon, obj, field, val):
    """
    Generates a random US-style phone number
    """
    return anon.faker.phone_number(field=field)


def street_address(anon, obj, field, val):
    """
    Generates a random street address - the first line of a full address
    """
    return anon.faker.street_address(field=field)


def city(anon, obj, field, val):
    """
    Generates a random city name. Resembles the name of US/UK city.
    """
    return anon.faker.city(field=field)


def state(anon, obj, field, val):
    """
    Returns a randomly selected US state code
    """
    return anon.faker.state(field=field)


def zip_code(anon, obj, field, val):
    """
    Returns a randomly generated US zip code (not necessarily valid, but will look like one).
    """
    return anon.faker.zipcode(field=field)


def company(anon, obj, field, val):
    """
    Generates a random company name
    """
    return anon.faker.company(field=field)


def lorem(anon, obj, field, val):
    """
    Generates a paragraph of lorem ipsum text
    """
    return ' '.join(anon.faker.sentences(field=field))


def unique_lorem(anon, obj, field, val):
    """
    Generates a unique paragraph of lorem ipsum text
    """
    return anon.faker.unique_lorem(field=field)


def similar_datetime(anon, obj, field, val):
    """
    Returns a datetime that is within plus/minus two years of the original datetime
    """
    return anon.faker.datetime(field=field, val=val)


def similar_date(anon, obj, field, val):
    """
    Returns a date that is within plus/minus two years of the original date
    """
    return anon.faker.date(field=field, val=val)


def similar_lorem(anon, obj, field, val):
    """
    Generates lorem ipsum text with the same length and same pattern of linebreaks
    as the original. If the original often takes a standard form (e.g. a single word
    'yes' or 'no'), this could easily fail to hide the original data.
    """
    return anon.faker.lorem(field=field, val=val)


def choice(anon, obj, field, val):
    """
    Randomly chooses one of the choices set on the field.
    """
    return anon.faker.choice(field=field)
