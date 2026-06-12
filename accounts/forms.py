from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class ProfileEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['email'].initial = self.instance.email
            self.fields['first_name'].initial = self.instance.first_name
            self.fields['last_name'].initial = self.instance.last_name

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class AccountDeleteForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    def clean_password(self):
        return self.cleaned_data.get('password')


class CustomSignupForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}), label='Confirm Password')

    color_scheme = forms.ChoiceField(
        choices=[
            ('blue', 'Blue'),
            ('purple', 'Purple'),
            ('green', 'Green'),
            ('orange', 'Orange'),
            ('pink', 'Pink'),
            ('indigo', 'Indigo'),
        ],
        required=False,
        initial='blue',
        widget=forms.RadioSelect(),
        label='Choose Your Theme Color'
    )

    theme_mode = forms.ChoiceField(
        choices=[
            ('light', 'Light Mode'),
            ('dark', 'Dark Mode'),
        ],
        required=False,
        initial='light',
        widget=forms.RadioSelect(),
        label='Choose Your Theme'
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match.')

        return cleaned_data

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )

        # Update UserProfile with theme preferences (signal creates it automatically)
        user.userprofile.color_scheme = self.cleaned_data.get('color_scheme', 'blue')
        user.userprofile.theme_mode = self.cleaned_data.get('theme_mode', 'light')
        user.userprofile.save()

        return user


