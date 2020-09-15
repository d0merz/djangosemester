from rest_framework.viewsets import ModelViewSet

from music.models import Song, Singer, Album, Genre
from music.serializers import SongSerializer, SingerSerializer, AlbumSerializer, GenreSerializer


class APISongViewSet(ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = ()


class APISingerViewSet(ModelViewSet):
    queryset = Singer.objects.all()
    serializer_class = SingerSerializer


class APIAlbumViewSet(ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class APIGenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
