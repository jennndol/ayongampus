""" This file contains forms for authentication process """

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from ayongampus.settings import ALLOWED_SIGNUP_DOMAINS


def signup_domain_validator(value):
    """signup_domain_validator is a function to make validation while signup"""
    if '*' not in ALLOWED_SIGNUP_DOMAINS:
        try:
            domain = value[value.index("@"):]
            if domain not in ALLOWED_SIGNUP_DOMAINS:
                raise ValidationError(
                    u'Invalid domain. Allowed domains on this network: {0}'.format(
                        ','.join(ALLOWED_SIGNUP_DOMAINS)))

        except Exception:
            raise ValidationError(
                u'Invalid domain. Allowed domains on this network: {0}'.format(
                    ','.join(ALLOWED_SIGNUP_DOMAINS)))


def forbidden_usernames_validator(value):
    """
    forbidden_usernames_validator is a function
    in which forbidden_usernames cannot be taken to be username
    """
    forbidden_usernames = ['admin', 'settings', 'news', 'about', 'help',
                           'signin', 'signup', 'signout', 'terms', 'privacy',
                           'cookie', 'new', 'login', 'logout', 'administrator',
                           'join', 'account', 'username', 'root', 'blog',
                           'user', 'users', 'billing', 'subscribe', 'reviews',
                           'review', 'blog', 'blogs', 'edit', 'mail', 'email',
                           'home', 'job', 'jobs', 'contribute', 'newsletter',
                           'shop', 'profile', 'register', 'auth',
                           'authentication', 'campaign', 'config', 'delete',
                           'remove', 'forum', 'forums', 'download',
                           'downloads', 'contact', 'blogs', 'feed', 'feeds',
                           'faq', 'intranet', 'log', 'registration', 'search',
                           'explore', 'rss', 'support', 'status', 'static',
                           'media', 'setting', 'css', 'js', 'follow',
                           'activity', 'questions', 'articles', 'network', ]

    if value.lower() in forbidden_usernames:
        raise ValidationError(_('This is a reserved word.'))


def invalid_username_validator(value):
    """
    invalid_username_validator is a function to make validation
    in which there are symbols cannot be used to be username
    """
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError(_('Enter a valid username.'))


def unique_email_validator(value):
    """
    unique_email_validator is a function to make sure email
    that can be used for signup is unique
    """
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError(_('User with this Email already exists.'))


def ignore_case_validator(value):
    """
    ignore_case_validator is used to make sure
    username that has been taken by another user cannot be used again as username
    """
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError(_('User with this Username already exists.'))


class SignUpForm(forms.ModelForm):
    """
    SignUpForm is a class where form that will be used for signup activity is initialized
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control border-input', 'placeholder': _('Username')}),
        max_length=30,
        required=True,
        help_text=_('Username may contain alphanumeric and characters'))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control border-input', 'placeholder': _('Password')}))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control border-input', 'placeholder': _('Confirm password')}),
        label=_("Confirm password"),
        required=True)
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control border-input', 'placeholder': 'Email'}),
        required=True,
        max_length=75)

    class Meta:
        """
        initialize SignUpForm
        """
        model = User
        exclude = ['last_login', 'date_joined']
        fields = ['username', 'email', 'password', 'confirm_password', ]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(forbidden_usernames_validator)
        self.fields['username'].validators.append(invalid_username_validator)
        self.fields['username'].validators.append(ignore_case_validator)
        self.fields['email'].validators.append(unique_email_validator)
        self.fields['email'].validators.append(signup_domain_validator)

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self._errors['password'] = self.error_class(
                [_('Passwords don\'t match')])
        return self.cleaned_data
