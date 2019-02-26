from django.conf import settings
from django.db import models


class Image(models.Model):
    image_file = models.ImageField(upload_to='images/')

    def get_image_url(self):
        return 'http://{}/{}'.format(settings.SITE_URL, self.image_file.url)

    def to_json(self):
        return {'id': self.id, 'url': self.get_image_url()}
