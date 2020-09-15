from django.contrib.auth import views as auth_views
from django.urls import path

from account import views
from account.views import ProfileListView, CustomLoginView, ProfileDetailView, CustomPasswordResetDoneView, \
    CustomPasswordResetView, CustomPasswordResetCompleteView, CustomPasswordResetConfirmView

app_name = 'account'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile-user/<int:id>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/', views.user_profile, name='profile'),
    path('add_song/', views.add_song, name='add-song'),
    path('change_avatar/', views.change_avatar, name='change-avatar'),
    path('my-music/', views.user_tracks, name='my-music'),
    path('profiles/', ProfileListView.as_view(), name='profile-list'),
    path('playlist/<int:id>', views.playlist_detail, name='playlist-detail'),
    path('playlist/add/', views.playlist_create, name='playlist-create'),
    path('add_playlist/', views.add_playlist, name='add-playlist'),
    path('follow/', views.user_follow, name='user_follow'),
    path('password/reset/done/', CustomPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password/reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password/confirm/complete/', CustomPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('password/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
]
