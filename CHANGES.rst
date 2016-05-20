Version 0.5.1
-------------

* Added unicode compatibility for anonymizer.py files
* Now with universal wheels
* Added a new maintainer

Version 0.5
-----------
* Python 3 compatibility

Version 0.4
-----------

* Changed 'Anonymizer.attributes' to require every field to be listed.  This is
  deal with the common security problem when a model is updated, but the
  Anonymizer is not updated.

  Fields that should not be anonymized should specify the special value "SKIP"
  as the 'replacer'.

* attributes must now be a list of tuples, not a dictionary.

Version 0.3
-----------

* Support for ``DecimalField``.
* Improved docs.
* Added tests

Version 0.2
-----------

* Changed format of attributes from a dictionary to a list of 2-tuples
  (with backwards compatibility - previous format is deprecated).
* Fixed small bug with names/usernames/emails sometimes not being generated in
  corresponding sets, due to fields with unique=True not being (reliably) set
  before other fields.
* Added docs.

Version 0.1.2
-------------

* Changed 'varchar' field to do max_length introspection at runtime.
  This breaks the previous signature of the function.
* Introduced 'replacers' module and new shortcuts.

Version 0.1.1
-------------

* Removed some debug code
* Better handling of SlugField and skipped fields in introspection

Version 0.1
-----------

Initial release
