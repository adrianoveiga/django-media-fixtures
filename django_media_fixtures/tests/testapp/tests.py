# -*- coding: utf-8 -*-
from django.test import TestCase
from django_media_fixtures import finders
from django.core.files.storage import default_storage as media_storage
from django.core.management import call_command
 
 
class TestCollectMedia(TestCase):
 
    def test_sample_media_from_app_folder_collected(self):
        """
        Default behaviour, looking for the folder media_fixtures
        inside of all registered app's folders.
        """
        IMAGE_PATH = 'uploads/foomodel/img/board.jpg'
        if media_storage.exists(IMAGE_PATH):
            media_storage.delete(IMAGE_PATH)
        self.assertEqual(media_storage.exists(IMAGE_PATH), False)
        call_command('collectmedia', verbosity=3, interactive=False)
        self.assertEqual(media_storage.exists(IMAGE_PATH), True)

    def test_sample_media_from_custom_folder_collected(self):
        """
        Testing collect media from custom file directories, defined on
        MEDIA_FIXTURES_FILES_DIRS settings variable.
        NOTE: To use this option, you need add
        'django_media_fixtures.finders.FileSystemFinder' on
        MEDIA_FIXTURES_FILES_FINDERS settings variable.
        """
        FILE_PATH = 'uploads/attachments/example_file.txt'
        if media_storage.exists(FILE_PATH):
            media_storage.delete(FILE_PATH)
        self.assertEqual(media_storage.exists(FILE_PATH), False)
        call_command('collectmedia', verbosity=3, interactive=False)
        self.assertEqual(media_storage.exists(FILE_PATH), True)
