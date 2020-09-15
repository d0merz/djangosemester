from rest_framework import serializers

from music.models import Song, Album, Singer, Genre


class SongSerializer(serializers.ModelSerializer):
    album = serializers.SlugRelatedField(slug_field='title', read_only=True)
    genre = serializers.SlugRelatedField(slug_field='name', read_only=True)
    singers = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)

    class Meta:
        model = Song
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Album
        fields = '__all__'


class SingerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Singer
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('slug',)
