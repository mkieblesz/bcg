import io
import os
from django.conf import settings
from django.core.files.images import ImageFile
from django.db import models
from PIL import Image as PILImage


class Image(models.Model):
    ALLOWED_CONVERSIONS = {'png': ['jpg'], 'jpg': ['png']}

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

    def get_converted_image(self, ext):
        try:
            return Image.objects.get(image_file__endswith=ext, converted_from=self)
        except Image.DoesNotExist:
            return None

    def can_convert_to(self, ext):
        return ext in Image.ALLOWED_CONVERSIONS.get(self.get_extension(), [])

    def convert_image(self, ext):
        '''Creates extension as new image in database'''

        # pil will convert image automatically after save https://stackoverflow.com/a/10759145
        im = PILImage.open(self.image_file)
        im_buffer = io.BytesIO()
        try:
            im.save(im_buffer, format=ext)
            image = Image(converted_from=self)

            # swap extension, keep filename
            pre, _ = os.path.splitext(os.path.basename(self.image_file.name))
            converted_filename = '{}.{}'.format(pre, ext)

            image.image_file.save(converted_filename, ImageFile(im_buffer))
        finally:
            im_buffer.close()

        image.save()

        return image
