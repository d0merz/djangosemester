from django.db import models
from django.urls import reverse
from music.validators import validate_file_extension


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name='Genre name', unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = 'Genres'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('music:song_list_by_genre', args=[self.slug])


class Singer(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    image = models.ImageField(upload_to="images/singers", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Singers'
        ordering = ['name', ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('music:singer_detail', args=[self.id, ])


class Album(models.Model):
    title = models.CharField(max_length=100, verbose_name='Album title', db_index=True)
    image = models.ImageField(upload_to="images/albums", null=True, blank=True)
    author = models.ForeignKey(Singer, on_delete=models.CASCADE, related_name='albums', related_query_name='album')
    published = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('music:album_detail', args=[self.id])

    class Meta:
        verbose_name_plural = 'Albums'
        ordering = ['-published', 'author', 'title']
        get_latest_by = 'published'


class Song(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    image = models.ImageField(upload_to="images/songs", null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_query_name='songs',
                              related_name='songs')
    track = models.FileField(upload_to='songs/%Y/%m/%d', validators=[validate_file_extension])
    published = models.DateField(null=True, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True, related_name='songs',
                              related_query_name='songs')
    singers = models.ManyToManyField(Singer, related_name='songs')
    clip_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('music:song_detail', args=[self.id])

    class Meta:
        verbose_name_plural = 'Songs'
        ordering = ['-published', 'title']
        get_latest_by = 'published'
