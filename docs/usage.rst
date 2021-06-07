=====
Usage
=====

To use NgoSubscription in a project, add it to your `INSTALLED_APPS`:

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
