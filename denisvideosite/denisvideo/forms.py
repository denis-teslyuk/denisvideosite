from django import forms

from denisvideo.models import Video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('file', 'name', 'preview', 'description', 'tags',)


