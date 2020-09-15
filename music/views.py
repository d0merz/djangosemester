import math

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.db.models import Count, Max, Q
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, CreateView, ListView

from account.forms import PasswordResetForm
from account.models import TrackUser
from music.forms import SongForm, SingerForm, AlbumForm
from music.models import Song, Genre, Singer, Album


class AlbumCreate(CreateView):
    form_class = AlbumForm
    model = Album

    def get_success_url(self):
        return reverse('music:add-content')


class SingerCreate(CreateView):
    form_class = SingerForm
    model = Singer

    def get_success_url(self):
        return reverse('music:add-content')


class SongCreate(CreateView):
    form_class = SongForm
    model = Song

    def get_success_url(self):
        return reverse('music:add-content')


def song_list(request, genre_slug=None, ):
    genre = None
    genres = Genre.objects.all()
    songs = Song.objects.all()
    search_q = request.GET.get('q')
    if search_q:
        songs = songs.filter(Q(title__icontains=search_q) | Q(singers__name__icontains=search_q)).distinct()
    if genre_slug:
        genre = get_object_or_404(Genre, slug=genre_slug)
        songs = songs.filter(genre=genre)
    return render(request, 'music/song_list.html',
                  {'genre': genre,
                   'genres': genres,
                   'songs': songs})


class AlbumDetailView(DetailView):
    model = Album
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genres = Genre.objects.filter(songs__album=self.object)

        count_song_by_genre = genres.annotate(cnt=Count("songs"))

        max_count_genre = count_song_by_genre.aggregate(Max('cnt'))['cnt__max']

        rec_genre = count_song_by_genre.filter(cnt=max_count_genre).first()

        rec_albs = Album.objects.filter(Q(author__name=self.object.author.name) | Q(songs__genre__name=rec_genre)) \
            .exclude(id=self.object.id) \
            .distinct()
        context['songs_count_by_genre'] = count_song_by_genre
        context['rec_albs'] = rec_albs
        return context


class SingerDetailView(DetailView):
    model = Singer
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        albums = self.object.albums.all()
        if albums:
            album_counts = albums.count()
            count_slide_page = math.ceil(album_counts / 3)
            print(count_slide_page)
            slides = None
            if count_slide_page > 1:
                slides = range(1, count_slide_page)
            print(slides)
        else:
            slides = None
        context['slides'] = slides
        context['albums'] = albums
        return context


class SongDetailView(DetailView):
    model = Song

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def get_rec_music(request):
    cur_user = request.user
    love_genres = cur_user.profile.love_genres.all()
    cur_user_tracks = cur_user.tracks.values('singers')
    similar_users = TrackUser.objects.values('user') \
        .filter((~Q(user=cur_user)) & Q(track__in=cur_user_tracks))
    q = ''
    if cur_user_tracks.exists():
        q1 = Q(singers__in=cur_user_tracks) | Q(owners_set__in=similar_users)
        q = q1

    if love_genres.exists():
        q2 = Q(genre__in=love_genres)
        if q == '':
            q = q2
        else:
            q = q | q2

    if q != '':
        rec = Song.objects.filter(q).distinct()
    else:
        rec = Song.objects.all()
    print(rec)
    return render(request,
                  'music/recommendations.html',
                  {'songs': rec, })


def add_content(request):
    album_form = AlbumForm()
    song_form = SongForm()
    singer_form = SingerForm()
    return render(request,
                  'music/create_content.html',
                  {'album_form': album_form,
                   'song_form': song_form,
                   'singer_form': singer_form, }, )


class AlbumListView(ListView):
    template_name = 'music/album_list.html'
    model = Album
    context_object_name = 'albums'


class SingerListView(ListView):
    template_name = 'music/singer_list.html'
    model = Singer
    context_object_name = 'singers'


def main(request):
    return redirect('music:song_list')
