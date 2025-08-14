from denisvideosite.settings import DEFAULT_USER_PHOTO


def get_default_photo(request):
    return {'default_photo': DEFAULT_USER_PHOTO}