from django import forms
from .models import Reclamacion

class ReclamacionForm(forms.ModelForm):
    class Meta:
        model = Reclamacion
        fields = ['cuerpo']  # Los campos que quieres incluir en el formulario

    def __init__(self, *args, **kwargs):
        super(ReclamacionForm, self).__init__(*args, **kwargs)
        # Aquí puedes personalizar los campos del formulario si es necesario
        self.fields['cuerpo'].widget = forms.Textarea(attrs={'placeholder': 'Escribe tu reclamación aquí', 'cols': None})
        self.fields['cuerpo'].label = ''  # Esto establecerá la etiqueta en blanco