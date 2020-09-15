from django.urls import path, re_path, include

from music.views import SingerCreate, AlbumCreate, SongCreate, AlbumListView, SingerListView
from . import views

app_name = 'music'

urlpatterns = [
    path('', views.song_list, name='song_list'),
    path('recommendations/', views.get_rec_music, name='rec-music'),
    path('create-content/', views.add_content, name='add-content'),
    path('song/add/', SongCreate.as_view(), name='song_create'),
    path('singer/add/', SingerCreate.as_view(), name='singer_create'),
    path('singer/list', SingerListView.as_view(), name='singer-list'),
    path('album/add/', AlbumCreate.as_view(), name='album_create'),
    path('album/list/', AlbumListView.as_view(), name='album-list'),
    path('singer/<int:id>/', views.SingerDetailView.as_view(), name='singer_detail'),
    re_path(r'^song/(?P<pk>[0-9]+)/', views.SongDetailView.as_view(), name='song_detail'),
    re_path(r'^album/(?P<pk>[0-9]+)/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('<slug:genre_slug>/', views.song_list, name='song_list_by_genre'),
]
