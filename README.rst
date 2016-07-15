django-media-fixtures
------------------------

Simple project to copy media files (intended for fixtures loads), pretty much as staticfiles does.


Dependencies
------------

- Django 1.8 or higher (not tested on previous versions)


Installation
------------

.. code-block:: python

   pip install django-media-fixtures==0.0.2

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