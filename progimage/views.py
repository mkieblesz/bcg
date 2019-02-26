from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from progimage.models import Image


@require_http_methods(['POST'])
def upload_image(request, ext=None):
    image = Image.objects.create(image_file=request.FILES.get('image'))

    return JsonResponse(image.to_json())


@require_http_methods(['GET'])
def get_image(request, image_id):
    try:
        image = Image.objects.get(id=image_id)
    except Image.DoesNotExist:
        return JsonResponse({'error': 'Image Not Found'}, status=404)

    return JsonResponse(image.to_json(), status=200)


@require_http_methods(['GET'])
def get_converted_image(request, image_id, ext=None):
    try:
        image = Image.objects.get(id=image_id)
    except Image.DoesNotExist:
        return JsonResponse({'error': 'Image Not Found'}, status=404)

    if not image.can_convert_to(ext):
        return JsonResponse({'error': 'Provided image extension is invalid'}, status=400)

    if image.get_extension() == ext:
        return JsonResponse({'error': 'Provided image is already has {} extension'.format(ext)}, status=400)

    ext_image = image.get_converted_image(ext)
    if not ext_image:
        ext_image = image.convert_image(ext)

    return JsonResponse(ext_image.to_json(), status=200)
