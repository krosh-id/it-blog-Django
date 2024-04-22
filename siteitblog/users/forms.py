from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин:',
        widget=forms.TextInput(attrs={'class': ''})
    )
    password = forms.CharField(
        label='Пароль:',
        widget=forms.PasswordInput(attrs={'class': ''})
    )


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Придумайте логин:", widget=forms.TextInput(attrs={'class': ''}))
    password1 = forms.CharField(label="Придумайте пароль:", widget=forms.PasswordInput(attrs={'class': ''}))
    password2 = forms.CharField(label="Повторите пароль:", widget=forms.PasswordInput(attrs={'class': ''}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'Введите адрес электронной почты:',
            'first_name': "Ваше имя:",
            'last_name': "Ваша фамилия:",
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': ''}),
            'first_name': forms.TextInput(attrs={'class': ''}),
            'last_name': forms.TextInput(attrs={'class': ''}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой email уже существует")
        return email
