from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from account.models import Profile, TrackUser, Playlist, TrackPlaylist, PlaylistUser
from music.models import Song



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo', 'get_photo', 'track_counts')
    readonly_fields = ('get_photo',)
    search_fields = ('user',)
    autocomplete_fields = ('love_genres',)
    list_filter = ('love_genres',)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src={obj.photo.url} height="80"')
        else:
            return '-'


@admin.register(TrackUser)
class TrackUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'track', 'added')
    sortable_by = ('-added',)
    search_fields = ('user', 'track')


@admin.register(TrackPlaylist)
class TrackPlaylistAdmin(admin.ModelAdmin):
    list_display = ('playlist', 'track')


@admin.register(PlaylistUser)
class PlaylistUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'playlist', 'added')
    ordering = ('-added', )


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published', 'get_image', 'description', 'isPrivate')
    readonly_fields = ('get_image',)
    list_editable = ('isPrivate', )
    search_fields = ('^title',)
    autocomplete_fields = ('author', 'tracks')
    filter_horizontal = ('tracks',)
    list_filter = ('author',)
    sortable_by = ['published', 'author', 'title']
    ordering = ('author', '-published', 'title',)
    save_on_top = True

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} height="80"')
        else:
            return '-'

    get_image.short_description = "Image"
