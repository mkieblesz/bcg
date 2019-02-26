import tempfile
from django.test import TestCase, override_settings
from django.urls import reverse

from progimage.models import Image


class ImageEndpointsTestCase(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_upload_image(self):
        with open('tests/data/test.jpg', 'rb') as image_file:
            response = self.client.post(reverse('upload-image'), data={'image': image_file})
        assert Image.objects.count() == 1
        assert response.json() == Image.objects.first().to_json()

    def test_get_image(self):
        image = Image.objects.create(image_file='test_image.png')
        response = self.client.get(reverse('get-image', kwargs={'image_id': image.id}))
        assert response.json() == image.to_json()

    def test_convert_same_ext(self):
        """Provided same extension as the one existing in database there should be no new image created"""
        image = Image.objects.create(image_file='test_image.jpg')
        response = self.client.get(reverse('get-converted-image', kwargs={'image_id': image.id, 'ext': 'jpg'}))
        assert Image.objects.count() == 1
        assert response.json() == image.to_json()

    def test_convert_ext_already_exists(self):
        """If extension for particular image already exists new image shouldn't be created"""

        image = Image.objects.create(image_file='test_image.jpg')
        converted_image = Image.objects.create(image_file='different_image.png', converted_from=image)
        assert Image.objects.count() == 2

        response = self.client.get(reverse('get-converted-image', kwargs={'image_id': image.id, 'ext': 'png'}))
        assert Image.objects.count() == 2
        assert response.json() == {'id': image.id, 'url': converted_image.get_image_url()}

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_convert_to_extension(self):
        with open('tests/data/test.jpg', 'rb') as image_file:
            response = self.client.post(reverse('upload-image'), data={'image': image_file})
        assert Image.objects.count() == 1

        url = reverse('get-converted-image', kwargs={'image_id': response.json()['id'], 'ext': 'png'})
        response = self.client.get(url)
        assert Image.objects.count() == 2
