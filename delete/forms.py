from django import forms
from lectorqr.models import Paciente

class DeleteAccountForm(forms.Form):
    last_name = forms.CharField(
        label="Escribe el código para confirmar",
        widget=forms.TextInput(attrs={
            'class': 'form-control',            
        })
    )
    
    qr_id = forms.CharField(
        label="Una vez más",
        widget=forms.TextInput(attrs={
            'class': 'form-control',            
        })
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        last_name = cleaned_data.get('last_name')
        qr_id = cleaned_data.get('qr_id')
        
        # 1. Validar apellido
        if self.user and last_name != self.user.last_name:
            self.add_error('last_name', "El apellido no coincide con el registrado.")
        
        # 2. Validar existencia del Paciente por ID QR
        if qr_id:
            try:
                paciente = Paciente.objects.get(id=qr_id)
                # Guardamos la instancia para usarla en la vista
                cleaned_data['paciente_instance'] = paciente
            except Paciente.DoesNotExist:
                self.add_error('qr_id', "No se encontró ningún paciente con este ID QR.")
        
        return cleaned_data
