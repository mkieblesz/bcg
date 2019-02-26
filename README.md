# Progimage

Microservice which enables image upload, retrieval and type conversion.

## Solution

### Basic

* although not essential database is used for storing id of images for more reliable management
* pil library is used for image convertion and manipulation
* caching is done by create new image obj with same name

### Operating in bulk and performance

TODO

### Solution stretch - transform

Quick solution could be to use same image with different env paramaters. For example `settings.TRANSFORMATION_TYPE = env('TRANSFORM_TYPE')` will be provided by container vars passed to the view via urls `path('transform/', views.transform_image, name='transform-image', kwargs={'transformation_type': settings.TRANSFORMATION_TYPE}),`. Selecting appropriate service can be used by configuring nginx container.

Although I don't have experience with RPC it would be perhaps more elegant solution. There will be only one more service which will stand behind nginx and will rpc procedure calls depending on url, just like load balancing with nginx. It will be very simple and most of it's functionality would be very similar to strech shim lib solution. It would be preferable in cases where 2 services will need to be used in one api call, for example something like chained transformations.

### Solution stretch - shim lib

Because there are not many endpoints the client library should be very simple. It could be something like this:

```python
import requests

BASE_URL = 'http://progimage.com'


class ProgImageException(Exception):
    pass


class ProgImageClient:

    def __init__(self, api_id, api_secret, base_url=None):
        # if only for internal use insid vpc api_secret only can be used which is hardcoded in the api
        self.base_url = base_url or BASE_URL

    def request(self, method, url, **kwargs):
        response = getattr(requests, method)(url)
        if response.status_code != requests.codes.ok:
            raise ProgImageException('Status code error or response is not json')

        return response.json()

    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)

    def post(self, url, **kwargs):
        return self.request('POST', url, **kwargs)

    def get_image(self, image_id):
        return self.get('{}/image/{}/'.format(self.base_url, image_id))

    def upload_image(self, image_data):
        return self.post('{}/upload/'.format(self.base_url), data={'image': image_data})

    def convert_image(self, image_id, ext):
        return self.get('{}/image/{}/convert/{}/'.format(self.base_url, image_id, ext))

    def transform_image(self, image_id, transform_type):
        return self.get('{}/image/{}/transform/{}/'.format(self.base_url, image_id, transform_type))


client = ProgImageClient('client_id', 'client_secret')
client.get_image('3284u3284')
```

## Improvements

* check if PIL type conversion solution works for other types of images (it's very likely that it does) and use `django.core.validators.get_available_image_extensions`
* use image paths instead of primary key  in urls to allow conversion just by changing the extension of the file
* use better test runner like pytest so it can give better output to assert x == y
* make 404 always json and similar
* more tests for validation and model methods, more conversion testing
* seperate convertion functionality to new class from the model
* ensure unique file uploads

## Requirements

* docker >= `18.06.1-ce`
* docker-compose >= `1.22.0`

## Development

Run development environment with `make ultimate`.

## Test

### Running tests

In order to test microservice clone this repo and run `make ultimate`. After containers are up and running run `make test`.

### Testing production configuration

To fintetune production settings you can use test production containers with `make ultimate-prod`. In order to avoid 400 error you must point `prodimage.com` to `localhost` in your hosts settings.
