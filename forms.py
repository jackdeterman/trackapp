from django import forms
from .models import *

class UploadForm(forms.Form):
    file = forms.FileField()

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        exclude = ['id', 'athlete']

class MergeAthleteForm(forms.Form):

    user = forms.ModelChoiceField(queryset=User.objects.all().order_by('last_name'))