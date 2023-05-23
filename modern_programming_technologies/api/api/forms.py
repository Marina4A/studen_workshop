from django import forms
from .models import RepairJob


class RepairJobForm(forms.ModelForm):
    class Meta:
        model = RepairJob
        fields = ['car_model', 'description', 'price']

