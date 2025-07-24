from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Profile, Settings, Post
from django.contrib.auth.models import User 

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'})
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'})
    )
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        })

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nombre de usuario'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Contraseña'
    }))

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Correo electrónico'
    }))

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nueva contraseña'
        }))
    new_password2 = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar nueva contraseña'
        }))

class ProfileEditForm(forms.ModelForm):
    # Campos para el modelo User
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre'
        }))
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellido'
        }))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo electrónico'
        }))
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario'
        }))
    
    # Campo para el modelo Settings
    profile_visibility = forms.ChoiceField(
        choices=Settings.VISIBILITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture_url']  # Solo campos del modelo Profile
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegurarse de que los campos existan antes de asignar valores iniciales
        self.fields.setdefault('first_name', forms.CharField())
        self.fields.setdefault('last_name', forms.CharField())
        self.fields.setdefault('email', forms.EmailField())
        self.fields.setdefault('username', forms.CharField())
        self.fields.setdefault('profile_visibility', forms.ChoiceField())
        
        if self.instance and self.instance.user:
            # Inicializar campos de User
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['username'].initial = self.instance.user.username
            
            # Inicializar visibilidad
            if hasattr(self.instance.user, 'settings'):
                self.fields['profile_visibility'].initial = self.instance.user.settings.profile_visibility

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        
        # Actualizar campos de User
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        
        # Guardar configuración de visibilidad
        if hasattr(user, 'settings'):
            user.settings.profile_visibility = self.cleaned_data['profile_visibility']
            if commit:
                user.settings.save()
        
        if commit:
            user.save()
            profile.save()
        return profile
    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text_content', 'media_url']
        widgets = {
            'text_content': forms.Textarea(attrs={
                'placeholder': '¿Qué deseas publicar?',
                'rows': 3,
                'class': 'PubTextarea'
            }),
            'media_url': forms.URLInput(attrs={
                'class': 'hidden',  # Oculto, se manejará con JavaScript
                'id': 'media-url-input'
            })
        }
        labels = {
            'text_content': '',
            'media_url': ''
        }