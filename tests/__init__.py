import tempfile
from django.test import TestCase, override_settings

from progimage.models import Image


class ImageEndpointsTestCase(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_upload_image(self):
        with open('tests/data/test.jpg', 'rb') as image_file:
            response = self.client.post('/upload/', data={'image': image_file})

        assert 'id' in response.json()
        assert Image.objects.count() == 1
        image = Image.objects.first()
        assert response.json() == {'url': image.get_image_url(), 'id': image.id}

    def test_get_image(self):
        image = Image.objects.create(image_file='test_image.png')
        response = self.client.get('/get/', data={'id': image.id})
        assert response.json() == {'url': image.get_image_url(), 'id': image.id}
