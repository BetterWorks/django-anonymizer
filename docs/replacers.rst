=============================
Replacers - fake data sources
=============================

A 'replacer' is a source of faked data. The replacers in this module can be
referred to using a string that is simply the name of the function. They are
listed below.

Standard replacers
==================


.. automodule:: anonymizer.replacers
   :members:


Custom replacers
================

Custom replacers can be used by defining them as callables.

When run by the anonymizer, the callable will be passed the Anonymizer object,
the object being altered, the field being altered, and the current value of the
field. It must return random data of the appropriate type. You can use ``lambda
*args: my_constant_value`` to return a constant.

All of the replacers defined in this module use a
:class:`anonymizer.base.DjangoFaker` instance to generate fake data, and this
object may be of use to you in writing your own replacers. The ``DjangoFaker``
instance is available on the Anonymizer instance in the ``faker`` attribute. So,
you could have a replacer callable defined like this, which uses
:meth:`anonymizer.base.DjangoFaker.simple_pattern`::

    lambda anon, obj, field, val: anon.faker.simple_pattern('???##', field=field)
