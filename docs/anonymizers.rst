===================
Writing Anonymizers
===================

For each model, you need a subclass of :class:`anonymizer.base.Anonymizer`. They
can be automatically generated using the :ref:`create-anonymizers-command`
command.

The main attributes that must be set are ``model`` and ``attributes``. You can
also override other methods to customise the process.


.. class:: anonymizer.base.Anonymizer

   .. attribute:: model

      This is the Django model that will be anonymized.

   .. attribute:: attributes

      This should be a list of 2-tuples, where the first value is the name of an
      attribute on the model that need to be set (i.e. usually a field name),
      and the second value specifies a 'replacer' - a source of faked data. The
      replacer is either a string or a callable:

      * If the replacer is string, it will be interpreted as a function in the
        module :mod:`anonymizer.replacers`.

      * If the replacer is a callable, it should have a signature compatible
        with the callables in :mod:`anonymizer.replacers` - see the
        documentation in that module for writing your own replacers.

      Note that the order the fields are listed can be important. If you have a
      username field with ``unique=True``, for example, it will help if this comes
      before other fields like name (see :class:`anonymizer.base.DjangoFaker`
      for more details).

      For security in the case of new fields being added to the model, the list
      must contain all attributes corresponding to fields on the model. To
      specify that an attribute should not be altered, using the string "SKIP".

   .. attribute:: order

      Sometimes it is important that some anonymizers are run before others.  By
      default, this value is zero, but you can set it to any other numeric
      value. The anonymizers will be sorted by this attribute before being run.

   .. method:: get_query_set(self)

      Returns the QuerySet to be manipulated.

      The default implementation uses the default manager for the model, and
      returns all objects, ordered by the 'id' field if it exists. You can
      override this method to change that.

   .. method:: alter_object(self, obj)

      Alters the object (but does not save).

      Override this method to add custom behaviour for altering an object. This
      is especially useful if for some fields/rows you want to add some logic
      that cannot easily be written as a 'replacer'.

   .. method:: alter_object_attribute(self, obj, attname, replacer)

      Alters the attribute 'attname' on object 'obj', using the replacement
      source 'replacer'
