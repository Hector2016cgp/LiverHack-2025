# vacantes/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Vacante
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class VacanteForm(forms.ModelForm): # O forms.Form si no usas un modelo
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # --- Clases de CSS comunes para todos los campos ---
        common_classes = "mt-1 block w-full rounded-md border-slate-800 shadow-sm focus:border-pink-500 focus:ring-pink-500 sm:text-sm"
        
        # --- Aplicar clases y placeholders ---
        self.fields['titulo'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Ej: Gerente de Ventas'
        })
        self.fields['departamento'].widget.attrs.update({'class': common_classes})
        self.fields['ubicacion'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Ej: Ciudad de México'
        })
        self.fields['nivel'].widget.attrs.update({'class': common_classes})
        self.fields['tipo_contrato'].widget.attrs.update({'class': common_classes})
        self.fields['prioridad'].widget.attrs.update({'class': common_classes})
        self.fields['salario_minimo'].widget.attrs.update({
            'class': common_classes,
            'placeholder': '15000'
        })
        self.fields['salario_maximo'].widget.attrs.update({
            'class': common_classes,
            'placeholder': '25000'
        })
        
        self.fields['fecha_cierre'].widget = forms.DateInput(
            attrs={
                'type': 'date',
                'class': common_classes,
                'placeholder': 'dd/mm/aaaa'
            }
        )
        self.fields['responsable_rh'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Nombre del reclutador'
        })
        self.fields['descripcion'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Describe las responsabilidades y el rol...',
            'rows': 4
        })
        self.fields['requisitos'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Lista los requisitos y habilidades necesarias...',
            'rows': 4
        })

    class Meta:
        model = Vacante
        fields = '__all__'

class AdminAuthenticationForm(AuthenticationForm):
    """
    Formulario de autenticación personalizado para staff.
    """
    error_messages = {
        **AuthenticationForm.error_messages,
        "invalid_login": _(
            "Por favor ingresa el usuario y contraseña correctos para una cuenta de staff. Ambos campos distinguen mayúsculas y minúsculas."
        ),
    }
    required_css_class = "required"

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_staff:
            raise ValidationError(
                self.error_messages["invalid_login"],
                code="invalid_login",
                params={"username": self.username_field.verbose_name},
            )
        
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user