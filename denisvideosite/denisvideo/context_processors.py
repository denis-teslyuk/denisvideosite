from denisvideo.models import Tag


def get_tags(request):
    return {'tags': Tag.objects.all()}