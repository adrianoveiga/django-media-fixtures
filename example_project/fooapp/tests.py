# -*- coding: utf-8 -*-
from django.test import TestCase
from django_media_fixtures import finders
from django.core.files.storage import default_storage as media_storage
from django.core.management import call_command
 
 
class TestCollectMedia(TestCase):
 
    def test_sample_image_media_collected(self):
        self.assertEqual(media_storage.exists('uploads/foomodel/img/board.jpg'), False)
        call_command('collectmedia', verbosity=3, interactive=False)
        self.assertEqual(media_storage.exists('uploads/foomodel/img/board.jpg'), True)
