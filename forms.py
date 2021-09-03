from django import forms
from .models import *

class UploadForm(forms.Form):
    file = forms.FileField()
    team = forms.ModelChoiceField(queryset=Team.objects.all().order_by('name'))
    #season = forms.ModelChoiceField(queryset=Season.objects.all().order_by('name'))

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

class SeasonGoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        exclude = ['user', 'creator', 'meet']


class MergeMeetForm(forms.Form):

    user = forms.ModelChoiceField(queryset=Meet.objects.all().order_by('date'))

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']


