# Progimage

Microservice which enables image upload and retrieval.

## Solution

* although not essential database is used for storing id of images for more reliable management
* python pillow library is used for image manipulation
* caching transformed images can be implemented by using Image model pointing to original image from which transofrmation was made or writing directly to filesystem with expiration date by using cron
* use better test runner so it can give better output to assert x == y
* transformations will work same as type conversions (pil Image class has transformation functions like rotate etc.)

## Improvements

* use django rest framework or django class based views
* make 404 always json
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
