import math

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.core.files.storage import FileSystemStorage
from django.db.models import F, Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView

from MusicProject.settings import EMAIL_HOST_USER
from account.decorators import ajax_required
from account.forms import LoginForm, UserRegistrationForm, ProfileForm, UserEditForm, PhotoProfileForm, PlaylistForm, \
    PasswordResetForm
from account.models import Profile, TrackUser, Playlist, PlaylistUser, Contact
from music.models import Song


class CustomLoginView(LoginView):
    template_name = 'account/login.html'
    form = LoginForm
    redirect_authenticated_user = 'music/'


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            new_user.save()
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user, }, )
        return render(request,
                      'account/registration.html',
                      {'user_form': user_form, }, )
    else:
        user_form = UserRegistrationForm()
        return render(request,
                      'account/registration.html',
                      {'user_form': user_form, }, )


@login_required
def user_profile(request):
    avatar_form = PhotoProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileForm(instance=request.user.profile, data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлен')
        else:
            messages.error(request, 'Что-то пошло не так')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request,
                  'account/profile.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'avatar_form': avatar_form, })


@login_required
@require_POST
def change_avatar(request):
    avatar_form = PhotoProfileForm(request.POST, request.FILES)
    if avatar_form.is_valid():
        fs = FileSystemStorage()
        img = request.FILES['photo']
        filename = fs.save(img.name, img)
        Profile.objects.filter(user=request.user).update(photo=img)
    return redirect('account:profile')


@ajax_required
@login_required
@require_POST
def add_song(request):
    song_id = request.POST.get('id')
    action = request.POST.get('action')
    cur_user = request.user
    if song_id and action:
        try:
            song = Song.objects.get(id=song_id)
            if action == 'add':
                TrackUser.objects.get_or_create(user=request.user,
                                                track=song)
                Profile.objects.filter(user=cur_user).update(track_counts=F('track_counts') + 1)

            else:
                TrackUser.objects.filter(user=request.user,
                                         track=song).delete()
                Profile.objects.filter(user=cur_user).update(track_counts=F('track_counts') - 1)
            return JsonResponse({'status': 'ok', })
        except Song.DoesNotExist:
            return JsonResponse({'status': 'ok', })
    return JsonResponse({'status': 'ok'})


@login_required
def user_tracks(request):
    playlists = Playlist.objects.filter(Q(author=request.user.profile) | Q(users_add_set=request.user)).distinct()
    playlist_form = PlaylistForm()
    if playlists:
        print(playlists)
        playlist_count = playlists.count()
        count_slide_page = math.ceil(playlist_count / 3)
        slides = None
        if count_slide_page > 1:
            slides = range(1, count_slide_page)
    else:
        slides = None
    return render(request,
                  'account/user_musics.html',
                  {'songs': request.user.tracks.all(),
                   'slides': slides,
                   'playlist_form': playlist_form,
                   'playlists': playlists}, )


class ProfileListView(ListView):
    template_name = 'account/user_list.html'
    model = Profile
    context_object_name = 'profiles'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Profile.objects.exclude(user=self.request.user)
        else:
            return Profile.objects.all()


class ProfileDetailView(DetailView):
    model = Profile
    pk_url_kwarg = 'id'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        playlists = self.object.playlists.filter(isPrivate=False)
        isHavePlaylists = False
        if playlists.count() > 0:
            isHavePlaylists = True
        if playlists:
            album_counts = playlists.count()
            count_slide_page = math.ceil(album_counts / 3)
            slides = None
            if count_slide_page > 1:
                slides = range(1, count_slide_page)
        else:
            slides = None
        context['slides'] = slides
        context['albums'] = playlists
        context['isHavePlaylists'] = isHavePlaylists
        return context


@login_required
@require_POST
def playlist_create(request):
    playlist_form = PlaylistForm(request.POST, request.FILES)
    if playlist_form.is_valid():
        playlist = playlist_form.save(commit=False)
        playlist.author = request.user.profile
        playlist.save()
    return redirect('account:my-music')


@login_required
def playlist_detail(request, id):
    playlist = get_object_or_404(Playlist, id=id)
    is_playlist_from_cur_user = playlist.author.id == request.user.profile.id
    if (request.method == 'POST') & is_playlist_from_cur_user:
        playlist_form = PlaylistForm(instance=playlist, data=request.POST)
        if playlist_form.is_valid():
            playlist_form.save()
            messages.success(request, "Плэйлист успешно обновлен")
    else:
        if playlist.isPrivate & ~is_playlist_from_cur_user:
            return HttpResponse('Плейлист приватный')
        playlist_form = PlaylistForm(instance=playlist)
    return render(request, 'account/playlist_detail.html',
                  {'album': playlist,
                   'form': playlist_form,
                   'is_user_playlist': is_playlist_from_cur_user, }, )


@ajax_required
@login_required
@require_POST
def add_playlist(request):
    playlist_id = request.POST.get('id')
    action = request.POST.get('action')
    if playlist_id and action:
        try:
            playlist = Playlist.objects.get(id=playlist_id)
            if action == 'add':
                PlaylistUser.objects.get_or_create(user=request.user,
                                                   playlist=playlist)
            else:
                PlaylistUser.objects.filter(user=request.user, playlist=playlist).delete()
            return JsonResponse({'status': 'ok', })
        except Playlist.DoesNotExist:
            return JsonResponse({'status': 'ok', })
    return JsonResponse({'status': 'ok'})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'ok'})


class CustomPasswordResetView(PasswordResetView):
    template_name = 'account/password_reset.html'
    subject_template_name = 'email/reset_letter_subject.txt'
    email_template_name = 'email/reset_letter_body.txt'
    success_url = reverse_lazy('account:password_reset_done')
    form_class = PasswordResetForm
    from_email = EMAIL_HOST_USER


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/password_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'account/password_complete.html'
