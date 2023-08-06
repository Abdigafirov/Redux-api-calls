from django import forms
from .models import Dweet, Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user',  'image']

        widgets = {
            'image': forms.FileInput(attrs={'accept': 'images/*'}),
        }


class DweetFrom(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Dweet something...",
                "class": "textarea is-success is-medium",
            }
        ),
        label="",
    )

    class Meta:
        model = Dweet
        exclude = ("user", )


