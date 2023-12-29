# forms.py
from django import forms
from .models import Profile

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'interests', 'profile_image', 'hero_image']
