

# forms.py
from django import forms
from .models import UploadExcel
from django.forms import ClearableFileInput


class FileFieldForm(forms.ModelForm):
    class Meta:
        model = UploadExcel
        fields = ['file_field']
        widgets = {
            'file_field': ClearableFileInput(attrs={'multiple': True}),
        }
