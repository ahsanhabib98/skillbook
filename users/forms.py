from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from users.models import UserProfile, Profile


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'text-field w-input',
        'placeholder': 'eg. ******&#x27;'
    }))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={
        'class': 'text-field w-input',
        'placeholder': 'eg. ******&#x27;'
    }))

    class Meta:
        model = UserProfile
        fields = ('name', 'email')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'text-field w-input',
                'placeholder': 'eg. moshfequr rahman',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'text-field w-input',
                'placeholder': 'eg. email@gmail.com'
            }),
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserProfile
        fields = ('email', 'password', 'name', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'email', 'designation', 'bio', 'source_bio', 'image')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'text-field w-input',
                'placeholder': 'eg. moshfequr rahman',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'text-field w-input',
                'placeholder': 'eg. email@gmail.com',
                'required': True
            }),
            'designation': forms.TextInput(attrs={
                'class': 'text-field w-input',
                'placeholder': 'eg. Webflow developer'
            }),
            'bio': forms.TextInput(attrs={
                'class': 'text-field w-input',
                'placeholder': 'eg. google.com'
            }),
            'source_bio': forms.TextInput(attrs={
                'class': 'text-field w-input',
                'placeholder': 'eg. Why this source is important?'
            }),
        }
