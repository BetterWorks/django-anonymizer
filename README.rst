===================
 Django Anonymizer
===================

Downloads: http://pypi.python.org/pypi/django-anonymizer

Intro
=====

This app helps you anonymize data in a database used for development of a Django
project.

It is common practice in develpment to use a database that is very similar in
content to the real data. The problem is that this can lead to having copies of
sensitive customer data on development machines. This Django app helps by
providing an easy and customizable way to anonymize data in your models.

The basic method is to go through all the models that you specify, and generate
fake data for all the fields specified. Introspection of the models will produce
an anonymizer that will attempt to provide sensible fake data for each field,
leaving you to tweak for your needs.

Please note that the methods provided may not be able to give full
anonymity. Even if you anonymize the names and other details of your customers,
there may well be enough data to identify them. Relationships between records in
the database are not altered, in order to preserve the characteristic structure
of data in your application, but this may leave you open to information leaks
which might not be acceptable for your data. This application **should** be good
enough for simpler policies like 'remove all real telephone numbers from the
database'.

An alternative approach to the problem of realistic amounts of test data for
development/tests is to populate a database from scratch - see `django-poseur
<https://github.com/alliterativeanimal/django-poseur>`_, `django-mockups
<https://github.com/sorl/django-mockups>`_, `django-eadred
<https://github.com/willkg/django-eadred>`_ and `django-autofixture
<https://github.com/gregmuellegger/django-autofixture>`_.  The disavantage of
that method is that the structure of the data - in terms of related models - can
be unrealistic.

Usage
=====

Quick overview (see docs for more information, either in docs/ or on
<http://packages.python.org/django-anonymizer>).

* Install using setup.py or pip/easy_install.

* Add 'anonymizer' to your ``INSTALLED_APPS`` setting.

* Create some stub files for your anonymizers::

    ./manage.py create_anonymizers app_name1 [app_name2...]

  This will create a file ``anonymizers.py`` in each of the apps you specify.
  (It will not overwrite existing files).

* Edit the generated ``anonymizers.py`` files, adjusting or deleting as
  necessary, using the functions in module ``anonymizer.replacers`` or
  custom functions.

* Run the anonymizers::

    ./manage.py anonymize_data app_name1 [app_name2...]

  This will DESTRUCTIVELY UPDATE all your data. Make sure you only do this on a
  copy of your database, use at own risk, yada yada.

* Note: your database may not actually delete the changed data from the disk
  when you update fields.  For Postgresql you will need to VACUUM FULL to
  delete that data.

  And even then, your operating system may not delete the data from the
  disk. Properly getting rid of these traces is left as an excercise to the
  reader :-)


Tests
=====

To run the test suite, do the following inside the folder containing this
README::

  ./manage.py test anonymizers

or::

  ./manage.py test anonymizers.tests
