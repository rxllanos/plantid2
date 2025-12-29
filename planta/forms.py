from django import forms
from .models import Plant


class PlantPictureForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['user','plant_image', 'plant_latitude', 'plant_longitude']
        widgets = {
            'user': forms.HiddenInput(),
        }