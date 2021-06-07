=============================
NgoSubscription
=============================

.. image:: https://badge.fury.io/py/django-ngosubs.svg
    :target: https://badge.fury.io/py/django-ngosubs

.. image:: https://travis-ci.org/numengo/django-ngosubs.svg?branch=master
    :target: https://travis-ci.org/numengo/django-ngosubs

.. image:: https://codecov.io/gh/numengo/django-ngosubs/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/numengo/django-ngosubs

django plugin to add subscription to django-cms/shop

Documentation
-------------

The full documentation is at https://django-ngosubs.readthedocs.io.

Quickstart
----------

Install NgoSubscription::

    pip install django-ngosubs

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'ngosubs.apps.NgosubscriptionConfig',
        ...
    )

Add NgoSubscription's URL patterns:

.. code-block:: python

    from ngosubs import urls as ngosubs_urls


    urlpatterns = [
        ...
        url(r'^', include(ngosubs_urls)),
        ...
    ]

Settings are managed using
`simple-settings <https://raw.githubusercontent.com/drgarcia1986/simple-settings>`__
and can be overriden with configuration files (cfg, yaml, json) or with environment variables
prefixed with DJANGO-NGOSUBS_.

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
