'''from django import forms
from uploads.core.models import Document

class UserDataForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('username', 'file' )'''

from django import forms
from data.models import UserData

class UserDataForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ('username', 'file', )