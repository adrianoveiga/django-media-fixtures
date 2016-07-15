import os
from collections import OrderedDict

from django.apps import apps
from django.conf import settings
from django.contrib.staticfiles import utils
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import (
    FileSystemStorage, Storage, default_storage,
)
from django.utils import lru_cache, six
from django.utils._os import safe_join
from django.utils.module_loading import import_string

from django.contrib.staticfiles.finders import BaseFinder

# To keep track on which directories the finder has searched the media files.
searched_locations = []


class FileSystemFinder(BaseFinder):
    """
    A media files finder that uses the ``MEDIA_FIXTURES_FILES_DIRS`` setting
    to locate files.
    """
    def __init__(self, app_names=None, *args, **kwargs):
        # List of locations with media_fixtures files
        self.locations = []
        # Maps dir paths to an appropriate storage instance
        self.storages = OrderedDict()
        if not isinstance(settings.MEDIA_FIXTURES_FILES_DIRS, (list, tuple)):
            raise ImproperlyConfigured(
                "Your MEDIA_FIXTURES_FILES_DIRS setting is not a tuple or list; "
                "perhaps you forgot a trailing comma?")
        for root in settings.MEDIA_FIXTURES_FILES_DIRS:
            if isinstance(root, (list, tuple)):
                prefix, root = root
            else:
                prefix = ''
            if settings.MEDIA_ROOT and os.path.abspath(settings.MEDIA_ROOT) == os.path.abspath(root):
                raise ImproperlyConfigured(
                    "The MEDIA_FIXTURES_FILES_DIRS setting should "
                    "not contain the MEDIA_ROOT setting")
            if (prefix, root) not in self.locations:
                self.locations.append((prefix, root))
        for prefix, root in self.locations:
            filesystem_storage = FileSystemStorage(location=root)
            filesystem_storage.prefix = prefix
            self.storages[root] = filesystem_storage
        super(FileSystemFinder, self).__init__(*args, **kwargs)

    def find(self, path, all=False):
        """
        Looks for files in the extra locations
        as defined in ``MEDIA_FIXTURES_FILES_DIRS``.
        """
        matches = []
        for prefix, root in self.locations:
            if root not in searched_locations:
                searched_locations.append(root)
            matched_path = self.find_location(root, path, prefix)
            if matched_path:
                if not all:
                    return matched_path
                matches.append(matched_path)
        return matches

    def find_location(self, root, path, prefix=None):
        """
        Finds a requested media file in a location, returning the found
        absolute path (or ``None`` if no match).
        """
        if prefix:
            prefix = '%s%s' % (prefix, os.sep)
            if not path.startswith(prefix):
                return None
            path = path[len(prefix):]
        path = safe_join(root, path)
        if os.path.exists(path):
            return path

    def list(self, ignore_patterns):
        """
        List all files in all locations.
        """
        for prefix, root in self.locations:
            storage = self.storages[root]
            for path in utils.get_files(storage, ignore_patterns):
                yield path, storage


class AppDirectoriesFinder(BaseFinder):
    """
    A media fixture files finder that looks in the directory of each app as
    specified in the source_dir attribute.
    """
    storage_class = FileSystemStorage
    source_dir = 'media_fixtures'
    
    if hasattr(settings, 'MEDIA_FIXTURE_FOLDERNAME'):
        source_dir = settings.MEDIA_FIXTURE_FOLDERNAME

    def __init__(self, app_names=None, *args, **kwargs):
        # The list of apps that are handled
        self.apps = []
        # Mapping of app names to storage instances
        self.storages = OrderedDict()
        app_configs = apps.get_app_configs()
        if app_names:
            app_names = set(app_names)
            app_configs = [ac for ac in app_configs if ac.name in app_names]
        for app_config in app_configs:
            app_storage = self.storage_class(
                os.path.join(app_config.path, self.source_dir))
            if os.path.isdir(app_storage.location):
                self.storages[app_config.name] = app_storage
                if app_config.name not in self.apps:
                    self.apps.append(app_config.name)
        super(AppDirectoriesFinder, self).__init__(*args, **kwargs)

    def list(self, ignore_patterns):
        """
        List all files in all app storages.
        """
        for storage in six.itervalues(self.storages):
            if storage.exists(''):  # check if storage location exists
                for path in utils.get_files(storage, ignore_patterns):
                    yield path, storage

    def find(self, path, all=False):
        """
        Looks for files in the app directories.
        """
        matches = []
        for app in self.apps:
            app_location = self.storages[app].location
            if app_location not in searched_locations:
                searched_locations.append(app_location)
            match = self.find_in_app(app, path)
            if match:
                if not all:
                    return match
                matches.append(match)
        return matches

    def find_in_app(self, app, path):
        """
        Find a requested media file in an app's media fixtures locations.
        """
        storage = self.storages.get(app, None)
        if storage:
            # only try to find a file if the source dir actually exists
            if storage.exists(path):
                matched_path = storage.path(path)
                if matched_path:
                    return matched_path


def get_finders():
    """
    Set the media fixtures finders on settings.py. 
    Example:
        MEDIA_FIXTURES_FILES_FINDERS = (
            'django_media_fixtures.finders.FileSystemFinder',
            'django_media_fixtures.finders.AppDirectoriesFinder',  # default
        )
    """
    if hasattr(settings, 'MEDIA_FIXTURES_FILES_FINDERS'):
        finders = settings.MEDIA_FIXTURES_FILES_FINDERS
    else:
        finders = (
            'django_media_fixtures.finders.AppDirectoriesFinder',
        )

    for finder_path in finders:
        yield get_finder(finder_path)


@lru_cache.lru_cache(maxsize=None)
def get_finder(import_path):
    """
    Imports the media fixtures files finder class described by import_path, where
    import_path is the full Python path to the class.
    """
    Finder = import_string(import_path)
    if not issubclass(Finder, BaseFinder):
        raise ImproperlyConfigured('Finder "%s" is not a subclass of "%s"' %
                                   (Finder, BaseFinder))
    return Finder()
