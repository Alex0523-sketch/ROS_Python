import re
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError


class EmailPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label='Correo electrónico',
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'email',
                'placeholder': 'tu@correo.com',
            }
        ),
    )

    def get_users(self, email):
        """El modelo `User` usa el campo `activo`, no `is_active`, en la base de datos."""
        UserModel = get_user_model()
        email_field = UserModel.get_email_field_name()
        if not hasattr(UserModel, 'activo'):
            return super().get_users(email)
        active_users = UserModel._default_manager.filter(
            **{f'{email_field}__iexact': email},
            activo=True,
        )
        return (u for u in active_users.iterator() if u.has_usable_password())


def _validar_contrasena(value):
    errores = []
    if len(value) < 8:
        errores.append('Debe tener al menos 8 caracteres.')
    if not re.search(r'[A-Z]', value):
        errores.append('Debe contener al menos una letra mayúscula.')
    if not re.search(r'[a-z]', value):
        errores.append('Debe contener al menos una letra minúscula.')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>\-_=+\[\]\\/;\'\'`~]', value):
        errores.append('Debe contener al menos un carácter especial (!@#$%...).')
    if errores:
        raise ValidationError(errores)


class StyledSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].label = 'Nueva contraseña'
        self.fields['new_password2'].label = 'Confirmar contraseña'
        self.fields['new_password1'].help_text = ''
        for name in ('new_password1', 'new_password2'):
            if name in self.fields:
                self.fields[name].widget.attrs.update(
                    {
                        'class': 'form-control',
                        'autocomplete': 'new-password',
                    }
                )

    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1', '')
        _validar_contrasena(password)
        return password

    def clean_new_password2(self):
        p1 = self.cleaned_data.get('new_password1', '')
        p2 = self.cleaned_data.get('new_password2', '')
        if p1 and p2 and p1 != p2:
            raise ValidationError('Las contraseñas no coinciden.')
        return p2
