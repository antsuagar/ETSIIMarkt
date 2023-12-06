from django import forms
from .models import Opinion

class OpinionForm(forms.ModelForm):
    class Meta:
        model = Opinion
        fields = ['cuerpo']  # Los campos que quieres incluir en el formulario

    def __init__(self, *args, **kwargs):
        super(OpinionForm, self).__init__(*args, **kwargs)
        # Aquí puedes personalizar los campos del formulario si es necesario
        self.fields['cuerpo'].widget = forms.Textarea(attrs={'placeholder': 'Escribe tu opinión aquí'})