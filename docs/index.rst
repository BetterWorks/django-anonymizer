.. Django Anonymizer documentation master file, created by
   sphinx-quickstart on Mon Dec 27 17:00:15 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Django Anonymizer's documentation!
=============================================

Django Anonymizer helps you anonymize data in a database used for development of
a Django project.

It is common practice in develpment to use a database that is very similar in
content to the real data, and sometimes you need the live data on a developer's
machine in order to reproduce a bug. The problem is that this can lead to having
copies of sensitive customer data on development machines and other places (like
automatic backups).

This app helps by providing an easy and customizable way to anonymize data in
your models. It is designed for fairly small databases (or databases that have
already been reduced to a small size) - otherwise the anonymization process will
simply take too long to execute.

Please note that the methods provided may not be able to give full
anonymity. Even if you anonymize the names and other details of your customers,
there may well be enough data to identify them. Relationships between records in
the database are not altered, in order to preserve the characteristic structure
of data in your application, but this may leave you open to information leaks
which might not be acceptable for your data. This application **should** be good
enough for simpler policies like 'remove all real telephone numbers from the
database'.


Contents:

.. toctree::
   :maxdepth: 2

   install
   overview
   commands
   anonymizers
   replacers
   djangofaker

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

