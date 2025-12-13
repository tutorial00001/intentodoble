from django import forms
from .models import Practica

class EditPerfilForm(forms.ModelForm):
    class Meta:
        model = Practica
        fields = ['email', 'bio', 'location', 'website', 'avatar_url']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

