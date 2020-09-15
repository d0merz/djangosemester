from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from music.models import Genre, Song


class Profile(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True)
    gender = models.CharField(max_length=1,
                              choices=GENDER_CHOICES,
                              default=MALE,
                              null=False,
                              blank=False)
    love_genres = models.ManyToManyField(Genre,
                                         related_name='users',
                                         related_query_name='users',
                                         blank=True)
    track_counts = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('account:profile-detail', args=[self.id])


class TrackUser(models.Model):
    user = models.ForeignKey('auth.User',
                             related_name='tracks_set',
                             related_query_name='tracks_set',
                             on_delete=models.CASCADE)
    track = models.ForeignKey(Song,
                              related_name='owners_set',
                              related_query_name='owners_set',
                              on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True,
                                 db_index=True)

    class Meta:
        ordering = ('added',)


class Playlist(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название плейлиста', db_index=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='playlists',
                               related_query_name='playlists')
    image = models.ImageField(upload_to="images/albums", null=True, blank=True)
    published = models.DateField(auto_now_add=True)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    tracks = models.ManyToManyField(Song, related_name='playlists', related_query_name='playlists',
                                    through='TrackPlaylist')
    isPrivate = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('account:playlist-detail', args=[self.id])

    def __str__(self):
        return self.title


class TrackPlaylist(models.Model):
    track = models.ForeignKey(Song, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

    def __str__(self):
        return '{} in {}'.format(self.track.title, self.playlist.title)


class PlaylistUser(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-added',)

    def __str__(self):
        return '{} add playlist {}'.format(self.user.username, self.playlist.title)


class Contact(models.Model):
    user_from = models.ForeignKey('auth.User',
                                  related_name='rel_from_set',
                                  related_query_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User',
                                related_name='rel_to_set',
                                related_query_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)


User.add_to_class('tracks',
                  models.ManyToManyField(Song,
                                         through=TrackUser,
                                         related_name='owners',
                                         related_query_name='owners',
                                         blank=True, ))

User.add_to_class('playlists',
                  models.ManyToManyField(Playlist,
                                         through=PlaylistUser,
                                         related_name='users_add_set',
                                         related_query_name='users_add_set',
                                         blank=True, ))

User.add_to_class('following',
                  models.ManyToManyField('self',
                                         through=Contact,
                                         related_name='followers',
                                         symmetrical=False))
