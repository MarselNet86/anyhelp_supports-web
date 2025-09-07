from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


BASE_CLASS_INPUT = "w-full px-4 py-3 bg-white border border-gray-200 rounded-2xl text-gray-900 text-sm focus:outline-none focus:ring-2 focus:ring-brand-orange focus:border-transparent transition-all duration-200"


class EmailAuthForm(forms.Form):
    username = forms.EmailField(
        label="email",
        widget=forms.EmailInput(
            attrs={
                "autofocus": True,
                "class": BASE_CLASS_INPUT,
                "placeholder": "Введите почту",
                "autocomplete": "email"
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "autofocus": True,
                "class": BASE_CLASS_INPUT,
                "placeholder": "Введите пароль",
            }
        ),
    )

    error_messages = {
        "invalid_login": "Неверная почта или пароль.",
        "inactive": "Учётная запись отключена.",
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get("username")
        password = cleaned.get("password")
        if email and password:
            # Находим реальный username по e-mail
            try:
                user_obj = User.objects.get(email__iexact=email)
                username = user_obj.get_username()
            except User.DoesNotExist:
                username = email  # fallback: вдруг админ ввёл e-mail и в username
            user = authenticate(self.request, username=username, password=password)
            if user is None:
                raise forms.ValidationError(self.error_messages["invalid_login"])
            if not user.is_active:
                raise forms.ValidationError(self.error_messages["inactive"])
            self.user = user
        return cleaned

    def get_user(self):
        return self.user