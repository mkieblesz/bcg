from django.http import JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404
from progimage.models import Image


def upload_image(request):
    if request.method != 'POST':
        return HttpResponse('', status=405)

    image = Image.objects.create(image_file=request.FILES.get('image'))

    return JsonResponse(image.to_json())


def get_image(request):
    image = get_object_or_404(Image, id=request.GET.get('id', None))

    return JsonResponse(image.to_json())
