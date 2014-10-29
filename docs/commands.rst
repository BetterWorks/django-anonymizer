========
Commands
========

.. _create-anonymizers-command:

create_anonymizers
------------------

.. code-block:: bash

  manage.py create_anonymizers <app name> [<app name 2>..]

For each model in each app, default anonymizers will be generated and saved in
``<app>/anonymizers.py``. For each field, the best guess 'replacer' will be
used, using the types and names of the Django fields defined. But you will
almost certainly have to edit the generated file to tweak the choices made, and
in many cases to completely remove anonymizers for models that don't need them.

Currently some fields are deliberately skipped - these include `ForeignKey`
fields and `ManyToManyField` relations.

Some fields type are also currently unsupported. The corresponding code
generated will produce an error on import, to indicate that it must be dealt
with before proceeding. Some of the missing fields could be added fairly easily
(requests welcome, patches even more so).

.. _anonymize-data-command:

anonymize_data
--------------

.. code-block:: bash

   manage.py anonymize_data <app name> [<app name 2>..]

Runs all the anonymizers defined in ``<app>/anonymizers.py``. This destructively
updates the data in your database, so be careful not to use on a live database!
