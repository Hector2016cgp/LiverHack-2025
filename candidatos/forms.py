from django import forms
from django.contrib.auth.models import User
from candidatos.models import Candidato

class PerfilCandidatoForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='Nombre',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent',
            'placeholder': 'Tu nombre'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='Apellidos',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent',
            'placeholder': 'Tus apellidos'
        })
    )
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent',
            'placeholder': 'tu@email.com'
        })
    )

    class Meta:
        model = Candidato
        fields = [
            'cv',
            'linkedin', 
            'github',
            'resumen',
        ]
        widgets = {
            'cv': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent',
            }),
            'linkedin': forms.URLInput(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent',
                'placeholder': 'https://linkedin.com/in/tu-perfil'
            }),
            'github': forms.URLInput(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent',
                'placeholder': 'https://github.com/tu-usuario'
            }),
            'resumen': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent',
                'rows': 4,
                'placeholder': 'Describe tu experiencia, habilidades y objetivos profesionales...'
            }),
        }
        labels = {
            'cv': 'Curriculum Vitae',
            'linkedin': 'Perfil de LinkedIn',
            'github': 'Perfil de GitHub',
            'resumen': 'Resumen Profesional',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and hasattr(self.instance, 'user'):
            user = self.instance.user
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        candidato = super().save(commit=False)
        
        if hasattr(candidato, 'user') and candidato.user:
            candidato.user.first_name = self.cleaned_data['first_name']
            candidato.user.last_name = self.cleaned_data['last_name']
            candidato.user.email = self.cleaned_data['email']
            if commit:
                candidato.user.save()
                candidato.save()
        
        return candidato