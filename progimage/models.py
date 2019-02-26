from django.conf import settings
from django.db import models


class Image(models.Model):
    image_file = models.ImageField(upload_to='images/')
    converted_from = models.ForeignKey('self', models.CASCADE, null=True, blank=True)

    def get_image_url(self):
        return 'http://{}/{}'.format(settings.SITE_URL, self.image_file.url)

    def get_extension(self):
        return self.image_file.name.split('.')[-1]

    def to_json(self):
        return {
            'id': self.id if not self.converted_from else self.converted_from.id,
            'url': self.get_image_url()
        }

    def get_extension_image(self, ext):
        if ext == self.get_extension():
            return self

        try:
            return Image.objects.get(image_file__endswith=ext, converted_from=self)
        except Image.DoesNotExist:
            return None

    def create_extension_image(self, ext):
        '''Creates extension as new image in database'''

        # TODO: convert image
        return None
