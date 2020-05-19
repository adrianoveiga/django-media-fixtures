from django.test import TestCase
from django.core.files.storage import default_storage as media_storage
from django.core.management import call_command
from django_media_fixtures import finders
from pathlib import Path


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

    def test_searching_media_by_fixtures_finders(self):
        """
        Testing get the files by the media_fixtures finders directly,
        not by default_storage from Django.
        """
        IMAGE_PATH = 'uploads/foomodel/img/board.jpg'
        FILE_PATH = 'uploads/attachments/example_file.txt'
        call_command('collectmedia', clear=True,
                     verbosity=3, interactive=False)
        media_finders = finders.get_finders()

        # searching for the image and the text file, where each one need a
        # different finder (AppDirectoriesFinder or FileSystemFinder)
        has_found_img = False
        has_found_file = False
        for finder in media_finders:
            if not has_found_img:
                has_found_img = finder.find(IMAGE_PATH) or False
            if not has_found_file:
                has_found_file = finder.find(FILE_PATH) or False

        self.assertTrue(has_found_img)
        self.assertTrue(has_found_file)

    def test_list_mediafiles_by_fixtures_finders(self):
        """Simple test to assert finders can list the files."""
        call_command('collectmedia', verbosity=3, interactive=False)
        media_finders = finders.get_finders()
        files_found = []
        for finder in media_finders:
            for file in finder.list():
                files_found.append(file)
        self.assertTrue(files_found)

    def test_symbolic_link_on_collectmedia(self):
        """Simple test to assert collectmedia can make symbolic links."""
        call_command('collectmedia', link=True, clear=True,
                     verbosity=3, interactive=False)
        media_finders = finders.get_finders()
        files_found = []
        for finder in media_finders:
            for file in finder.list():
                files_found.append(file)
                self.assertTrue(Path(media_storage.path(file[0])).is_symlink())
        self.assertTrue(files_found)
