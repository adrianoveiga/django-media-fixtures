|badge1| |badge2| |badge3| |badge4| |badge5|

.. |badge1| image:: https://travis-ci.org/adrianoveiga/django-media-fixtures.svg?branch=master
    :target: https://travis-ci.org/adrianoveiga/django-media-fixtures
    :alt: Build Status

.. |badge2| image:: https://coveralls.io/repos/github/adrianoveiga/django-media-fixtures/badge.svg?branch=master
    :target: https://coveralls.io/github/adrianoveiga/django-media-fixtures?branch=master
    :alt: Coverage

.. |badge3| image:: https://img.shields.io/pypi/v/django-media-fixtures.svg
    :target: https://pypi.org/project/django-media-fixtures/
    :alt: PyPI Version

.. |badge4| image:: https://img.shields.io/pypi/pyversions/django-media-fixtures.svg
    :target: https://pypi.org/project/django-media-fixtures/
    :alt: Python Versions

.. |badge5| image:: https://img.shields.io/pypi/l/django-media-fixtures.svg
    :target: https://pypi.org/project/django-media-fixtures/
    :alt: License

django-media-fixtures
------------------------

Simple project to copy media files (intended for fixtures loads), pretty much as staticfiles does.


Dependencies
------------

- Python 3.5+
- Django 1.8+

**Note**: The version (v1.x.x) dropped support of Python2! If you still need Python2, please check the last version of `v0.1.x series <https://github.com/adrianoveiga/django-media-fixtures/tree/version/0.1.x>`_


Installation
------------

.. code-block:: python

   pip install django-media-fixtures==1.0.0

Then, put 'django_media_fixtures' on your INSTALLED_APPS (on settings.py), just below 'django.contrib.staticfiles'.


Usage
-----

Just call manage command 'collectmedia', same as you do with collectstatic:

.. code-block:: python

    python manage.py collectmedia

And then all files on 'media_fixtures' folder in-apps will be copied to your MEDIA_ROOT.

So, when you create your fixture (for any ways, even through shell), put your file path matching the same tree folder view as your media file.

For instance,

.. code-block:: python

    YourModel.objects.get_or_create(image="uploads/yourmodel/img/example.jpg")

Where the file 'example.jpg' is on: yourappfolder/media_fixtures/uploads/yourmodel/img/example.jpg


Configurations
--------------

- MEDIA_FIXTURE_FOLDERNAME
    You can change the media fixtures folder's name on your apps, just putting this variable on settings.py. 

    .. code-block:: python
        
        MEDIA_FIXTURE_FOLDERNAME='my_media_fixtures_folder'

- MEDIA_FIXTURES_FILES_FINDERS
    You can change the media fixtures finders, to search media files on other folders not in-app, for instance. 
    
    .. code-block:: python
        
        MEDIA_FIXTURES_FILES_FINDERS = (
                'django_media_fixtures.finders.FileSystemFinder',      # combined with MEDIA_FIXTURES_FILES_DIRS, choose specific folders
                'django_media_fixtures.finders.AppDirectoriesFinder',  # default (if you do not set MEDIA_FIXTURES_FILES_FINDERS)
        )

- MEDIA_FIXTURES_FILES_DIRS
    You can list specific media folders that you want to include on search.

    .. code-block:: python

        MEDIA_FIXTURES_FILES_DIRS = [
            "/home/user/myproject/mediafiles",
            "/opt/webfiles/common/",
        ]
