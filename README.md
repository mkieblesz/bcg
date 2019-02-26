# Progimage

Microservice which enables image upload and retrieval.

## Solution

* using database for storing images for more reliable image management

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
