from django import forms
from django.contrib.auth.forms import PasswordResetForm as PasswordResetFormCore
from django.contrib.auth.models import User
from django_select2 import forms as s2forms
from account.models import Profile, Playlist

from account.tasks import send_mail_task


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('love_genres', 'gender')
        widgets = {
            'love_genres': forms.CheckboxSelectMultiple(),
            'gender': forms.RadioSelect,
        }
        labels = {
            'love_genres': 'Любимые жанры',
            'gender': 'Ваш пол',
        }


class PhotoProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo',)


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        exclude = ('author', 'published',)
        widgets = {
            'tracks': s2forms.Select2MultipleWidget,
            'description': forms.Textarea,
            'isPrivate': forms.CheckboxInput,
        }


class PasswordResetForm(PasswordResetFormCore):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'email',
            'placeholder': 'Email'
        }
    ))

    def send_mail(self, subject_template_name, email_template_name, context,
                  from_email, to_email, html_email_template_name=None):
        context['user'] = context['user'].id

        send_mail_task.delay(subject_template_name=subject_template_name,
                             email_template_name=email_template_name,
                             context=context, from_email=from_email, to_email=to_email,
                             html_email_template_name=html_email_template_name)

# class PasswordResetRequestForm(forms.Form):
#     email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)
#
#
# class SetPasswordForm(forms.Form):
#     """
#     A form that lets a user change set their password without entering the old
#     password
#     """
#     error_messages = {
#         'password_mismatch': ("The two password fields didn't match."),
#         }
#     new_password1 = forms.CharField(label=("New password"),
#                                     widget=forms.PasswordInput)
#     new_password2 = forms.CharField(label=("New password confirmation"),
#                                     widget=forms.PasswordInput)
#
#     def clean_new_password2(self):
#         password1 = self.cleaned_data.get('new_password1')
#         password2 = self.cleaned_data.get('new_password2')
#         if password1 and password2:
#             if password1 != password2:
#                 raise forms.ValidationError(
#                     self.error_messages['password_mismatch'],
#                     code='password_mismatch',
#                     )
#         return password2
