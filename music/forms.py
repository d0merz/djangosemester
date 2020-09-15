from django import forms
from django_select2 import forms as s2forms

from music.models import Album, Singer, Song
from music.validators import validate_file_extension


class SongForm(forms.ModelForm):
    track = forms.FileField(validators=[validate_file_extension], label='Файл с треком')
    published = forms.DateField(required=False,
                                label='Дата публикации',
                                help_text='В формате YYYY-mm-dd')

    class Meta:
        model = Song
        widgets = {
            'genre': forms.RadioSelect,
            'singers': s2forms.Select2MultipleWidget,
            'album': s2forms.Select2Widget,
        }
        fields = ('title', 'track', 'singers', 'image', 'album', 'published', 'genre', 'clip_link')


class SingerForm(forms.ModelForm):
    class Meta:
        model = Singer
        fields = ('name', 'image',)


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('title', 'image', 'author', 'published')
        widgets = {
            'author': s2forms.Select2Widget(),
        }





